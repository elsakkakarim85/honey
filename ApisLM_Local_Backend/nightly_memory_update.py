import os
import json
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from sentence_transformers import SentenceTransformer

LOG_FILE = "rlhf_corrections_log.jsonl"
QDRANT_PATH = "local_qdrant_db"
COLLECTION_NAME = "apis_knowledge"

def run_nightly_memory_update():
    print("Initializing Nightly Self-Healing Memory Update...")
    if not os.path.exists(LOG_FILE):
        print("No new RLHF corrections found. Sleeping...")
        return
        
    print("Loading local BGE-M3 embedding model...")
    embedder = SentenceTransformer("BAAI/bge-m3")
    
    print("Connecting to local Qdrant database...")
    client = QdrantClient(path=QDRANT_PATH)
    
    corrections = []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                corrections.append(json.loads(line))
                
    if not corrections:
        return
        
    print(f"Processing {len(corrections)} expert corrections...")
    points = []
    
    # We use a high base ID for corrections so they don't collide with base dataset easily
    base_id = 900000 
    
    for idx, entry in enumerate(corrections):
        # The new ground truth to memorize
        correction_text = f"EXPERT KNOWLEDGE OVERRIDE:\nQ: {entry['prompt']}\nA: {entry['chosen']}"
        
        # Generate Vector
        vector = embedder.encode(correction_text).tolist()
        
        points.append(PointStruct(
            id=base_id + idx,
            vector=vector,
            payload={
                "text": correction_text,
                "source": "RLHF_EXPERT_CORRECTION",
                "priority": "HIGH" # Instruct CRAG to favor this heavily
            }
        ))
        
    print("Upserting corrected vectors into Qdrant...")
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )
    
    print("Executing Vector Eviction Policy...")
    # Prevent memory leaks by deleting RLHF corrections older than 180 days
    # In production, this uses Qdrant's Filter API on a timestamp payload
    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector={"filter": {"must": [{"key": "age_days", "range": {"gte": 180}}]}}
    )
    
    print("Nightly Update Complete. CRAG pipeline will now retrieve these corrections!")
    
    # Archive the log so we don't re-embed tomorrow
    os.rename(LOG_FILE, f"{LOG_FILE}.archived")

if __name__ == "__main__":
    run_nightly_memory_update()
