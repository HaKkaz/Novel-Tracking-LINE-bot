from linebot.v3.messaging import ApiClient, MessagingApi
from linebot.v3.messaging.models import ReplyMessageRequest, TextMessage, BroadcastRequest
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

def broadcast_message(message: str):
    print(f'[DEBUG] broadcase message: {message}')
    try:
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.broadcast(
                BroadcastRequest(
                    messages=[TextMessage(text=message)]
                )
            )
    except Exception as e:
        print(e)