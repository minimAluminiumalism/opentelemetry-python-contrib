Zero-Code Instrumentation Example
==================================

This example demonstrates how to automatically instrument Langchain ChatOpenAI calls using the `opentelemetry-instrument` CLI.

Prerequisites
-------------
- Set the OpenAI API key as an environment variable:
  ```bash
  export OPENAI_API_KEY=<your_api_key>
  ```
- Run an OTLP collector locally or set the endpoint via:
  ```bash
  export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
  ```

Install Dependencies
--------------------
```bash
pip install -r requirements.txt
pip install -e ../..
```

Run Example
-----------
```bash
# enable use the agent if virtualenv
.venv/bin/opentelemetry-instrument python app.py
```

After running the command, you should see spans printed to the console along with the chat response. 

Combine
-------

When integrating Langchain's instrumentation with existing OpenTelemetry instrumentation, multiple spans may appear outside of a single trace.

.. image:: ../../../../assets/auto-llm-combine/langchain.png