from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, ScalarQuantization, ScalarQuantizationConfig, ScalarType

def init_local_qdrant():
    print("Initializing Zero-Cost Local Qdrant Database...")
    # Saves data directly to local disk without needing a Docker container
    client = QdrantClient(path="./qdrant_storage")
    
    collection_name = "apis_local_knowledge"
    
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=1024, # BGE-M3 dimension size
                distance=Distance.COSINE
            ),
            # 8-bit Scalar Quantization (SQ) to compress memory usage on local hardware
            quantization_config=ScalarQuantization(
                scalar=ScalarQuantizationConfig(
                    type=ScalarType.INT8,
                    quantile=0.99,
                    always_ram=True,
                )
            )
        )
        print(f"Collection '{collection_name}' created with INT8 Quantization.")
    else:
        print(f"Collection '{collection_name}' already exists.")
        
    return client

if __name__ == "__main__":
    init_local_qdrant()
