# Attribution

Vault-Mind builds on the following open-source models, libraries, and tools. We're grateful to their authors and maintainers.

## Pretrained Models

| Model | Author/Org | License | Used for |
|---|---|---|---|
| [Qwen2.5-1.5B-Instruct (GGUF)](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF) | Alibaba Cloud (Qwen Team) | Apache 2.0 | Local LLM generation |
| [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) | Sentence-Transformers / UKPLab | Apache 2.0 | Local text embeddings |

## Runtimes and Libraries

| Library | Purpose |
|---|---|
| [llama.cpp](https://github.com/ggml-org/llama.cpp) / [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) | Local LLM inference runtime (GGUF) |
| [sentence-transformers](https://www.sbert.net/) | Embedding model loading and inference |
| [FAISS](https://github.com/facebookresearch/faiss) (Meta AI) | Local vector similarity search |
| [pypdf](https://pypdf.readthedocs.io/) | PDF text extraction |
| [Gradio](https://www.gradio.app/) | Local web UI framework |
| [huggingface_hub](https://github.com/huggingface/huggingface_hub) | Model weight downloading |

## Datasets

No custom or third-party datasets were used. All testing was performed against original workshop-manual PDFs used for demonstration purposes; no model training or fine-tuning was performed on any dataset in this submission.

## APIs

None. No external/cloud APIs are called by the core application at runtime (see `PRIVACY_AND_SAFETY.md` and `ARCHITECTURE.md`).

## License Compliance

All libraries and models listed above are used under their respective open-source licenses (Apache 2.0 for all listed components at time of writing). This project itself is released under the MIT License — see [LICENSE](./LICENSE).
