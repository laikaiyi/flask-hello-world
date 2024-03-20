from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage   # 載入 TextSendMessage 模組
import json


app = Flask(__name__)


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
        print(f'使用者傳送訊息: {msg}')                             # 印出使用者發送的訊息
        line_bot_api.reply_message(tk, TextSendMessage(text=msg)) # 回傳訊息(目前單純重複使用者的訊息)
    except Exception as e:
        print(f"捕獲到異常：{type(e).__name__}: {str(e)}")
    return 'OK'

@app.route('/')
def hello_world():
    return 'Hello, World!'
