import pytest
import os
from opentelemetry.semconv_ai import SpanAttributes


@pytest.mark.vcr
@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"), 
    reason="OpenAI API key not available"
)
def test_langchain_chat_model_openai(exporter):
    """Test Langchain ChatOpenAI model instrumentation"""
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage, SystemMessage
    
    # Create chat model instance
    chat = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=100
    )
    
    # Create messages
    messages = [
        SystemMessage(content="You are a helpful AI assistant."),
        HumanMessage(content="Tell me a joke about OpenTelemetry")
    ]
    
    # Execute chat call
    response = chat.invoke(messages)
    
    # Verify spans
    spans = exporter.get_finished_spans()
    assert len(spans) >= 1
    
    # Find chat model span
    chat_span = None
    for span in spans:
        if span.attributes.get(SpanAttributes.LLM_SYSTEM) == "Langchain":
            chat_span = span
            break
    
    assert chat_span is not None
    assert chat_span.attributes.get(SpanAttributes.LLM_SYSTEM) == "Langchain"
    assert chat_span.attributes.get(SpanAttributes.LLM_REQUEST_TYPE) == "chat"
    assert chat_span.attributes.get(SpanAttributes.LLM_REQUEST_MODEL) == "gpt-3.5-turbo"
    
    # Verify messages
    assert chat_span.attributes.get(f"{SpanAttributes.LLM_PROMPTS}.0.role") == "system"
    assert chat_span.attributes.get(f"{SpanAttributes.LLM_PROMPTS}.0.content") == "You are a helpful AI assistant."
    assert chat_span.attributes.get(f"{SpanAttributes.LLM_PROMPTS}.1.role") == "user"
    assert chat_span.attributes.get(f"{SpanAttributes.LLM_PROMPTS}.1.content") == "Tell me a joke about OpenTelemetry"
    
    # Verify response
    assert chat_span.attributes.get(f"{SpanAttributes.LLM_COMPLETIONS}.0.role") == "assistant"
    assert chat_span.attributes.get(f"{SpanAttributes.LLM_COMPLETIONS}.0.content") == response.content
    
    # Verify token usage
    assert chat_span.attributes.get(SpanAttributes.LLM_USAGE_PROMPT_TOKENS) is not None
    assert chat_span.attributes.get(SpanAttributes.LLM_USAGE_COMPLETION_TOKENS) is not None
    assert chat_span.attributes.get(SpanAttributes.LLM_USAGE_TOTAL_TOKENS) is not None


@pytest.mark.vcr
def test_langchain_chat_model_fake(exporter):
    """Test Langchain FakeListChatModel instrumentation (no API key required)"""
    from langchain_community.chat_models.fake import FakeListChatModel
    from langchain_core.messages import HumanMessage
    
    # Create FakeListChatModel instance with string responses
    responses = ["This is a test response", "This is second response"]
    chat = FakeListChatModel(responses=responses)
    
    # Execute chat call
    message = HumanMessage(content="Test message")
    response = chat.invoke([message])
    
    # Verify spans
    spans = exporter.get_finished_spans()
    assert len(spans) >= 1
    
    # Find chat model span
    chat_span = None
    for span in spans:
        if span.attributes.get(SpanAttributes.LLM_SYSTEM) == "Langchain":
            chat_span = span
            break
    
    assert chat_span is not None
    assert chat_span.attributes.get(SpanAttributes.LLM_SYSTEM) == "Langchain"
    assert chat_span.attributes.get(SpanAttributes.LLM_REQUEST_TYPE) == "chat"
    
    # Verify messages
    assert chat_span.attributes.get(f"{SpanAttributes.LLM_PROMPTS}.0.role") == "user"
    assert chat_span.attributes.get(f"{SpanAttributes.LLM_PROMPTS}.0.content") == "Test message"
    
    # Verify response
    assert chat_span.attributes.get(f"{SpanAttributes.LLM_COMPLETIONS}.0.role") == "assistant"
    assert chat_span.attributes.get(f"{SpanAttributes.LLM_COMPLETIONS}.0.content") == response.content
    assert response.content == responses[0]  # FakeListChatModel returns the first response


@pytest.mark.vcr
def test_langchain_chat_model_with_tools(exporter):
    """Test chat model instrumentation with tool calls"""
    from langchain_community.chat_models.fake import FakeMessagesListChatModel
    from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
    from langchain_core.tools import tool
    
    # Define a simple tool
    @tool
    def get_weather(location: str) -> str:
        """Get weather for specified location"""
        return f"Weather in {location} is sunny"
    
    # Create tool call response
    tool_call_response = AIMessage(
        content="I need to check weather information",
        tool_calls=[{
            "id": "call_123",
            "name": "get_weather",
            "args": {"location": "Beijing"}
        }]
    )
    
    responses = [tool_call_response]
    chat = FakeMessagesListChatModel(responses=responses)
    
    # Execute chat call without binding tools
    message = HumanMessage(content="How is the weather in Beijing?")
    response = chat.invoke([message])
    
    # Verify spans
    spans = exporter.get_finished_spans()
    assert len(spans) >= 1
    
    # Find chat model span
    chat_span = None
    for span in spans:
        if span.attributes.get(SpanAttributes.LLM_SYSTEM) == "Langchain":
            chat_span = span
            break
    
    assert chat_span is not None
    
    # Verify tool call (if supported)
    if hasattr(response, 'tool_calls') and response.tool_calls:
        # Verify tool call related attributes
        assert len(response.tool_calls) > 0
        tool_call = response.tool_calls[0]
        assert tool_call["name"] == "get_weather" 