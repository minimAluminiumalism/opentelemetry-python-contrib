# main.py
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

def main():
    chat = ChatOpenAI(
        model="deepseek-chat", 
        temperature=0.7,
        openai_api_key = os.getenv("OPENAI_API_KEY"),
        openai_api_base = "https://api.deepseek.com/v1"
    )
    messages = [
        SystemMessage(content="You are a helpful AI assistant."),
        HumanMessage(content="Tell me a joke about OpenTelemetry")
    ]
    response = chat.invoke(messages)
    print("Chat response:", response.content)

if __name__ == "__main__":
    main()
