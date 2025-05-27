Ollama Chat 示例应用
====================

该示例演示如何使用 Ollama 客户端的 `chat` 方法（模型 `gemma3:1b`），并通过 OpenTelemetry 自动埋点将生成的 span 输出到控制台。

先决条件
--------
- 已安装并拉取模型：
  ```bash
  ollama pull gemma3:1b
  ```
- 启动 Ollama 服务：
  ```bash
  ollama serve
  ```

安装依赖
--------
```bash
pip install ollama \
  opentelemetry-api opentelemetry-sdk
# 安装本地 Ollama 插件
pip install -e ../..
```

运行示例
--------
```bash
export OLLAMA_MODEL=gemma3:1b
python main.py
```

控制台将输出 trace span 信息及聊天回复。 