"""
Vault-Mind local web UI (Gradio).

Runs entirely on your machine — the browser tab is just a local interface;
no data leaves your device. Same RAG pipeline as the CLI (app.py chat),
just with a friendlier interface for demos.

Usage:
    python web_app.py
Then open the local URL Gradio prints (usually http://127.0.0.1:7860).
"""

import os
import shutil
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import gradio as gr

from ingest import build_index
from rag import RAGPipeline

MODEL_PATH = "models/qwen2.5-1.5b-instruct-q4_k_m.gguf"
DATA_DIR = "data"

rag_pipeline = None  # lazy-loaded on first chat message


def get_pipeline():
    global rag_pipeline
    if rag_pipeline is None:
        rag_pipeline = RAGPipeline(model_path=MODEL_PATH)
    return rag_pipeline


def upload_and_ingest(files):
    if not files:
        return "No files selected."

    os.makedirs(DATA_DIR, exist_ok=True)
    for f in files:
        dest = os.path.join(DATA_DIR, os.path.basename(f.name))
        shutil.copy(f.name, dest)

    build_index(data_dir=DATA_DIR)

    global rag_pipeline
    rag_pipeline = None  # force reload so it picks up the new index

    return f"Indexed {len(files)} file(s). You can start asking questions below."


def respond(message, history):
    pipeline = get_pipeline()
    result = pipeline.query(message, verbose=False)

    sources = ", ".join(sorted(set(result["sources"]))) if result["sources"] else "none"
    timing = f"_(retrieval: {result['retrieval_time']:.2f}s · generation: {result['generation_time']:.2f}s · sources: {sources})_"

    answer = f"{result['answer']}\n\n{timing}"
    history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": answer},
    ]
    return history, ""


with gr.Blocks(title="Vault-Mind — Offline Document Assistant") as demo:
    gr.Markdown(
        """
        # 🔒 Vault-Mind
        **A fully offline AI assistant for your documents.**
        Everything below — embeddings, retrieval, and generation — runs locally on this machine. No document content leaves your device.
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 1. Add documents")
            file_upload = gr.File(
                label="Upload .txt / .pdf files",
                file_count="multiple",
                file_types=[".txt", ".pdf"],
            )
            ingest_btn = gr.Button("Build / Update Index", variant="primary")
            ingest_status = gr.Markdown("")

        with gr.Column(scale=2):
            gr.Markdown("### 2. Ask questions")
            chatbot = gr.Chatbot(height=420, label="Vault-Mind")
            msg = gr.Textbox(
                label="Your question",
                placeholder="Ask something about your documents...",
            )
            clear = gr.Button("Clear chat")

    ingest_btn.click(fn=upload_and_ingest, inputs=file_upload, outputs=ingest_status)
    msg.submit(fn=respond, inputs=[msg, chatbot], outputs=[chatbot, msg])
    clear.click(lambda: [], None, chatbot)

    gr.Markdown(
        """
        ---
        **On-device AI:** embeddings via `all-MiniLM-L6-v2`, retrieval via local FAISS,
        generation via quantized `Qwen2.5-1.5B-Instruct` (GGUF, Q4_K_M) running through `llama.cpp` — all on this machine.
        """
    )


if __name__ == "__main__":
    demo.launch()