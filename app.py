from flask import Flask, request, abort, jsonify

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, StickerSendMessage, FollowEvent, UnfollowEvent, JoinEvent, LeaveEvent
)

app = Flask(__name__)
app.config["DEBUG"] = True

# Channel access token
line_bot_api = LineBotApi('你的token')
# Channel secret
handler = WebhookHandler('你的 Webhook token')

admin_userid = '你的 userid'

sent_message = TextSendMessage(text='Link Start !')
line_bot_api.push_message(admin_userid, sent_message)


@app.route('/', methods=['GET'])
def home():
    return "<h1>Line Bot alive check !!</h1>"


@app.route('/data', methods=['GET', 'POST'])
def look_post_data():
    try:
        app.logger.info("get_data() :" + str(request.get_data()))
    except Exception as e:
        app.logger.info("Exception :" + e)
    return 'OK'


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

    user_message = event.message.text
    userid = event.source.user_id

    profile = line_bot_api.get_profile(userid)
    sent_message = TextSendMessage(
        text=profile.display_name + '\n' + profile.user_id + '\n' + user_message)
    line_bot_api.push_message(admin_userid, sent_message)


@handler.add(FollowEvent)
def handle_follow(event):
    app.logger.info("Got Follow event:" + event.source.user_id)
    profile = line_bot_api.get_profile(event.source.user_id)
    line_bot_api.push_message(
        admin_userid, TextSendMessage(text=profile.user_id+' Got follow event'))


@handler.add(UnfollowEvent)
def handle_unfollow(event):
    app.logger.info("Got Unfollow event:" + event.source.user_id)


@handler.add(JoinEvent)
def handle_join(event):
    line_bot_api.push_message(admin_userid, TextSendMessage(
        text='Joined this ' + event.source.type))


@handler.add(LeaveEvent)
def handle_leave():
    app.logger.info("Got leave event")


if __name__ == '__main__':

    app.run()
    # app.run(host='0.0.0.0', port=8000)

    # 圖片
    img_url = 'https://yt3.ggpht.com/uMUat6yJL2_Sk6Wg2-yn0fSIqUr_D6aKVNVoWbgeZ8N-edT5QJAusk4PI8nmPgT_DxFDTyl8=s900-c-k-c0x00ffffff-no-rj'
    img_url = 'https://i1.hdslb.com/bfs/archive/90b4a45163eb27eb4c0ce911fca38e2d64d876c5.jpg@480w_270h_1c'
    sent_image_test = ImageSendMessage(
        original_content_url=img_url,
        preview_image_url=img_url
    )
    # 貼圖
    sticker_message = StickerSendMessage(
        package_id='1',
        sticker_id='1'
    )
