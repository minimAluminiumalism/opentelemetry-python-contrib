import os
import pytest
import vcr
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.instrumentation.langchain import LangchainInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import InMemoryMetricReader

pytest_plugins = []

@pytest.fixture(scope="session")
def exporter():
    exporter = InMemorySpanExporter()
    processor = SimpleSpanProcessor(exporter)

    provider = TracerProvider()
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    LangchainInstrumentor().instrument()

    return exporter


@pytest.fixture(autouse=True)
def clear_exporter(exporter):
    exporter.clear()


@pytest.fixture(scope="session")
def metrics_test_context():
    resource = Resource.create()
    reader = InMemoryMetricReader()
    provider = MeterProvider(metric_readers=[reader], resource=resource)
    metrics.set_meter_provider(provider)
    LangchainInstrumentor().instrument(meter_provider=provider)
    return provider, reader


@pytest.fixture(scope="session", autouse=True)
def clear_metrics_test_context(metrics_test_context):
    provider, reader = metrics_test_context
    reader.shutdown()
    provider.shutdown()


def scrub_api_key(response):
    if 'headers' in response:
        if 'authorization' in response['headers']:
            response['headers']['authorization'] = ['Bearer REDACTED']
        if 'x-api-key' in response['headers']:
            response['headers']['x-api-key'] = ['REDACTED']
    return response


def scrub_request(request):
    if hasattr(request, 'headers'):
        if 'authorization' in request.headers:
            request.headers['authorization'] = 'Bearer REDACTED'
        if 'x-api-key' in request.headers:
            request.headers['x-api-key'] = 'REDACTED'
    return request


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_headers": ["authorization", "x-api-key"],
        "filter_query_parameters": ["api_key"],
        "before_record_response": scrub_api_key,
        "before_record_request": scrub_request,
        "record_mode": "once",
        "match_on": ["uri", "method", "body"],
        "cassette_library_dir": "tests/cassettes",
    }


@pytest.fixture(autouse=True)
def vcr_setup(request, vcr_config):
    if request.node.get_closest_marker("vcr"):
        test_name = request.node.name
        cassette_path = f"{test_name}.yaml"
        
        with vcr.use_cassette(cassette_path, **vcr_config):
            yield
    else:
        yield 