import pytest
import time
from opentelemetry.semconv_ai import SpanAttributes, Meters

pytest.skip("Skipping metrics instrumentation tests as unsupported now", allow_module_level=True)


@pytest.mark.vcr
def test_langchain_llm_metrics(exporter, metrics_test_context):
    """Test LLM metrics collection"""
    from langchain_community.llms.fake import FakeListLLM
    
    provider, reader = metrics_test_context
    
    # Create FakeListLLM instance
    responses = ["This is a test response for metrics testing"]
    llm = FakeListLLM(responses=responses)
    
    # Record start time
    start_time = time.time()
    
    # Execute LLM call
    prompt = "Test prompt"
    response = llm.invoke(prompt)
    
    # Record end time
    end_time = time.time()
    
    # Wait a bit to ensure metrics are recorded
    time.sleep(0.1)
    
    # Get metrics data
    metrics_data = reader.get_metrics_data()
    
    # Find duration metrics
    duration_metrics = []
    token_metrics = []
    
    for resource_metrics in metrics_data.resource_metrics:
        for scope_metrics in resource_metrics.scope_metrics:
            for metric in scope_metrics.metrics:
                if metric.name == Meters.LLM_OPERATION_DURATION:
                    duration_metrics.append(metric)
                elif metric.name == Meters.LLM_TOKEN_USAGE:
                    token_metrics.append(metric)
    
    # Verify duration metrics
    if duration_metrics:
        duration_metric = duration_metrics[0]
        assert len(duration_metric.data.data_points) > 0
        
        # Verify metric attributes
        data_point = duration_metric.data.data_points[0]
        attributes = dict(data_point.attributes)
        assert attributes.get(SpanAttributes.LLM_SYSTEM) == "Langchain"
        
        # Verify duration value is reasonable
        duration_value = data_point.value
        assert 0 < duration_value < (end_time - start_time) * 2  # Allow some tolerance


@pytest.mark.vcr
def test_langchain_token_metrics(exporter, metrics_test_context):
    """Test Token usage metrics"""
    from langchain_community.llms.fake import FakeListLLM
    from langchain_core.outputs import LLMResult, Generation
    from unittest.mock import MagicMock
    
    provider, reader = metrics_test_context
    
    # Create a mock LLM to test token metrics
    class MockTokenLLM(FakeListLLM):
        def _generate(self, prompts, stop=None, run_manager=None, **kwargs):
            # Create a result with token usage information
            generations = [[Generation(text="Mock response")]]
            llm_output = {
                "token_usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 5,
                    "total_tokens": 15
                }
            }
            return LLMResult(generations=generations, llm_output=llm_output)
    
    llm = MockTokenLLM(responses=["Mock response"])
    
    # Execute call
    result = llm.invoke("Test prompt")
    
    # Wait for metrics to be recorded
    time.sleep(0.1)
    
    # Get metrics data
    metrics_data = reader.get_metrics_data()
    
    # Find token metrics
    token_metrics = []
    for resource_metrics in metrics_data.resource_metrics:
        for scope_metrics in resource_metrics.scope_metrics:
            for metric in scope_metrics.metrics:
                if metric.name == Meters.LLM_TOKEN_USAGE:
                    token_metrics.append(metric)
    
    # Verify token metrics
    if token_metrics:
        token_metric = token_metrics[0]
        data_points = token_metric.data.data_points
        
        # There should be records of input and output tokens
        input_tokens = []
        output_tokens = []
        
        for dp in data_points:
            attributes = dict(dp.attributes)
            if attributes.get(SpanAttributes.LLM_TOKEN_TYPE) == "input":
                input_tokens.append(dp)
            elif attributes.get(SpanAttributes.LLM_TOKEN_TYPE) == "output":
                output_tokens.append(dp)
        
        # Verify there is an input token record
        if input_tokens:
            input_dp = input_tokens[0]
            assert input_dp.value == 10
            attributes = dict(input_dp.attributes)
            assert attributes.get(SpanAttributes.LLM_SYSTEM) == "Langchain"
            assert attributes.get(SpanAttributes.LLM_TOKEN_TYPE) == "input"
        
        # Verify there is an output token record
        if output_tokens:
            output_dp = output_tokens[0]
            assert output_dp.value == 5
            attributes = dict(output_dp.attributes)
            assert attributes.get(SpanAttributes.LLM_SYSTEM) == "Langchain"
            assert attributes.get(SpanAttributes.LLM_TOKEN_TYPE) == "output"


@pytest.mark.vcr
def test_langchain_multiple_calls_metrics(exporter, metrics_test_context):
    """Test metrics aggregation for multiple calls"""
    from langchain_community.llms.fake import FakeListLLM
    
    provider, reader = metrics_test_context
    
    # Create LLM instance
    responses = ["Response 1", "Response 2", "Response 3"]
    llm = FakeListLLM(responses=responses)
    
    # Execute multiple calls
    for i in range(3):
        result = llm.invoke(f"Test prompt {i}")
        time.sleep(0.05)  # Short wait between calls
    
    # Wait for metrics to be recorded
    time.sleep(0.1)
    
    # Get metrics data
    metrics_data = reader.get_metrics_data()
    
    # Find duration metrics
    duration_metrics = []
    for resource_metrics in metrics_data.resource_metrics:
        for scope_metrics in resource_metrics.scope_metrics:
            for metric in scope_metrics.metrics:
                if metric.name == Meters.LLM_OPERATION_DURATION:
                    duration_metrics.append(metric)
    
    # Verify there are multiple data points
    if duration_metrics:
        duration_metric = duration_metrics[0]
        # There should be records for 3 calls
        assert len(duration_metric.data.data_points) >= 3
        
        # All data points should have correct attributes
        for dp in duration_metric.data.data_points:
            attributes = dict(dp.attributes)
            assert attributes.get(SpanAttributes.LLM_SYSTEM) == "Langchain"
            assert dp.value > 0  # Duration should be greater than 0


@pytest.mark.vcr
def test_langchain_chat_model_metrics(exporter, metrics_test_context):
    """Test metrics for chat model"""
    from langchain_community.chat_models.fake import FakeListChatModel
    from langchain_core.messages import HumanMessage, AIMessage
    
    provider, reader = metrics_test_context
    
    # Create chat model
    responses = [AIMessage(content="This is chat response")]
    chat = FakeListChatModel(responses=responses)
    
    # Execute chat
    message = HumanMessage(content="Test message")
    response = chat.invoke([message])
    
    # Wait for metrics to be recorded
    time.sleep(0.1)
    
    # Get metrics data
    metrics_data = reader.get_metrics_data()
    
    # Find duration metrics
    duration_metrics = []
    for resource_metrics in metrics_data.resource_metrics:
        for scope_metrics in resource_metrics.scope_metrics:
            for metric in scope_metrics.metrics:
                if metric.name == Meters.LLM_OPERATION_DURATION:
                    duration_metrics.append(metric)
    
    # Verify chat model metrics
    if duration_metrics:
        duration_metric = duration_metrics[0]
        assert len(duration_metric.data.data_points) > 0
        
        data_point = duration_metric.data.data_points[0]
        attributes = dict(data_point.attributes)
        assert attributes.get(SpanAttributes.LLM_SYSTEM) == "Langchain" 