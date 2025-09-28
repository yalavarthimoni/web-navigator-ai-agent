# backend/llm_interface.py
import os
import json
from dotenv import load_dotenv

load_dotenv()

LLM_MODEL = os.getenv("LLM_MODEL")  # path to gpt4all model if present

# Try to import GPT4All; if unavailable we will fall back to algorithmic selection
USE_GPT4ALL = False
try:
    if LLM_MODEL:
        from gpt4all import GPT4All
        model = GPT4All(model=LLM_MODEL)
        USE_GPT4ALL = True
except Exception:
    # GPT4All isn't available — we'll rely on fallback method
    USE_GPT4ALL = False

def generate_response(prompt: str, max_tokens: int = 512) -> str:
    """
    If GPT4All is available, call it and return string output.
    Otherwise raise RuntimeError so caller can fall back to deterministic selection.
    """
    if not USE_GPT4ALL:
        raise RuntimeError("Local LLM (gpt4all) not available")
    # call gpt4all
    out = model.generate(prompt, max_tokens=max_tokens)
    # ensure str
    if isinstance(out, (list, tuple)):
        out = " ".join(out)
    return str(out)
