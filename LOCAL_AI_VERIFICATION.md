# Local AI Verification

## What Runs Fully On-Device

| Function | Runs locally? | Details |
|---|---|---|
| Document parsing (`.txt`/`.pdf`) | ✅ Yes | `pypdf`, standard library — no network call |
| Text chunking | ✅ Yes | Pure Python, in-process |
| Embedding generation | ✅ Yes | `all-MiniLM-L6-v2` runs on local CPU |
| Vector similarity search | ✅ Yes | FAISS, in-process, no external database |
| LLM answer generation | ✅ Yes | Qwen2.5-1.5B-Instruct (Q4_K_M GGUF), via `llama.cpp`, local CPU |
| Web UI rendering | ✅ Yes | Gradio server bound to `127.0.0.1` (localhost) only |

**Every step in the core question-answering loop — from document upload to final answer — runs entirely on the user's machine.**

## What Requires Internet

Internet access is required **only once, ahead of time**, for setup — not during actual use:

1. Installing Python dependencies (`pip install -r requirements.txt`)
2. Downloading the LLM weights from Hugging Face Hub (`hf download ...`)
3. Downloading the embedding model weights (auto-fetched once by `sentence-transformers` on first run, then cached locally)

Once these one-time downloads are complete, `python app.py ingest`, `python app.py chat`, and `python web_app.py` all function with **no internet connection required** — this can be verified by disabling networking after setup and confirming the application still runs (informally verified during development; see `EVALUATION.md` for testing methodology).

## Does Any User Data Leave the Device?

**No.** Specifically:

- Document content uploaded or placed in `data/` is never transmitted over a network.
- Questions typed into the CLI or web UI are never transmitted over a network.
- Generated answers are never transmitted over a network.
- The web UI is bound to `127.0.0.1` (localhost) — not `0.0.0.0` — meaning it is not reachable from other devices on the same network, let alone the internet.
- `demo.launch(share=True)` (Gradio's public-tunnel option) is deliberately **not used** in this project, since it would route traffic through Gradio's servers and break the local-only guarantee. See `ARCHITECTURE.md` for this design decision.

## How to Independently Verify This

1. Complete setup (Step 1–3 in `README.md`) while connected to the internet.
2. Disconnect from the internet (disable Wi-Fi/Ethernet).
3. Run `python app.py ingest` and `python app.py chat` (or `python web_app.py`) — both should function normally, with no errors related to network connectivity.
