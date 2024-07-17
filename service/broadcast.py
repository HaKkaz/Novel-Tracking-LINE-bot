from linebot.v3.messaging.models import BroadcastRequest
from linebot.v3.messaging import (
    ApiClient, 
    MessagingApi,
    TextMessage
)

from .config import configuration
import time

def broadcast_message():
    while True:
        try:
            with ApiClient(configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                line_bot_api.broadcast(
                    BroadcastRequest(
                        messages=[TextMessage(text="Hello, BroadCast!")]
                    )
                )
        except Exception as e:
            print(e)
        time.sleep(60)