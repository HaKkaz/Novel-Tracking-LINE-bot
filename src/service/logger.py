import logging

# 設置 logging 配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('service.log'),
        logging.StreamHandler()
    ]
)

# 創建一個全局 logger 實例
logger = logging.getLogger(__name__)