OpenTelemetry Ollama Instrumentation
====================================

该包为 Ollama LLM 客户端库提供 OpenTelemetry 插桩支持。

安装
-----
.. code-block:: bash

    pip install tapm-instrumentation-ollama

用法
-----
.. code-block:: python

    from opentelemetry.instrumentation.ollama import OllamaInstrumentor
    OllamaInstrumentor().instrument()

测试
-----
使用 pytest 和 VCR 录制网络请求：

.. code-block:: bash

    pytest --vcr-record=once 