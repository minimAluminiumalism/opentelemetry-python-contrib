import pytest
import os
from opentelemetry.semconv_ai import SpanAttributes


@pytest.mark.vcr
@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"), 
    reason="OpenAI API key not available"
)
def test_langchain_llm_openai(exporter):
    """Test Langchain OpenAI LLM instrumentation"""
    from langchain_openai import OpenAI
    
    # Create LLM instance
    llm = OpenAI(
        model="gpt-3.5-turbo-instruct",
        temperature=0.7,
        max_tokens=100
    )
    
    # Execute LLM call
    prompt = "Tell me a joke about OpenTelemetry"
    response = llm.invoke(prompt)
    
    # Verify spans
    spans = exporter.get_finished_spans()
    assert len(spans) >= 1
    
    # Find LLM span
    llm_span = None
    for span in spans:
        if span.attributes.get(SpanAttributes.LLM_SYSTEM) == "Langchain":
            llm_span = span
            break
    
    assert llm_span is not None
    assert llm_span.attributes.get(SpanAttributes.LLM_SYSTEM) == "Langchain"
    assert llm_span.attributes.get(SpanAttributes.LLM_REQUEST_TYPE) == "completion"
    assert llm_span.attributes.get(SpanAttributes.LLM_REQUEST_MODEL) == "gpt-3.5-turbo-instruct"
    
    # Verify prompt and response
    assert llm_span.attributes.get(f"{SpanAttributes.LLM_PROMPTS}.0.role") == "user"
    assert llm_span.attributes.get(f"{SpanAttributes.LLM_PROMPTS}.0.content") == prompt
    assert llm_span.attributes.get(f"{SpanAttributes.LLM_COMPLETIONS}.0.role") == "assistant"
    assert llm_span.attributes.get(f"{SpanAttributes.LLM_COMPLETIONS}.0.content") == response
    
    # Verify token usage
    assert llm_span.attributes.get(SpanAttributes.LLM_USAGE_PROMPT_TOKENS) is not None
    assert llm_span.attributes.get(SpanAttributes.LLM_USAGE_COMPLETION_TOKENS) is not None
    assert llm_span.attributes.get(SpanAttributes.LLM_USAGE_TOTAL_TOKENS) is not None


@pytest.mark.vcr
def test_langchain_llm_fake(exporter):
    """Test Langchain FakeListLLM instrumentation (no API key required)"""
    from langchain_community.llms.fake import FakeListLLM
    
    # Create FakeListLLM instance
    responses = ["This is a test response", "This is second response"]
    llm = FakeListLLM(responses=responses)
    
    # Execute LLM call
    prompt = "Test prompt"
    response = llm.invoke(prompt)
    
    # Verify spans
    spans = exporter.get_finished_spans()
    assert len(spans) >= 1
    
    # Find LLM span
    llm_span = None
    for span in spans:
        if span.attributes.get(SpanAttributes.LLM_SYSTEM) == "Langchain":
            llm_span = span
            break
    
    assert llm_span is not None
    assert llm_span.attributes.get(SpanAttributes.LLM_SYSTEM) == "Langchain"
    assert llm_span.attributes.get(SpanAttributes.LLM_REQUEST_TYPE) == "completion"
    
    # Verify prompt and response
    assert llm_span.attributes.get(f"{SpanAttributes.LLM_PROMPTS}.0.role") == "user"
    assert llm_span.attributes.get(f"{SpanAttributes.LLM_PROMPTS}.0.content") == prompt
    assert llm_span.attributes.get(f"{SpanAttributes.LLM_COMPLETIONS}.0.role") == "assistant"
    assert llm_span.attributes.get(f"{SpanAttributes.LLM_COMPLETIONS}.0.content") == response
    assert response == responses[0]  # FakeListLLM returns the first response 