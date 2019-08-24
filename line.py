from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('R5jp0imIlnBLH6ZUePd+DJ6jSXjgEKJhnD8YLUdfqlcCscRhdmjIaqp4ykEqkuDZIthAo3wuYLd6Yd1R1DlbXzF0+uox1O5aR+VBKnoWtAaOCEyYdVY2CIGaTyMdAdEU1w5vc02AvQaS9kZDWb7wtQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f64450321859018d39180ac776621e9d')


@app.route("/")
def home():
    return 'home OK'


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


if __name__ == "__main__":
    app.run()