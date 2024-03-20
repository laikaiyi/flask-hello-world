from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage   # 載入 TextSendMessage 模組
import json


app = Flask(__name__)
@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    try:
        
        line_bot_api.reply_message(tk, TextSendMessage(text=response_text))      # 回傳訊息
    except Exception as e:
        print(f"捕獲到異常：{type(e).__name__}: {str(e)}")
    return 'OK'


@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    # print(json_data)
    try:
        line_bot_api = LineBotApi('FgRwDsmCC055uMWW/YTiv/X/+vP+WzYMz/X6nl9wde6iaB/Q/C1chDgrGCDxHJVnK5mcR8wJmKuYCT5cK5OGRbw1e6BW9C9JtQaQefu7hJ9vQ8WqomLTg4kjzZDYxNk4fIQmma6GJMZAKRauBWTjQgdB04t89/1O/w1cDnyilFU=')
        handler = WebhookHandler('d59461ed36fad764c35e258a67fe724f')
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']                 # 取得 reply token
        msg = json_data['events'][0]['message']['text']           # 取得使用者發送的訊息
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        user_id = json_data['events'][0]['source']['userId']  # 取得使用者 ID
        msg = json_data['events'][0]['message']['text']   # 取得使用者發送的訊息
        print(f'使用者傳送訊息: {msg}') 
        if msg == "預約羽球課":
            students[user_id] = True  # 將使用者加入到預約名單中
            response_text = "已收到您的預約，謝謝！"
        else:
            response_text = "感謝您的訊息！"
            line_bot_api.reply_message(tk, TextSendMessage(text=msg)) # 回傳訊息(目前單純重複使用者的訊息)
    except Exception as e:
        print(f"捕獲到異常：{type(e).__name__}: {str(e)}")
    return 'OK'

@app.route('/')
def hello_world():
    return 'Hello, World!'
