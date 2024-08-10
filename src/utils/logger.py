import logging

# 設置 logging 配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('service_logs.log'),
        logging.StreamHandler()
    ]
)

# 創建一個全局 logger 實例
service_logger = logging.getLogger(__name__)