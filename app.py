from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage   # 載入 TextSendMessage 模組
import json


app = Flask(__name__)
def reserve_class(student_id):
    # 在這裡實現預約課程的相關邏輯，例如儲存學生的預約狀態到資料庫中等

# 每週日向學生發送是否預約上課的通知
def send_notification():
    today = datetime.date.today()
    if today.weekday() == 6:  # 檢查今天是否是週日 (週日是星期天，weekday() 回傳的是 6)
        # 在這裡實現發送通知的相關邏輯，例如從資料庫中取得預約狀態，然後發送通知給學生

        # 假設我們有一個名為 students 的列表，其中包含所有學生的 Line 使用者 ID
        students = ['student1_id', 'student2_id', 'student3_id']
        for student_id in students:
            message = TextSendMessage(text="請問您這週是否預約上羽球課程？")
            try:
                line_bot_api.push_message(student_id, messages=message)
            except LineBotApiError as e:
                print("發送訊息時發生錯誤:", e)

# 假設有一個 Webhook 接收使用者的訊息，然後根據訊息的內容執行不同的動作
# 這裡假設使用者發送 "預約羽球課" 來預約課程
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    message_text = event.message.text

    if message_text == "預約羽球課":
        reserve_class(user_id)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="已收到您的預約！"))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請回覆「預約羽球課」來預約課程。"))

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
