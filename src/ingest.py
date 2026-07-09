"""
Ingestion pipeline: reads documents from data/, chunks them, embeds them,
and stores them in the local vector store.

Supports .txt and .pdf files. Extend as needed.
"""

import os
from pypdf import PdfReader
from tqdm import tqdm

from embed import LocalEmbedder
from vector_store import VectorStore


def read_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def read_pdf(path: str) -> str:
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Simple word-based sliding-window chunking."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        if chunk.strip():
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def load_documents(data_dir: str = "data") -> list[tuple[str, str]]:
    """Returns list of (filename, full_text)."""
    docs = []
    for fname in os.listdir(data_dir):
        path = os.path.join(data_dir, fname)
        if fname.lower().endswith(".txt"):
            docs.append((fname, read_txt(path)))
        elif fname.lower().endswith(".pdf"):
            docs.append((fname, read_pdf(path)))
    return docs


def build_index(data_dir: str = "data", store_dir: str = "vector_store"):
    embedder = LocalEmbedder()
    documents = load_documents(data_dir)

    if not documents:
        print(f"No .txt or .pdf files found in {data_dir}/. Add some documents first.")
        return

    all_chunks = []
    all_metadata = []
    for fname, text in documents:
        chunks = chunk_text(text)
        all_chunks.extend(chunks)
        all_metadata.extend([{"source": fname} for _ in chunks])

    print(f"Embedding {len(all_chunks)} chunks from {len(documents)} document(s)...")
    embeddings = embedder.embed(all_chunks)

    store = VectorStore(dim=embeddings.shape[1], store_dir=store_dir)
    store.add(embeddings, all_chunks, all_metadata)
    store.save()
    print(f"Index built and saved to {store_dir}/")


if __name__ == "__main__":
    build_index()
