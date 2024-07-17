from linebot.v3.messaging import ApiClient, MessagingApi
from linebot.v3.messaging.models import ReplyMessageRequest, TextMessage
from service.config import configuration

def reply_message(reply_token, message):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=reply_token, 
                messages=[TextMessage(text=message)]
            )
        )

def subscribe(event):
    msg: str = event.message.text
    msg = msg.split()
    if len(msg) != 2:
        reply_message(event.reply_token, "訂閱說輸入指令: subscribe <novel_id>")

    with open('subscribers.txt', 'a') as f:
        user_id = event.source.user_id
        novel_id = msg[1]
        f.write(f'{user_id} {novel_id}\n')

def unsubscribe(event):
    pass