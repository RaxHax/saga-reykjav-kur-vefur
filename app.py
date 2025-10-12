from flask import Flask, render_template, request, jsonify, send_file
import torch
import open_clip
from PIL import Image
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from pathlib import Path
import os
import threading
import time

app = Flask(__name__)

# Global variables
device = "cuda" if torch.cuda.is_available() else "cpu"
model = None
preprocess = None
tokenizer = None
client = None
indexing_status = {
    "is_indexing": False, 
    "progress": 0, 
    "total": 0, 
    "message": "",
    "start_time": None,
    "estimated_time": None
}

def initialize_models():
    """Initialize CLIP model and Qdrant client"""
    global model, preprocess, tokenizer, client
    
    print(f"🚀 Initializing models on {device}...")
    
    # Load CLIP
    model, _, preprocess = open_clip.create_model_and_transforms(
        'ViT-B-32', 
        pretrained='laion2b_s34b_b79k'
    )
    model = model.to(device)
    model.eval()
    tokenizer = open_clip.get_tokenizer('ViT-B-32')
    
    # Initialize Qdrant
    client = QdrantClient(path="./qdrant_storage")
    
    # Create collection if doesn't exist
    try:
        client.create_collection(
            collection_name="image_search",
            vectors_config=VectorParams(size=512, distance=Distance.COSINE),
        )
        print("✅ Created new collection")
    except Exception as e:
        print(f"📁 Using existing collection")
    
    print("✅ Models initialized successfully!")

def embed_image(image_path):
    """Generate embedding for an image"""
    try:
        image = Image.open(image_path).convert('RGB')
        image_input = preprocess(image).unsqueeze(0).to(device)
        
        with torch.no_grad():
            image_features = model.encode_image(image_input)
            image_features /= image_features.norm(dim=-1, keepdim=True)
        
        return image_features.cpu().numpy()[0]
    except Exception as e:
        print(f"❌ Error processing {image_path}: {e}")
        return None

