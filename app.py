from flask import Flask,render_template,request,jsonify
from openai import OpenAI
from dotenv import load_dotenv
from flask import Response
import os

load_dotenv()

api_key = os.getenv("DASHSCOPE_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
app = Flask(__name__)

#保存聊天记录
messages = [
    {
        "role": "system",
        "content": "你是一个专业的Python老师，回答要清晰易懂。"
    }
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

    messages.append({
        "role":"user",
        "content": user_message
    })
    def generate():

        response = client.chat.completions.create(
            model="qwen-plus",
            messages=messages,
            stream=True
        )

        ai_reply = ""

        for chunk in response:
            if chunk.choices[0].delta.content:
                text = chunk.choices[0].delta.content
                ai_reply += text
                yield text
    
        messages.append({
            "role":"assistant",
            "content":ai_reply
        })

    return Response(generate(), content_type="text/plain")

if __name__ =="__main__":
    app.run(debug=True)