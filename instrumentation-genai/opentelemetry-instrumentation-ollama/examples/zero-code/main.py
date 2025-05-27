import os
import ollama
import sys

def main():
    model = os.getenv("OLLAMA_MODEL", "gemma3:1b")
    messages = [
        {"role": "user", "content": "Write a short poem on OpenTelemetry."},
    ]
    
    # 使用 streaming 模式调用 chat
    print("Chat response: ", end="", flush=True)
    
    # stream=True 启用流式响应
    for chunk in ollama.chat(
        model=model,
        messages=messages,
        stream=True,
    ):
        # 每收到一个响应块就打印出来
        chunk_content = chunk.get("message", {}).get("content", "")
        print(chunk_content, end="", flush=True)
        sys.stdout.flush()  # 确保输出立即显示
    
    print()  # 最后换行

if __name__ == "__main__":
    main()
