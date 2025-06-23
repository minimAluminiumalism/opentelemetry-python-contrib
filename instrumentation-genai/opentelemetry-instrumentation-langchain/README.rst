OpenTelemetry Langchain Instrumentation
========================================

This package provides OpenTelemetry instrumentation support for the Langchain framework.

Installation
------------

::

    pip install tapm-instrumentation-langchain

Usage
-----

.. code-block:: python

    from opentelemetry.instrumentation.langchain import LangchainInstrumentor
    LangchainInstrumentor().instrument()

    # Now your Langchain application will automatically generate traces 