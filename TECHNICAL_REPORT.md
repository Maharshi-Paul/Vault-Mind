# Technical Report

## Model and Runtime

| Component | Detail |
|---|---|
| LLM | Qwen2.5-1.5B-Instruct |
| LLM format | GGUF |
| LLM runtime | `llama.cpp` (via `llama-cpp-python`) |
| Embedding model | `all-MiniLM-L6-v2` (via `sentence-transformers`) |
| Vector index | FAISS `IndexFlatL2` (exact search) |

## Quantization / Optimization Techniques

- **Quantization:** Q4_K_M (4-bit, mixed-precision GGUF quantization). Chosen over more aggressive options (e.g. Q4_0) to preserve answer quality on reasoning-heavy queries — see `EVALUATION.md` for examples of the reasoning tasks this needed to handle correctly.
- **Thread tuning:** `n_threads` increased from a default of 4 to 8, matching the test machine's physical core count.
- **Context/response tuning:** `max_tokens` capped at 220 (down from a default of 512) to avoid unnecessarily long generations.
- **Retrieval tuning:** `top_k` reduced from 4 to 3, and chunk size reduced from 500 to 300 words (30-word overlap) — this reduced redundant/overlapping context passed to the LLM, which was a major latency contributor when multiple retrieved chunks came from the same source document.

## Model Size

| Stage | Size |
|---|---|
| Base model (FP16) | ~3 GB (upstream, not deployed) |
| Deployed model (Q4_K_M GGUF) | **1.04 GB** (1,117,320,736 bytes, measured) |
| Embedding model (`all-MiniLM-L6-v2`) | ~90 MB |

## Inference Latency

Measured on the test device described below, using real multi-page PDF documents (workshop manuals with mixed text and diagrams).

| Stage | Before tuning | After tuning |
|---|---|---|
| Retrieval (FAISS search) | ~0.02–0.05s | ~0.02–0.05s (unchanged, already fast) |
| Generation | ~40s | **~12–17s** |

**~60–70% reduction in generation latency** from the tuning changes listed above, with no observed loss in answer quality on the same test question set (see `EVALUATION.md`).

## CPU / GPU / NPU Usage

- **CPU-only.** No GPU or NPU is used or required; `llama.cpp` runs entirely on CPU threads.
- Both the embedding model and the LLM run on CPU. This was a deliberate choice to keep the project runnable on standard consumer laptops without dedicated AI hardware, per the hackathon's "no special hardware required" guidance.

## Peak Memory Usage

Not formally profiled with a memory profiler under the time constraints of this hackathon. Rough estimate based on model sizes loaded into memory:
- Quantized LLM (~1.04 GB) + embedding model (~90 MB) + FAISS index (small, proportional to corpus size — under a few MB at tested document counts) + Python/runtime overhead.
- Informally, the application ran comfortably alongside a browser and IDE on an 8-core / consumer-RAM laptop with no observed swapping or slowdown outside of LLM generation time itself.
- **Noted as a gap:** precise peak RSS measurement (e.g. via `psutil` or Windows Task Manager sampling during generation) is listed as future work.

## Tested Device Specifications

| Spec | Value |
|---|---|
| OS | Windows |
| CPU | 8 physical cores |
| GPU | None used (CPU-only inference) |
| Python version | 3.14 |

## Known Gaps in This Report

- No formal peak-memory profiling (see above)
- Only tested on one physical device configuration (8-core Windows laptop) — behavior on lower core-count or ARM devices (e.g. Raspberry Pi, as mentioned in the hackathon resource guide) has not been verified
- Latency figures are from a single test machine and document set; not averaged across multiple runs or statistically validated
