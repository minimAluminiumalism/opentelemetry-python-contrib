# main.py
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.langchain import LangchainInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

# Set up tracer and exporter
resource = Resource.create({SERVICE_NAME: "langchain-instr"})
trace.set_tracer_provider(TracerProvider(resource=resource))

trace.get_tracer_provider().add_span_processor(
    SimpleSpanProcessor(
        OTLPSpanExporter(endpoint="http://localhost:4317")
    )
)

# Instrument Langchain
LangchainInstrumentor().instrument()

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

def main():
    chat = ChatOpenAI(
        model="deepseek-chat", 
        temperature=0.7,
        openai_api_key = os.getenv("OPENAI_API_KEY"),
        openai_api_base = "https://api.deepseek.com/v1"
    )
    messages = [
        SystemMessage(content="You are a helpful AI assistant."),
        HumanMessage(content="Tell me a joke about OpenTelemetry")
    ]
    response = chat.invoke(messages)
    print("Chat response:", response.content)

if __name__ == "__main__":
    main() 