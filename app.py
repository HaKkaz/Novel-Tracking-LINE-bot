import threading

from flask import Flask, request, abort
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from src.service import command, broadcast
from src.service.config import handler

app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def callback():
    if request.headers.get('X-Line-Signature') is None:
        abort(404)
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    msg: str = event.message.text
    if msg.startswith("訂閱"):
        command.subscribe(event)
    elif msg.startswith("取消"):
        command.unsubscribe(event)
    else:
        command.reply_message(event.reply_token, "請輸入正確指令")

# Start broadcast thread
broadcast_thread = threading.Thread(target=broadcast.broadcast_updates)
broadcast_thread.daemon = True
broadcast_thread.start()

# Start flask app
app.run(host='0.0.0.0', port=9876)