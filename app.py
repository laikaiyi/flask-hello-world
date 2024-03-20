from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage   # 載入 TextSendMessage 模組
import json


app = Flask(__name__)

students = {}  # 學生預約的字典，將來存儲學生的預約信息

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    try:
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']         # 取得 reply token
        user_id = json_data['events'][0]['source']['userId']  # 取得使用者 ID
        msg = json_data['events'][0]['message']['text']   # 取得使用者發送的訊息
        if msg == "預約羽球課":
            students[user_id] = True  # 將使用者加入到預約名單中
            response_text = "好的，已收到您的預約。"
            # 傳送預約日期表單給學生填寫
            buttons_template = TemplateSendMessage(
                alt_text='預約日期表單',
                template=ButtonsTemplate(
                    title='預約日期表單',
                    text='請選擇您想要預約的日期：',
                    actions=[
                        PostbackTemplateAction(
                            label='3月5日',
                            data='booking_date_2024-03-05'
                        ),
                        PostbackTemplateAction(
                            label='3月12日',
                            data='booking_date_2024-03-12'
                        ),
                        PostbackTemplateAction(
                            label='3月19日',
                            data='booking_date_2024-03-19'
                        ),
                        PostbackTemplateAction(
                            label='3月26日',
                            data='booking_date_2024-03-26'
                        )
                    ]
                )
            )
            line_bot_api.reply_message(tk, [TextSendMessage(text=response_text), buttons_template])
        else:
            response_text = "感謝您的訊息！"
            line_bot_api.reply_message(tk, TextSendMessage(text=response_text))      # 回傳訊息
    except Exception as e:
        print(f"捕獲到異常：{type(e).__name__}: {str(e)}")
    return 'OK'

@app.route('/')
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
@app.route('/')
def handle_message(event):
    user_id = event.source.user_id
    message_text = event.message.text

    if message_text == "預約羽球課":
        reserve_class(user_id)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="已收到您的預約！"))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請回覆「預約羽球課」來預約課程。"))

@app.route('/')
def hello_world():
    return 'Hello, World!'
