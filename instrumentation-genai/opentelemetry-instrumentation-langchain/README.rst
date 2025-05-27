OpenTelemetry Langchain Instrumentation
========================================

该包为 Langchain 框架提供 OpenTelemetry 插桩支持。

安装
----

::

    pip install opentelemetry-instrumentation-langchain

使用方法
--------

.. code-block:: python

    from opentelemetry.instrumentation.langchain import LangchainInstrumentor
    LangchainInstrumentor().instrument()

    # 现在您的 Langchain 应用程序将自动生成 traces

API
---

.. automodule:: opentelemetry.instrumentation.langchain
    :members:
    :undoc-members:
    :show-inheritance: 