# pylint: skip-file
"""
示例：使用 Ollama Chat 与 OpenTelemetry 自动埋点
"""
import os
import ollama

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
from opentelemetry.instrumentation.ollama import OllamaInstrumentor

# 配置追踪器，将 span 输出到控制台
trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    SimpleSpanProcessor(ConsoleSpanExporter())
)

# 启用 Ollama 插桩
OllamaInstrumentor().instrument()


def main():
    model = os.getenv("OLLAMA_MODEL", "gemma3:1b")
    messages = [
        {"role": "user", "content": "Tell me a joke about OpenTelemetry"},
    ]

    # 调用 chat 并触发自动埋点
    response = ollama.chat(model=model, messages=messages)

    print("Chat response:", response.get("response"))


if __name__ == "__main__":
    main() 