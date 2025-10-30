#!/usr/bin/env python3
"""
SAGA Reykjavík - Comprehensive Feature Demonstration Script

This script demonstrates all major features of the SAGA image search platform:
1. Service health checks
2. Image indexing workflow (with FastAPI indexing service)
3. Semantic search (English)
4. Icelandic search with translation
5. Hybrid search (text + metadata)
6. Job management (pause/resume/cancel)
7. Statistics and monitoring

Usage:
    python demo_all_features.py [--demo-data-path /path/to/images]

Prerequisites:
    - Flask backend running on http://localhost:5000
    - FastAPI indexing service running on http://localhost:8001
    - Sample images in demo data path (default: ./demo_images)
"""

import requests
import time
import sys
import argparse
from pathlib import Path
from typing import Dict, Any, List
import json


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


class SAGADemo:
    """Comprehensive demonstration of SAGA platform features"""

    def __init__(self, demo_data_path: str = "./demo_images"):
        self.flask_base_url = "http://localhost:5000"
        self.indexing_base_url = "http://localhost:8001"
        self.demo_data_path = Path(demo_data_path)
        self.current_job_id = None

    def print_header(self, text: str):
        """Print a formatted header"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.END}")
        print(f"{Colors.HEADER}{Colors.BOLD}{text.center(70)}{Colors.END}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.END}\n")

    def print_step(self, step: str):
        """Print a step description"""
        print(f"{Colors.CYAN}▶ {step}{Colors.END}")

    def print_success(self, message: str):
        """Print a success message"""
        print(f"{Colors.GREEN}✓ {message}{Colors.END}")

    def print_error(self, message: str):
        """Print an error message"""
        print(f"{Colors.RED}✗ {message}{Colors.END}")

    def print_info(self, message: str):
        """Print an info message"""
        print(f"{Colors.BLUE}ℹ {message}{Colors.END}")

    def print_json(self, data: Dict[Any, Any], indent: int = 2):
        """Pretty print JSON data"""
        print(json.dumps(data, indent=indent))

    # =========================================================================
    # FEATURE 1: Health Checks
    # =========================================================================

    def check_health(self) -> bool:
        """Check health of both backend services"""
        self.print_header("FEATURE 1: Service Health Checks")

        all_healthy = True

        # Check Flask backend
        self.print_step("Checking Flask backend health...")
        try:
            response = requests.get(f"{self.flask_base_url}/api/health", timeout=5)
            if response.status_code == 200:
                self.print_success("Flask backend is healthy")
                self.print_json(response.json())
            else:
                self.print_error(f"Flask backend returned status {response.status_code}")
                all_healthy = False
        except Exception as e:
            self.print_error(f"Flask backend is not responding: {e}")
            all_healthy = False

        print()

        # Check FastAPI indexing service
        self.print_step("Checking FastAPI indexing service health...")
        try:
            response = requests.get(f"{self.indexing_base_url}/health", timeout=5)
            if response.status_code == 200:
                self.print_success("Indexing service is healthy")
                self.print_json(response.json())
            else:
                self.print_error(f"Indexing service returned status {response.status_code}")
                all_healthy = False
        except Exception as e:
            self.print_error(f"Indexing service is not responding: {e}")
            all_healthy = False

        return all_healthy

    # =========================================================================
    # FEATURE 2: Statistics
    # =========================================================================

    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        self.print_header("FEATURE 2: Database Statistics")

        self.print_step("Fetching database statistics...")
        try:
            response = requests.get(f"{self.flask_base_url}/api/stats")
            response.raise_for_status()
            stats = response.json()

            self.print_success("Statistics retrieved successfully")
            print(f"\n{Colors.BOLD}Database Statistics:{Colors.END}")
            print(f"  Collection: {stats.get('collection_name', 'N/A')}")
            print(f"  Total Images: {stats.get('count', 0):,}")
            print(f"  Vector Dimensions: {stats.get('vector_size', 'N/A')}")
            print(f"  Distance Metric: {stats.get('distance', 'N/A')}")

            return stats
        except Exception as e:
            self.print_error(f"Failed to get statistics: {e}")
            return {}

    # =========================================================================
    # FEATURE 3: Image Indexing with Job Management
    # =========================================================================

    def start_indexing(self, folder_path: str) -> str:
        """Start an indexing job"""
        self.print_header("FEATURE 3: Image Indexing with Job Management")

        self.print_step(f"Starting indexing job for folder: {folder_path}")

        try:
            payload = {
                "folder_path": folder_path,
                "options": {
                    "batch_size": 50,
                    "recursive": True,
                    "skip_existing": False,
                    "image_formats": ["jpg", "jpeg", "png", "webp"]
                }
            }

            response = requests.post(
                f"{self.indexing_base_url}/jobs/start",
                json=payload
            )
            response.raise_for_status()
            result = response.json()

            job_id = result.get('job_id')
            self.current_job_id = job_id

            self.print_success(f"Indexing job started with ID: {job_id}")
            self.print_info(f"Status: {result.get('status', 'N/A')}")

            return job_id
        except Exception as e:
            self.print_error(f"Failed to start indexing: {e}")
            return None

    def monitor_indexing(self, job_id: str, max_wait: int = 300):
        """Monitor an indexing job until completion"""
        self.print_step(f"Monitoring indexing job: {job_id}")

        start_time = time.time()
        last_progress = 0

        try:
            while time.time() - start_time < max_wait:
                response = requests.get(f"{self.indexing_base_url}/jobs/{job_id}/status")
                response.raise_for_status()
                status_data = response.json()

                status = status_data.get('status', 'unknown')
                progress = status_data.get('progress', {})
                processed = progress.get('processed', 0)
                total = progress.get('total', 0)
                percentage = progress.get('percentage', 0)

                if processed != last_progress:
                    print(f"  Progress: {processed}/{total} ({percentage:.1f}%) - Status: {status}")
                    last_progress = processed

                if status in ['completed', 'failed', 'cancelled']:
                    if status == 'completed':
                        self.print_success(f"Indexing completed! Processed {processed} images")
                    elif status == 'failed':
                        error = status_data.get('error', 'Unknown error')
                        self.print_error(f"Indexing failed: {error}")
                    elif status == 'cancelled':
                        self.print_error("Indexing was cancelled")
                    break

                time.sleep(2)
            else:
                self.print_error(f"Monitoring timed out after {max_wait} seconds")

        except Exception as e:
            self.print_error(f"Error monitoring indexing: {e}")

    def pause_job(self, job_id: str):
        """Pause an indexing job"""
        self.print_step(f"Pausing job: {job_id}")
        try:
            response = requests.post(f"{self.indexing_base_url}/jobs/{job_id}/pause")
            response.raise_for_status()
            self.print_success("Job paused successfully")
        except Exception as e:
            self.print_error(f"Failed to pause job: {e}")

    def resume_job(self, job_id: str):
        """Resume a paused indexing job"""
        self.print_step(f"Resuming job: {job_id}")
        try:
            response = requests.post(f"{self.indexing_base_url}/jobs/{job_id}/resume")
            response.raise_for_status()
            self.print_success("Job resumed successfully")
        except Exception as e:
            self.print_error(f"Failed to resume job: {e}")

    def cancel_job(self, job_id: str):
        """Cancel an indexing job"""
        self.print_step(f"Cancelling job: {job_id}")
        try:
            response = requests.post(f"{self.indexing_base_url}/jobs/{job_id}/cancel")
            response.raise_for_status()
            self.print_success("Job cancelled successfully")
        except Exception as e:
            self.print_error(f"Failed to cancel job: {e}")

    def list_jobs(self):
        """List all indexing jobs"""
        self.print_step("Listing all indexing jobs...")
        try:
            response = requests.get(f"{self.indexing_base_url}/jobs")
            response.raise_for_status()
            jobs = response.json().get('jobs', [])

            if not jobs:
                self.print_info("No indexing jobs found")
                return

            print(f"\n{Colors.BOLD}Indexing Jobs:{Colors.END}")
            for job in jobs:
                status_color = Colors.GREEN if job['status'] == 'completed' else Colors.YELLOW
                print(f"  {status_color}• ID: {job['job_id']}{Colors.END}")
                print(f"    Status: {job['status']}")
                print(f"    Folder: {job.get('folder_path', 'N/A')}")
                progress = job.get('progress', {})
                print(f"    Progress: {progress.get('processed', 0)}/{progress.get('total', 0)}")
                print()
        except Exception as e:
            self.print_error(f"Failed to list jobs: {e}")

    # =========================================================================
    # FEATURE 4: Semantic Search (English)
    # =========================================================================

    def semantic_search(self, query: str, limit: int = 10):
        """Perform semantic image search"""
        self.print_header("FEATURE 4: Semantic Search (English)")

        self.print_step(f"Searching for: '{query}'")

        try:
            payload = {
                "query": query,
                "limit": limit,
                "min_score": 0.0
            }

            response = requests.post(f"{self.flask_base_url}/api/search", json=payload)
            response.raise_for_status()
            results = response.json()

            result_list = results.get('results', [])
            self.print_success(f"Found {len(result_list)} results")

            self._display_search_results(result_list, limit=5)

            return result_list
        except Exception as e:
            self.print_error(f"Search failed: {e}")
            return []

    # =========================================================================
    # FEATURE 5: Icelandic Search with Translation
    # =========================================================================

    def icelandic_search(self, query: str, limit: int = 10):
        """Perform search with Icelandic query"""
        self.print_header("FEATURE 5: Icelandic Search with Translation")

        self.print_step(f"Searching with Icelandic query: '{query}'")

        try:
            payload = {
                "query": query,
                "limit": limit,
                "min_score": 0.0
            }

            response = requests.post(
                f"{self.flask_base_url}/api/search/icelandic",
                json=payload
            )
            response.raise_for_status()
            results = response.json()

            translated_query = results.get('translated_query', query)
            if translated_query != query:
                self.print_info(f"Translated to English: '{translated_query}'")

            result_list = results.get('results', [])
            self.print_success(f"Found {len(result_list)} results")

            self._display_search_results(result_list, limit=5)

            return result_list
        except Exception as e:
            self.print_error(f"Icelandic search failed: {e}")
            return []

    # =========================================================================
    # FEATURE 6: Hybrid Search (Text + Metadata)
    # =========================================================================

    def hybrid_search(self, text_query: str, metadata: Dict[str, Any] = None, limit: int = 10):
        """Perform hybrid search combining text and metadata"""
        self.print_header("FEATURE 6: Hybrid Search (Text + Metadata)")

        self.print_step(f"Hybrid search with text: '{text_query}'")
        if metadata:
            self.print_info(f"Metadata filters: {metadata}")

        try:
            payload = {
                "text_query": text_query,
                "metadata": metadata or {},
                "weights": {
                    "text": 0.7,
                    "metadata": 0.3
                },
                "limit": limit
            }

            response = requests.post(
                f"{self.flask_base_url}/api/search/hybrid",
                json=payload
            )
            response.raise_for_status()
            results = response.json()

            result_list = results.get('results', [])
            self.print_success(f"Found {len(result_list)} results")

            self._display_search_results(result_list, limit=5)

            return result_list
        except Exception as e:
            self.print_error(f"Hybrid search failed: {e}")
            return []

    # =========================================================================
    # Helper Methods
    # =========================================================================

    def _display_search_results(self, results: List[Dict], limit: int = 5):
        """Display search results in a formatted table"""
        if not results:
            self.print_info("No results to display")
            return

        print(f"\n{Colors.BOLD}Top {min(len(results), limit)} Results:{Colors.END}\n")

        for i, result in enumerate(results[:limit], 1):
            score = result.get('score', 0)
            filename = result.get('filename', 'Unknown')
            description = result.get('description', 'No description')

            score_color = Colors.GREEN if score > 0.7 else Colors.YELLOW if score > 0.5 else Colors.RED

            print(f"  {Colors.BOLD}{i}. {filename}{Colors.END}")
            print(f"     Score: {score_color}{score:.4f}{Colors.END}")
            if description and description != 'No description':
                print(f"     Description: {description[:80]}...")
            print()

    # =========================================================================
    # Main Demo Flow
    # =========================================================================

    def run_full_demo(self):
        """Run the complete demonstration"""
        self.print_header("SAGA REYKJAVÍK - COMPREHENSIVE FEATURE DEMO")
        print(f"{Colors.BOLD}This demo will showcase all major features of the platform{Colors.END}\n")

        # 1. Health checks
        if not self.check_health():
            self.print_error("Services are not healthy. Please start both backend services.")
            return False

        input(f"\n{Colors.YELLOW}Press Enter to continue to statistics...{Colors.END}")

        # 2. Get statistics
        self.get_stats()

        # Ask if user wants to run indexing demo
        print(f"\n{Colors.YELLOW}The next demo will test indexing functionality.{Colors.END}")
        run_indexing = input(f"{Colors.YELLOW}Do you want to run the indexing demo? (y/n): {Colors.END}").lower() == 'y'

        if run_indexing:
            # Check if demo data exists
            if not self.demo_data_path.exists():
                self.print_error(f"Demo data path does not exist: {self.demo_data_path}")
                self.print_info("Creating demo data folder...")
                self.demo_data_path.mkdir(parents=True, exist_ok=True)
                self.print_info(f"Please add some images to {self.demo_data_path} and run the demo again")
            else:
                # 3. Start indexing
                job_id = self.start_indexing(str(self.demo_data_path.absolute()))

                if job_id:
                    # 4. Monitor indexing
                    self.monitor_indexing(job_id, max_wait=120)

                    # 5. List all jobs
                    input(f"\n{Colors.YELLOW}Press Enter to list all jobs...{Colors.END}")
                    self.list_jobs()

        # 6. Semantic search demo
        input(f"\n{Colors.YELLOW}Press Enter to demo semantic search...{Colors.END}")
        self.semantic_search("historical building", limit=10)

        # 7. Icelandic search demo
        input(f"\n{Colors.YELLOW}Press Enter to demo Icelandic search...{Colors.END}")
        self.icelandic_search("gamall bær", limit=10)  # "old town" in Icelandic

        # 8. Hybrid search demo
        input(f"\n{Colors.YELLOW}Press Enter to demo hybrid search...{Colors.END}")
        self.hybrid_search("landscape", metadata={"folder": "iceland"}, limit=10)

        # Final statistics
        input(f"\n{Colors.YELLOW}Press Enter to view final statistics...{Colors.END}")
        self.get_stats()

        self.print_header("DEMO COMPLETE")
        self.print_success("All features demonstrated successfully!")

        return True


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="SAGA Reykjavík - Comprehensive Feature Demo"
    )
    parser.add_argument(
        '--demo-data-path',
        default='./demo_images',
        help='Path to demo images folder (default: ./demo_images)'
    )

    args = parser.parse_args()

    demo = SAGADemo(demo_data_path=args.demo_data_path)

    try:
        success = demo.run_full_demo()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Demo interrupted by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n{Colors.RED}Demo failed with error: {e}{Colors.END}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
