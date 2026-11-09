"""Model backends. Real backend = local llama.cpp `llama-server` (OpenAI-compatible, loopback only)."""
import json, time, urllib.request
from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass
class Reply:
    text: str
    prompt_tokens: int
    completion_tokens: int
    seconds: float
    finish_reason: str = ""


class LlamaServerBackend:
    is_mock = False

    def __init__(self, base_url="http://127.0.0.1:8080", model_label="local", timeout=900):
        host = urlparse(base_url).hostname
        if host not in ("127.0.0.1", "localhost", "::1"):
            raise ValueError(f"Refusing non-loopback endpoint {base_url!r}: P1 forbids cloud/remote inference.")
        self.url = base_url.rstrip("/") + "/v1/chat/completions"
        self.model_label, self.timeout = model_label, timeout

    def chat(self, messages, temperature, top_p, top_k, max_tokens, seed) -> Reply:
        body = {"model": self.model_label, "messages": messages, "temperature": temperature, "top_p": top_p,
                "top_k": top_k, "max_tokens": max_tokens, "seed": seed, "stream": False}
        req = urllib.request.Request(self.url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
        t0 = time.time()
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            d = json.loads(r.read().decode())
        ch = d["choices"][0]
        u = d.get("usage", {})
        return Reply(ch["message"].get("content") or "", u.get("prompt_tokens", 0), u.get("completion_tokens", 0),
                     round(time.time() - t0, 3), ch.get("finish_reason", ""))


class MockBackend:
    """Scripted policy for harness self-tests ONLY. Every record it produces is flagged is_mock=true."""
    is_mock = True
    model_label = "MOCK"

    def __init__(self, policy):
        self.policy, self.state = policy, {}

    def chat(self, messages, temperature, top_p, top_k, max_tokens, seed) -> Reply:
        text = self.policy(messages, self.state)
        return Reply(text, sum(len(m["content"]) for m in messages) // 4, len(text) // 4, 0.0, "stop")
