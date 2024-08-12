from datetime import datetime

def get_current_time() -> str:
    now = datetime.now()
    formatted_time = now.strftime("%Y/%m/%d %H:%M:%S")
    return formatted_time