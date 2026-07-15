# Privacy and Safety

## Data Handling

- **Documents you upload/place in `data/` are never transmitted anywhere.** All parsing, chunking, embedding, indexing, and generation happen in-process on your machine.
- **No telemetry, analytics, or usage tracking** is implemented anywhere in this project.
- **The web UI (`web_app.py`) is bound to `127.0.0.1` (localhost) only** — it is not exposed to your network or the internet. No one other than the local user can access it, and no request from it ever leaves the machine.
- **Chat history is not persisted to disk.** Conversations exist only in memory for the current session (CLI process or browser tab) and are lost when the session ends. This is a deliberate design choice, not an oversight — see `README.md` Known Limitations.

## Permissions Required

- **Filesystem read access** to the `data/` directory (to ingest documents) and `models/` directory (to load the LLM).
- **Filesystem write access** to `vector_store/` (to save the FAISS index) and, in the web UI, to `data/` (to save uploaded files).
- **Network access is required only once**, during setup, to download:
  - Python dependencies (`pip install`)
  - The LLM weights (via Hugging Face Hub)
  - The embedding model weights (auto-downloaded by `sentence-transformers` on first run)
- **No network access is required or used during actual ingestion or chat/query operations.**

## Storage

- Uploaded/ingested documents are copied into the local `data/` folder.
- Embeddings and the FAISS index are saved locally to `vector_store/`.
- Both directories are excluded from version control (`.gitignore`) so a user's actual document content is never accidentally committed to a public repository.

## Limitations

- This project has not undergone formal security review or penetration testing — it is a hackathon submission, not production-hardened software.
- The local web UI has no authentication. This is acceptable given it is bound to `127.0.0.1` only, but would need addressing before any multi-user or network-exposed deployment.
- Document content is not encrypted at rest in `data/` or `vector_store/` — it is stored as plain files/index data on the local disk, protected only by the operating system's normal file permissions.

## Potential Risks

- **Sensitive document exposure if misconfigured:** if a user were to manually change the Gradio launch call to `share=True` or expose the port publicly, document content could be transmitted through Gradio's tunnel infrastructure or become accessible to others on the network. The project is configured explicitly to avoid this by default (see `ARCHITECTURE.md`).
- **No input sanitization beyond standard library parsing** (`pypdf` for PDFs) — malformed or adversarial PDF files are not specifically hardened against, consistent with typical hackathon-scope security posture.
