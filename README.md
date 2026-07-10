# Vault-Mind

A fully offline AI assistant that answers questions over your own documents — local LLM + local embeddings, zero cloud dependency for the core AI.

Built for **OSDHack 2026** (theme: On-Device AI).

## How it works

1. Drop documents (`.txt` / `.pdf`) into `data/`
2. `python app.py ingest` — chunks and embeds them locally using `all-MiniLM-L6-v2`, stores vectors in a local FAISS index
3. `python app.py chat` — ask questions; relevant chunks are retrieved locally and answered by a quantized local LLM (Qwen2.5, via `llama.cpp`)

No cloud API calls for the core AI functionality — everything runs on your machine.

## Setup

### 1. Install dependencies
```bash
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Download a local LLM (GGUF format)
Download a quantized model, e.g. `qwen2.5-1.5b-instruct-q4_k_m.gguf`, from Hugging Face and place it in `models/`.

Update `MODEL_PATH` in `app.py` if you use a different model or filename.

### 3. Add your documents
Place `.txt` or `.pdf` files into `data/`.

### 4. Build the index
```bash
python app.py ingest
```

### 5. Chat
```bash
python app.py chat
```

## Project Structure

```
vault-mind/
├── src/
│   ├── llm.py          # local LLM wrapper (llama.cpp)
│   ├── embed.py         # local embedding model wrapper
│   ├── ingest.py         # document chunking + embedding pipeline
│   ├── vector_store.py   # local FAISS vector store
│   └── rag.py             # retrieval + generation pipeline
├── data/                   # your documents (not tracked in git)
├── models/                 # downloaded GGUF model files (not tracked in git)
├── vector_store/            # saved index (not tracked in git)
├── app.py                    # CLI entry point
└── requirements.txt
```

## Roadmap / Hackathon Progress

- [x] Day 1: Project setup, local LLM + embedding pipeline scaffolded
- [x] Day 2: Document ingestion + local vector store
- [x] Day 3: End-to-end RAG query pipeline
- [ ] Day 4: Quantization + performance benchmarking
- [ ] Day 5: README polish, demo prep, optional cloud sync feature

## Performance (to be filled in after benchmarking)

- **Target hardware:** Standard consumer laptop (CPU-only)
- **Base model size:** TBD
- **Quantized model size:** TBD
- **Tokens/sec:** TBD
- **Retrieval latency:** TBD

## License

MIT
