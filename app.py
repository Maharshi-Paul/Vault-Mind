"""
Vault-Mind CLI entry point.

Usage:
    python app.py ingest          # build the vector index from data/
    python app.py chat            # start an interactive Q&A session
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

MODEL_PATH = "models/qwen2.5-1.5b-instruct-q4_k_m.gguf"  # update after downloading


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    command = sys.argv[1]

    if command == "ingest":
        from ingest import build_index
        build_index()

    elif command == "chat":
        from rag import RAGPipeline
        rag = RAGPipeline(model_path=MODEL_PATH)
        print("Vault-Mind ready. Type 'exit' to quit.\n")
        while True:
            q = input("You: ")
            if q.lower() in ("exit", "quit"):
                break
            result = rag.query(q)
            print(f"\nVault-Mind: {result['answer']}")
            print(f"(sources: {result['sources']})\n")

    else:
        print(f"Unknown command: {command}")
        print(__doc__)


if __name__ == "__main__":
    main()
