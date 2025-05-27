Manual Instrumentation Example
==============================

This example demonstrates how to programmatically instrument Langchain ChatOpenAI calls.

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
python main.py
```

After running the command, you should see spans printed to the console along with the chat response. 