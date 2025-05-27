Ollama Zero-Code Instrumentation 示例
=======================================

该示例演示如何通过 `opentelemetry-instrument` 命令对 Ollama 的 `chat` 调用实现零代码插桩。

先决条件
--------
- 已安装并拉取模型：
  ```bash
  ollama pull gemma3:1b
  ```
- 启动 Ollama 服务（默认监听 127.0.0.1:11434）：
  ```bash
  ollama serve
  ```
- 启动 OTLP 接收端，例如在本地运行 Collector，监听 `http://localhost:4317`。

安装依赖
--------
```bash
pip install -r requirements.txt
# 安装本地 Ollama 插件
pip install -e ../..
```

运行示例
--------
1. 可选：通过 `.env` 文件或环境变量配置模型名和 OTLP 端点：
   ```bash
   export OLLAMA_MODEL=gemma3:1b
   export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
   ```
2. 启动插桩并运行脚本：
   ```bash
   opentelemetry-instrument python main.py
   ```

执行后，你将在终端看到自动生成的 span（包含模型、请求时长等属性）以及返回的聊天内容。 