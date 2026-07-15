# Changelog

All notable changes to Vault-Mind are documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Planned
- LoRA fine-tuning for domain-specific tone/accuracy
- Semantic/structure-aware chunking
- Additional document format support (`.docx`, `.md`)

## [0.3.0] — 2026-07-14

### Added
- Local Gradio web UI (`web_app.py`) as an alternative to the CLI
- Multi-file upload support in the web UI
- Screenshots (CLI + web UI) added to README
- Project banner/poster image

### Changed
- Hid default Gradio branding footer for a cleaner demo UI
- Disabled API docs endpoint (`show_api=False`) since this is a local-only single-user tool

## [0.2.0] — 2026-07-13

### Added
- Tested end-to-end RAG pipeline against real-world documents (multi-page workshop manuals with mixed text and diagrams)
- Verified indirect-reasoning question handling and grounded refusal behavior (no hallucination on out-of-scope questions)

### Changed
- **Performance tuning:** reduced generation latency from ~40s to ~12–17s by:
  - Increasing `n_threads` from 4 → 8 (matching available CPU cores)
  - Reducing `max_tokens` from 512 → 220
  - Reducing retrieval `top_k` from 4 → 3
  - Reducing chunk size from 500 → 300 words

### Fixed
- Windows `llama-cpp-python` build failure — switched to prebuilt CPU wheel install to avoid requiring C++ build tools

## [0.1.0] — 2026-07-10

### Added
- Initial project scaffold: local LLM wrapper (`llama.cpp`), local embedding wrapper (`sentence-transformers`), local FAISS vector store
- Document ingestion pipeline (chunking + embedding for `.txt` / `.pdf`)
- RAG query pipeline with source citation
- CLI entry point (`app.py`) with `ingest` and `chat` commands
- MIT License
- Initial README

[Unreleased]: https://github.com/Maharshi-Paul/Vault-Mind/compare/main...HEAD
