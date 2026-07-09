"""
Local embedding model wrapper using sentence-transformers (all-MiniLM-L6-v2).
Runs fully offline once the model is downloaded/cached.
"""

from sentence_transformers import SentenceTransformer
import numpy as np


class LocalEmbedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: list[str]) -> np.ndarray:
        """Returns an (N, D) numpy array of embeddings for a list of texts."""
        return self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)

    def embed_one(self, text: str) -> np.ndarray:
        return self.embed([text])[0]


if __name__ == "__main__":
    embedder = LocalEmbedder()
    vec = embedder.embed_one("This is a test sentence.")
    print("Embedding shape:", vec.shape)
