from functools import lru_cache

from openai import OpenAI

from app import config


class OpenAILLM:
    def __init__(self, model_name: str, max_tokens: int = 400):
        if not config.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY is not set. Please configure your OpenAI credentials.")
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.model_name = model_name
        self.max_tokens = max_tokens

    def generate(self, prompt: str, temperature: float = 0.2) -> str:
        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=self.max_tokens,
        )
        return (completion.choices[0].message.content or "").strip()


@lru_cache(maxsize=1)
def get_llm() -> OpenAILLM:
    return OpenAILLM(model_name=config.OPENAI_MODEL, max_tokens=config.MAX_COMPLETION_TOKENS)
