# Evaluation

## Method

Vault-Mind was evaluated qualitatively against real-world multi-page PDF documents (workshop manuals: carpentry, fitting, and sheet metal shop guides, containing mixed prose, step-by-step procedures, and diagrams). Questions were designed to test four distinct capabilities, rather than relying on a single benchmark metric — appropriate for a RAG system where "correctness" depends on grounding in retrieved context, not just fluency.

No formal automated benchmark (e.g. exact-match QA dataset) was used, given hackathon time constraints. This is noted as a limitation below.

## Test Categories and Results

### 1. Direct factual recall
**Question:** *"What is the difference between soft wood and hard wood?"*
**Result:** ✅ Correct — accurately summarized both classifications with correct supporting detail, citing the source PDF.

### 2. Indirect reasoning (question doesn't use the document's own terminology)
**Question:** *"If I wanted a wood that resists bending forces well, which type should I pick and why?"*
**Result:** ✅ Correct — correctly mapped "resists bending forces" → hard wood, without the question ever using the word "hard wood," and explained why using document content.

### 3. Multi-hop / cross-referencing (requires combining information from different parts of a document, or across multiple documents)
**Question:** *"Differentiate between various workshops"* (with carpentry, fitting, and sheet metal shop PDFs all indexed together)
**Result:** ✅ Correct — produced a structured comparison pulling distinct facts from all three source PDFs, with correct per-document source citations.

### 4. Grounded refusal (question about something not present in the documents)
**Questions:**
- *"What safety certifications are required before using the carpenters bench vice?"*
- *"How much does a metal jack plane cost?"*

**Result:** ✅ Correct — in both cases, the model explicitly stated the information was not present in the provided context, rather than fabricating an answer. This is considered the most important result: it demonstrates the system is grounded in retrieved content rather than relying on the LLM's parametric knowledge or hallucinating plausible-sounding answers.

## Baseline Comparison

No comparison against a cloud-based baseline (e.g. GPT-4 with the same documents) was performed, given the project's explicit goal is local-only operation — a cloud comparison was considered out of scope for this submission's evaluation goals. This is noted as a limitation.

An informal internal baseline was used instead: generation latency and answer quality were compared **before and after** local optimization tuning (see `TECHNICAL_REPORT.md`), on the same fixed set of test questions, to validate that speed improvements did not come at the cost of correctness.

## Known Failure Cases / Limitations

- **Redundant source citations:** in early testing, multiple retrieved chunks sometimes originated from the same source document with overlapping content, inflating the effective context size and generation latency before `top_k` and chunk-size tuning. Partially mitigated by the tuning described in `TECHNICAL_REPORT.md`; not fully solved (no explicit deduplication logic implemented on retrieved chunks).
- **No automated regression testing:** correctness was verified manually against a small, fixed question set (documented above), not a large or automated benchmark. A regression could be introduced by future changes without being caught automatically.
- **Latency is noticeable, not instant:** ~12–17s per answer is usable but not conversational-speed. Acceptable for a hackathon demo; a production tool might need further optimization or a smaller model.
- **Chunking is naive:** word-count-based chunking can split content mid-sentence or mid-concept, which may occasionally reduce retrieval precision on documents with irregular structure. Not observed to cause incorrect answers in testing, but is a known theoretical weakness.
- **Single-document-type assumption in tests:** all real-document testing was done on similarly-structured technical/procedural PDFs (workshop manuals). Behavior on very different document types (e.g. dense academic papers, tables-heavy spreadsheets-as-PDF) has not been verified.
