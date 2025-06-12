import httpx

from lma.llm_client import LLMClient


def test_llm_client_openai(monkeypatch):
    called = {}

    def handler(request: httpx.Request) -> httpx.Response:
        called["path"] = request.url.path
        return httpx.Response(200, json={"choices": [{"message": {"content": "ok"}}]})

    transport = httpx.MockTransport(handler)

    cfg = {
        "llm": {
            "mode": "gpt-4o",
            "openai_api_key": "x",
        }
    }
    client = LLMClient(cfg)
    client.client = httpx.Client(transport=transport)
    result = client.send_prompt("hi")
    assert result == "ok"
    assert called["path"] == "/v1/chat/completions"
