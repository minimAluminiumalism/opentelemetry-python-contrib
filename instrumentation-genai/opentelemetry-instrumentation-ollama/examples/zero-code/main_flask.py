import os
import ollama
import sys
from flask import Flask, request, Response, jsonify

app = Flask(__name__)

@app.route('/generate', methods=['GET'])
def generate():
    # 从查询参数中获取提示，如果没有则使用默认提示
    prompt = request.args.get('prompt', 'Write a short poem on OpenTelemetry.')
    model = os.getenv("OLLAMA_MODEL", "gemma3:1b")
    
    # 构建消息
    messages = [
        {"role": "user", "content": prompt},
    ]
    
    # 检查是否请求流式响应 (true, 1, yes 等值都会被视为 True)
    stream_param = request.args.get('stream', 'false').lower()
    stream = stream_param in ('true', '1', 'yes', 'y')
    
    if stream:
        # 流式响应
        def generate_stream():
            for chunk in ollama.chat(model=model, messages=messages, stream=True):
                chunk_content = chunk.get("message", {}).get("content", "")
                if chunk_content:
                    yield chunk_content
        
        return Response(generate_stream(), mimetype='text/plain')
    else:
        # 非流式响应
        response = ollama.chat(model=model, messages=messages)
        return jsonify({"response": response.get("message", {}).get("content", "")})

if __name__ == "__main__":
    # 不要在 debug 模式下启动 reloader，reloader 会重新加载应用程序，导致链路数据无法捕获
    # DO NOT use app.run(host='0.0.0.0', port=5001, debug=True)
    # You can use app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False)
    app.run(host="0.0.0.0", port=5001)
