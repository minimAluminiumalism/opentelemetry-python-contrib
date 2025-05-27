# app.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_data():
    """
    对外暴露的 /api 接口，返回简单 JSON
    """
    return jsonify({
        "status": "success",
        "data": {
            "message": "Hello, Flask!",
            "port": 5002
        }
    })

if __name__ == '__main__':
    # 监听在 0.0.0.0:5002，外部可访问
    app.run(host='0.0.0.0', port=5001, debug=True)
