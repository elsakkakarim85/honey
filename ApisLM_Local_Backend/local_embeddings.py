from sentence_transformers import SentenceTransformer
from langchain_core.embeddings import Embeddings
from typing import List

class LocalBGEEmbeddings(Embeddings):
    """Zero-Cost local embeddings using BAAI/bge-m3 on CPU."""
    def __init__(self, model_name: str = "BAAI/bge-m3"):
        print(f"Loading local embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name, device="cpu")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings = self.model.encode(texts, normalize_embeddings=True)
        return embeddings.tolist()

    def embed_query(self, text: str) -> List[float]:
        embedding = self.model.encode(text, normalize_embeddings=True)
        return embedding.tolist()

if __name__ == "__main__":
    embedder = LocalBGEEmbeddings()
    print("Testing local embedder...", len(embedder.embed_query("Beekeeping test")))
