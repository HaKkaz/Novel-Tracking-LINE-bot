from linebot.v3.messaging import ApiClient, MessagingApi
from linebot.v3.messaging.models import ReplyMessageRequest, TextMessage, BroadcastRequest
from src.service.config import configuration
from src.utils.time import get_current_time


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
    print(f'[{get_current_time()}] [DEBUG] broadcase message: {message}\n')
    try:
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.broadcast(
                BroadcastRequest(
                    messages=[TextMessage(text=message)]
                )
            )
    except Exception as e:
        print(f'Error in broadcast_message, {e}')
        print('current message:', message)