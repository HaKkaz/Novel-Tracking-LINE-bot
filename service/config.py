from linebot.v3 import WebhookHandler
from linebot.v3.messaging import Configuration
from dotenv import load_dotenv
import os

load_dotenv()
LINE_CHANNEL_ACCESS_TOKEN=os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET=os.getenv('LINE_CHANNEL_SECRET')

BROADCAST_INTERVAL = 300

configuration = Configuration(
    access_token=LINE_CHANNEL_ACCESS_TOKEN
)
handler = WebhookHandler(LINE_CHANNEL_SECRET)