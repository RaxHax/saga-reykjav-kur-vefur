import tkinter as tk
from tkinter import filedialog, scrolledtext
import threading
import os
import requests
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Main Scraper Function ---
def start_scraping(url, max_photos, download_dir, log_widget, stop_event):
    
    def log(message):
        """Helper function to print messages to the UI log."""
        log_widget.config(state=tk.NORMAL)
        log_widget.insert(tk.END, message + "\n")
        log_widget.see(tk.END)
        log_widget.config(state=tk.DISABLED)

    driver = None
    try:
        log("Starting scraper...")
        
        log("Setting up Chrome driver...")
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.get(url)
        log(f"Opened URL: {url}")

        downloaded_count = 0
        processed_ids = set()

        while downloaded_count < max_photos and not stop_event.is_set():
            wait = WebDriverWait(driver, 20)
            
            try:
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.grid button.inline-flex')))
                image_buttons = driver.find_elements(By.CSS_SELECTOR, 'div.grid button.inline-flex')
            except Exception:
                log("No image buttons found on the page. Assuming end of content.")
                break

            buttons_to_process = []
            for button in image_buttons:
                try:
                    id_text = button.find_element(By.CSS_SELECTOR, 'p').text
                    if id_text and id_text not in processed_ids:
                        buttons_to_process.append((button, id_text))
                except Exception:
                    continue

            if not buttons_to_process:
                log("No new images found. Looking for 'Show More' button.")

            for button, item_id in buttons_to_process:
                if downloaded_count >= max_photos or stop_event.is_set():
                    break
                
                try:
                    driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    time.sleep(0.5)
                    button.click()

                    modal = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[role="dialog"]')))
                    
                    image_element = modal.find_element(By.CSS_SELECTOR, 'img.object-contain')
                    image_url = image_element.get_attribute('src')
                    
                    details_panel = modal.find_element(By.CSS_SELECTOR, 'div.lg\\:col-span-4')
                    text_content = details_panel.text
                    
                    # *** THIS IS THE NEW PART: Remove the unwanted text ***
                    text_to_remove = "Ertu með meiri upplýsingar um þessa mynd? Sendu okkur tölvupóst á ljosmyndasafn@reykjavik.is"
                    text_content = text_content.replace(text_to_remove, "").strip()
                    # ******************************************************
                    
                    text_filename = os.path.join(download_dir, f"{item_id}.txt")
                    image_filename = os.path.join(download_dir, f"{item_id}.jpg")

                    with open(text_filename, 'w', encoding='utf-8') as f:
                        f.write(text_content)

                    response = requests.get(image_url, stream=True)
                    response.raise_for_status()
                    with open(image_filename, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    downloaded_count += 1
                    processed_ids.add(item_id)
                    log(f"({downloaded_count}/{max_photos}) Downloaded: {item_id}")

                except Exception as e:
                    log(f"Error processing {item_id}: {e}")
                finally:
                    try:
                        close_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="loka"]')
                        close_button.click()
                        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div[role="dialog"]')))
                    except Exception:
                        pass

            if downloaded_count >= max_photos or stop_event.is_set():
                break

            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1) 
                
                show_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Sækja fleiri') or contains(., 'Sækja meira')]")))
                
                driver.execute_script("arguments[0].scrollIntoView(true);", show_more_button)
                time.sleep(0.5)
                show_more_button.click()

                log("Clicked 'Show More' button.")
                time.sleep(3)
            except Exception:
                log("Could not find 'Show More' button. Ending process.")
                break
        
        if stop_event.is_set():
            log("Stop button pressed. Scraping halted.")
        else:
            log(f"\nFinished! Downloaded {downloaded_count} photos.")

    except Exception as e:
        log(f"A critical error occurred: {e}")
    finally:
        if driver:
            driver.quit()
        app.start_button.config(state=tk.NORMAL)
        app.stop_button.config(state=tk.DISABLED)

# --- UI Class (No changes here) ---
class ScraperApp:
    def __init__(self, root):
        self.root = root
        root.title("Web Scraper UI")
        root.geometry("650x500")
        self.scraper_thread = None
        self.stop_event = threading.Event()

        settings_frame = tk.Frame(root, padx=10, pady=10)
        settings_frame.pack(fill=tk.X)

        tk.Label(settings_frame, text="Download Folder:").grid(row=0, column=0, sticky="w", pady=5)
        self.dir_entry = tk.Entry(settings_frame, width=60)
        self.dir_entry.grid(row=0, column=1, padx=5)
        self.dir_entry.insert(0, os.path.join(os.getcwd(), "downloaded_photos"))
        tk.Button(settings_frame, text="Browse...", command=self.browse_folder).grid(row=0, column=2)

        tk.Label(settings_frame, text="Max Photos:").grid(row=1, column=0, sticky="w", pady=5)
        self.max_photos_entry = tk.Entry(settings_frame, width=10)
        self.max_photos_entry.grid(row=1, column=1, sticky="w", padx=5)
        self.max_photos_entry.insert(0, "3000")

        control_frame = tk.Frame(root, padx=10, pady=5)
        control_frame.pack(fill=tk.X)
        
        self.start_button = tk.Button(control_frame, text="Start Scraping", command=self.start_thread, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=15)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = tk.Button(control_frame, text="Stop", command=self.stop_thread, bg="#f44336", fg="white", font=("Arial", 10, "bold"), width=15, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=10)

        log_frame = tk.Frame(root, padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(log_frame, text="Log:").pack(anchor="w")
        self.log_widget = scrolledtext.ScrolledText(log_frame, state=tk.DISABLED, wrap=tk.WORD, height=15)
        self.log_widget.pack(fill=tk.BOTH, expand=True)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, folder_selected)

    def start_thread(self):
        try:
            max_photos = int(self.max_photos_entry.get())
            download_dir = self.dir_entry.get()
            
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)

            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.stop_event.clear()

            self.scraper_thread = threading.Thread(
                target=start_scraping,
                args=("https://borgarsogusafn.is/myndasafn", max_photos, download_dir, self.log_widget, self.stop_event),
                daemon=True
            )
            self.scraper_thread.start()

        except ValueError:
            self.log_widget.config(state=tk.NORMAL)
            self.log_widget.insert(tk.END, "Error: 'Max Photos' must be a number.\n")
            self.log_widget.config(state=tk.DISABLED)
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def stop_thread(self):
        if self.scraper_thread and self.scraper_thread.is_alive():
            self.stop_event.set()
            self.stop_button.config(state=tk.DISABLED)

    def on_closing(self):
        self.stop_thread()
        self.root.destroy()

# --- Run the Application ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ScraperApp(root)
    root.mainloop()