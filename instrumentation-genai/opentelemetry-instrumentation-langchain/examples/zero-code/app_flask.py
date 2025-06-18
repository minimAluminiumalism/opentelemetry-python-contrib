# app_flask.py
import os
import uuid
import secrets
from flask import Flask, request, jsonify, session
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# 存储会话历史的字典
chat_histories = {}

def get_chat_response(query, session_id=None):
    if session_id is None:
        session_id = str(uuid.uuid4())
    
    chat = ChatOpenAI(
        model="deepseek-chat", 
        temperature=0.7,
        openai_api_key = os.getenv("OPENAI_API_KEY"),
        openai_api_base = "https://api.deepseek.com/v1",
        verbose=True
    )
    
    system_prompt = """你是一个非常有帮助的AI助手。
    你需要根据聊天历史和用户的问题提供有用、准确且详细的回答。
    如果你不知道答案，请诚实地说你不知道，不要编造信息。
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    
    chain = prompt | chat | StrOutputParser()
    
    # 添加消息历史支持
    chain_with_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: get_or_create_history(session_id),
        input_messages_key="input",
        history_messages_key="history",
    )
    
    # 执行链并获取响应
    response = chain_with_history.invoke(
        {"input": query},
        config={"configurable": {"session_id": session_id}}
    )
    
    return response

def get_or_create_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in chat_histories:
        chat_histories[session_id] = ChatMessageHistory()
    return chat_histories[session_id]

@app.route('/', methods=['POST'])
def chat():
    data = request.json
    if not data or 'query' not in data:
        return jsonify({'error': '请提供查询内容'}), 400
    
    # 获取或创建会话ID
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    
    query = data['query']
    response = get_chat_response(query, session['session_id'])
    return jsonify({'response': response, 'session_id': session['session_id']})

@app.route('/', methods=['GET'])
def index():
    return """
    <html>
        <head>
            <title>LangChain聊天应用</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                #chat-box { height: 300px; border: 1px solid #ccc; margin-bottom: 10px; padding: 10px; overflow-y: auto; }
                #query { width: 80%; padding: 8px; }
                button { padding: 8px 15px; }
                .controls { display: flex; margin-top: 10px; }
                .controls button { margin-right: 10px; }
            </style>
        </head>
        <body>
            <h1>LangChain聊天应用</h1>
            <div id="chat-box"></div>
            <input type="text" id="query" placeholder="输入您的问题...">
            <button onclick="sendQuery()">发送</button>
            <div class="controls">
                <button onclick="clearChat()">清空对话</button>
            </div>

            <script>
                let sessionId = localStorage.getItem('session_id') || null;
                
                // 页面加载时显示会话ID状态
                window.onload = function() {
                    if(sessionId) {
                        console.log("使用现有会话ID:", sessionId);
                    } else {
                        console.log("尚无会话ID，将在首次对话时创建");
                    }
                };
                
                function sendQuery() {
                    const query = document.getElementById('query').value;
                    if (!query) return;
                    
                    // 显示用户问题
                    const chatBox = document.getElementById('chat-box');
                    chatBox.innerHTML += `<p><strong>问:</strong> ${query}</p>`;
                    document.getElementById('query').value = '';
                    
                    // 发送请求
                    fetch('/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ 
                            query: query,
                            session_id: sessionId
                        }),
                    })
                    .then(response => response.json())
                    .then(data => {
                        chatBox.innerHTML += `<p><strong>答:</strong> ${data.response}</p>`;
                        chatBox.scrollTop = chatBox.scrollHeight;
                        
                        // 保存会话ID
                        if(data.session_id) {
                            sessionId = data.session_id;
                            localStorage.setItem('session_id', sessionId);
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        chatBox.innerHTML += `<p><strong>错误:</strong> 请求失败</p>`;
                    });
                }
                
                function clearChat() {
                    // 清空聊天界面
                    document.getElementById('chat-box').innerHTML = '';
                    
                    // 重置会话ID
                    sessionId = null;
                    localStorage.removeItem('session_id');
                    
                    // 显示清空提示
                    document.getElementById('chat-box').innerHTML = '<p><em>对话已清空，将创建新的会话</em></p>';
                }
                
                // 按回车键发送
                document.getElementById('query').addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        sendQuery();
                    }
                });
            </script>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
