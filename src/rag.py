"""
RAG pipeline: given a user question, retrieve relevant chunks from the local
vector store and generate an answer using the local LLM.
"""

import time

from embed import LocalEmbedder
from vector_store import VectorStore
from llm import LocalLLM


SYSTEM_PROMPT = (
    "You are Vault-Mind, an offline assistant that answers questions using only "
    "the provided context from the user's own documents. If the answer isn't in "
    "the context, say you don't know rather than guessing."
)


def build_prompt(question: str, context_chunks: list[str]) -> list[dict]:
    context = "\n\n---\n\n".join(context_chunks)
    user_content = f"Context:\n{context}\n\nQuestion: {question}"
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content},
    ]


class RAGPipeline:
    def __init__(self, model_path: str, store_dir: str = "vector_store", top_k: int = 3):
        self.embedder = LocalEmbedder()
        self.store = VectorStore(dim=384, store_dir=store_dir)  # 384 = MiniLM-L6 dim
        self.store.load()
        self.llm = LocalLLM(model_path=model_path)
        self.top_k = top_k

    def query(self, question: str, verbose: bool = True) -> dict:
        t0 = time.time()
        query_vec = self.embedder.embed_one(question)
        results = self.store.search(query_vec, k=self.top_k)
        context_chunks = [r["chunk"] for r in results]
        t1 = time.time()

        messages = build_prompt(question, context_chunks)
        answer = self.llm.chat(messages)
        t2 = time.time()

        if verbose:
            print(f"[retrieval: {t1 - t0:.2f}s] [generation: {t2 - t1:.2f}s]")

        return {
            "answer": answer,
            "sources": [r["metadata"].get("source") for r in results],
            "retrieval_time": t1 - t0,
            "generation_time": t2 - t1,
        }


if __name__ == "__main__":
    rag = RAGPipeline(model_path="models/qwen2.5-1.5b-instruct-q4_k_m.gguf")
    while True:
        q = input("\nAsk Vault-Mind (or 'exit'): ")
        if q.lower() == "exit":
            break
        result = rag.query(q)
        print(f"\nAnswer: {result['answer']}")
        print(f"Sources: {result['sources']}")
