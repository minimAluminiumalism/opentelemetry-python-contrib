import pytest
import ollama
from opentelemetry.semconv_ai import SpanAttributes

@pytest.mark.vcr
def test_ollama_generation(exporter):
    # 调用 ollama.generate 触发插桩
    response = ollama.generate(
        model="gemma3:1b", prompt="Tell me a joke about OpenTelemetry"
    )

    spans = exporter.get_finished_spans()
    ollama_span = spans[0]
    assert ollama_span.name == "ollama.completion"
    assert ollama_span.attributes.get(f"{SpanAttributes.LLM_SYSTEM}") == "Ollama"
    assert (
        ollama_span.attributes.get(f"{SpanAttributes.LLM_REQUEST_TYPE}") == "completion"
    )
    assert not ollama_span.attributes.get(f"{SpanAttributes.LLM_IS_STREAMING}")
    assert ollama_span.attributes.get(f"{SpanAttributes.LLM_REQUEST_MODEL}") == "gemma3:1b"
    assert (
        ollama_span.attributes.get(f"{SpanAttributes.LLM_PROMPTS}.0.content")
        == "Tell me a joke about OpenTelemetry"
    )
    assert (
        ollama_span.attributes.get(f"{SpanAttributes.LLM_COMPLETIONS}.0.content")
        == response.get("response")
    )
    prompt_tokens = ollama_span.attributes.get(SpanAttributes.LLM_USAGE_PROMPT_TOKENS)
    assert prompt_tokens > 0
    total = ollama_span.attributes.get(SpanAttributes.LLM_USAGE_COMPLETION_TOKENS) + prompt_tokens
    assert ollama_span.attributes.get(SpanAttributes.LLM_USAGE_TOTAL_TOKENS) == total 