OpenTelemetry Ollama Instrumentation
====================================

This package provides OpenTelemetry instrumentation support for Ollama LLM client libraries.

Installation
------------
.. code-block:: bash

    pip install tapm-instrumentation-ollama

Usage
-----
.. code-block:: python

    from opentelemetry.instrumentation.ollama import OllamaInstrumentor
    OllamaInstrumentor().instrument()

Testing
-------
Use pytest and VCR to record network requests:

.. code-block:: bash

    pytest --vcr-record=once 