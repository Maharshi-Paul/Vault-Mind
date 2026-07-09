"""
Simple local vector store using FAISS (flat index — fine for hackathon-scale doc counts).
Stores embeddings + their source text chunks, saved to disk under vector_store/.
"""

import os
import pickle
import numpy as np
import faiss


class VectorStore:
    def __init__(self, dim: int, store_dir: str = "vector_store"):
        self.dim = dim
        self.store_dir = store_dir
        self.index = faiss.IndexFlatL2(dim)
        self.chunks: list[str] = []
        self.metadata: list[dict] = []
        os.makedirs(store_dir, exist_ok=True)

    def add(self, embeddings: np.ndarray, chunks: list[str], metadata: list[dict] = None):
        self.index.add(embeddings.astype("float32"))
        self.chunks.extend(chunks)
        self.metadata.extend(metadata or [{} for _ in chunks])

    def search(self, query_embedding: np.ndarray, k: int = 4) -> list[dict]:
        query_embedding = query_embedding.astype("float32").reshape(1, -1)
        distances, indices = self.index.search(query_embedding, k)
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue
            results.append({
                "chunk": self.chunks[idx],
                "metadata": self.metadata[idx],
                "distance": float(dist),
            })
        return results

    def save(self, name: str = "index"):
        faiss.write_index(self.index, os.path.join(self.store_dir, f"{name}.index"))
        with open(os.path.join(self.store_dir, f"{name}.pkl"), "wb") as f:
            pickle.dump({"chunks": self.chunks, "metadata": self.metadata}, f)

    def load(self, name: str = "index"):
        self.index = faiss.read_index(os.path.join(self.store_dir, f"{name}.index"))
        with open(os.path.join(self.store_dir, f"{name}.pkl"), "rb") as f:
            data = pickle.load(f)
            self.chunks = data["chunks"]
            self.metadata = data["metadata"]
