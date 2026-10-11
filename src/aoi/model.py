"""Optional Hugging Face Transformers backend.

Loading a model downloads weights on first use unless they are cached.
The default 3B model can require substantial RAM and/or GPU memory.
"""
from __future__ import annotations


class LocalQwenGenerator:
    def __init__(self, model_name: str, max_new_tokens: int = 180, temperature: float = 0.7):
        self.model_name = model_name
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature
        self._tokenizer = None
        self._model = None

    def _load(self) -> None:
        if self._model is not None:
            return
        try:
            import torch
            from transformers import AutoTokenizer, AutoModelForCausalLM
        except ImportError as exc:
            raise RuntimeError("Install model dependencies: pip install -e '.[model]'") from exc
        self._tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self._model = AutoModelForCausalLM.from_pretrained(
            self.model_name, torch_dtype="auto", device_map="auto"
        )
        self._model.eval()

    def generate(self, messages: list[dict[str, str]]) -> str:
        self._load()
        import torch

        tokenizer = self._tokenizer
        model = self._model
        prompt = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        batch = tokenizer(prompt, return_tensors="pt")
        # Using model.device works for the typical single-device path. Complex
        # offloading setups may need changes based on local hardware.
        inputs = {key: value.to(model.device) for key, value in batch.items()}
        generation = {"max_new_tokens": self.max_new_tokens,
                      "pad_token_id": tokenizer.eos_token_id}
        if self.temperature > 0:
            generation.update(do_sample=True, temperature=self.temperature)
        else:
            generation.update(do_sample=False)
        with torch.inference_mode():
            output_ids = model.generate(**inputs, **generation)
        response_ids = output_ids[0][inputs["input_ids"].shape[-1]:]
        text = tokenizer.decode(response_ids, skip_special_tokens=True).strip()
        if not text:
            raise RuntimeError("The model produced an empty reply; no exchange was saved.")
        return text