def read_description(txt_path):
    """Read description from .txt file"""
    try:
        with open(txt_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            return content if content else "No description"
    except:
        return "No description"

def estimate_time_remaining(progress, total, start_time):
    """Estimate time remaining for indexing"""
    if progress == 0:
        return "Calculating..."
    
    elapsed = time.time() - start_time
    rate = progress / elapsed
    remaining = (total - progress) / rate
    
    if remaining < 60:
        return f"{int(remaining)}s remaining"
    elif remaining < 3600:
        return f"{int(remaining / 60)}m remaining"
    else:
        return f"{int(remaining / 3600)}h {int((remaining % 3600) / 60)}m remaining"

def index_images_background(image_folder):
    """Index images in background thread"""
    global indexing_status
    
    image_folder = Path(image_folder)
    
    # Find all image files
    image_files = (
        list(image_folder.glob("*.jpg")) + 
        list(image_folder.glob("*.jpeg")) + 
        list(image_folder.glob("*.png")) +
        list(image_folder.rglob("*.jpg")) +  # Recursive search
        list(image_folder.rglob("*.jpeg")) +
        list(image_folder.rglob("*.png"))
    )
    
    # Remove duplicates
    image_files = list(set(image_files))
    
    indexing_status["total"] = len(image_files)
    indexing_status["progress"] = 0
    indexing_status["start_time"] = time.time()
    indexing_status["message"] = f"Found {len(image_files)} images"
    
    print(f"📸 Starting to index {len(image_files)} images...")
    
    points = []
    batch_size = 100
    errors = 0
    
    for idx, image_file in enumerate(image_files):
        try:
            # Read description
            txt_file = image_file.with_suffix('.txt')
            description = read_description(txt_file)
            
            # Generate embedding
            embedding = embed_image(str(image_file))
            
            if embedding is None:
                errors += 1
                continue
            
            # Create point
            points.append(PointStruct(
                id=idx,
                vector=embedding.tolist(),
                payload={
                    "filename": image_file.name,
                    "path": str(image_file.absolute()),
                    "description": description,
                    "folder": str(image_file.parent)
                }
            ))
            
            # Batch upload
            if len(points) >= batch_size:
                client.upsert(collection_name="image_search", points=points)
                points = []
            
            # Update progress
            indexing_status["progress"] = idx + 1
            indexing_status["estimated_time"] = estimate_time_remaining(
                idx + 1, 
                len(image_files), 
                indexing_status["start_time"]
            )
            indexing_status["message"] = f"Processed {idx + 1}/{len(image_files)} images"
            
            # Log progress every 100 images
            if (idx + 1) % 100 == 0:
                print(f"📊 Progress: {idx + 1}/{len(image_files)} ({(idx+1)/len(image_files)*100:.1f}%)")
        
        except Exception as e:
            print(f"❌ Error with {image_file}: {e}")
            errors += 1
            continue
    
    # Upload remaining points
    if points:
        client.upsert(collection_name="image_search", points=points)
    
    # Finish
    indexing_status["is_indexing"] = False
    success_count = len(image_files) - errors
    indexing_status["message"] = f"✅ Completed! Indexed {success_count} images ({errors} errors)"
    
    print(f"✅ Indexing complete! {success_count}/{len(image_files)} images indexed successfully")

@app.route('/')
def home():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/index', methods=['POST'])
def start_indexing():
    """Start indexing images"""
    global indexing_status
    
    if indexing_status["is_indexing"]:
        return jsonify({"error": "Indexing already in progress"}), 400
    
    data = request.json
    image_folder = data.get('folder', './scraped_images')
    
    if not os.path.exists(image_folder):
        return jsonify({"error": f"Folder not found: {image_folder}"}), 404
    
    # Reset status
    indexing_status = {
        "is_indexing": True,
        "progress": 0,
        "total": 0,
        "message": "Starting indexing...",
        "start_time": None,
        "estimated_time": None
    }
    
    # Start background thread
    thread = threading.Thread(target=index_images_background, args=(image_folder,))
    thread.daemon = True
    thread.start()
    
    return jsonify({"message": "Indexing started", "status": indexing_status})

@app.route('/api/index/status', methods=['GET'])
def get_indexing_status():
    """Get current indexing status"""
    return jsonify(indexing_status)

@app.route('/api/search', methods=['POST'])
def search():
    """Search for images using semantic similarity"""
    data = request.json
    query = data.get('query', '')
    top_k = data.get('top_k', 12)
    
    if not query:
        return jsonify({"error": "Query is required"}), 400
    
    try:
        print(f"🔍 Searching for: '{query}'")
        
        # Encode text query
        text_input = tokenizer([query]).to(device)
        
        with torch.no_grad():
            text_features = model.encode_text(text_input)
            text_features /= text_features.norm(dim=-1, keepdim=True)
        
        # Search in Qdrant
        results = client.search(
            collection_name="image_search",
            query_vector=text_features.cpu().numpy()[0].tolist(),
            limit=top_k
        )
        
        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append({
                "score": float(result.score),
                "filename": result.payload['filename'],
                "path": result.payload['path'],
                "description": result.payload.get('description', 'No description'),
                "folder": result.payload.get('folder', '')
            })
        
        print(f"✅ Found {len(formatted_results)} results")
        
        return jsonify({
            "query": query,
            "results": formatted_results,
            "count": len(formatted_results)
        })
    
    except Exception as e:
        print(f"❌ Search error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get database statistics"""
    try:
        collection_info = client.get_collection("image_search")
        return jsonify({
            "total_images": collection_info.points_count,
            "device": device,
            "is_indexing": indexing_status["is_indexing"]
        })
    except Exception as e:
        return jsonify({
            "total_images": 0,
            "device": device,
            "is_indexing": False
        })

@app.route('/api/image/<path:filepath>')
def serve_image(filepath):
    """Serve image files"""
    try:
        if os.path.exists(filepath):
            return send_file(filepath)
        else:
            return jsonify({"error": "Image not found"}), 404
    except Exception as e:
        print(f"❌ Error serving image: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "device": device
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🖼️  Image Search System Starting...")
    print("="*60 + "\n")
    
    initialize_models()
    
    print("\n" + "="*60)
    print("✅ Server ready!")
    print("🌐 Open http://localhost:5000 in your browser")
    print("="*60 + "\n")
    
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)