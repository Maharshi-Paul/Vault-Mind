"""
Local LLM wrapper using llama.cpp (via llama-cpp-python).
Loads a quantized GGUF model and exposes a simple generate() method.
"""

from llama_cpp import Llama


class LocalLLM:
    def __init__(self, model_path: str, n_ctx: int = 4096, n_threads: int = 8, verbose: bool = False):
        """
        model_path: path to a .gguf model file (e.g. models/qwen2.5-1.5b-instruct-q4_k_m.gguf)
        """
        self.llm = Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            n_threads=n_threads,
            verbose=verbose,
        )

    def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.3) -> str:
        output = self.llm(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            stop=["</s>", "<|im_end|>"],
        )
        return output["choices"][0]["text"].strip()

    def chat(self, messages: list[dict], max_tokens: int = 512, temperature: float = 0.3) -> str:
        """messages: [{"role": "system"/"user"/"assistant", "content": "..."}]"""
        output = self.llm.create_chat_completion(
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return output["choices"][0]["message"]["content"].strip()


if __name__ == "__main__":
    # Quick manual test — update the path to your downloaded GGUF model
    llm = LocalLLM(model_path="models/qwen2.5-1.5b-instruct-q4_k_m.gguf")
    reply = llm.chat([{"role": "user", "content": "Say hello in one sentence."}])
    print(reply)
