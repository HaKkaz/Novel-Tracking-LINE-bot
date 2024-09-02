# 使用官方的 Python 3.9 slim 作為基礎映像
FROM python:3.9-slim

# 設置工作目錄
WORKDIR /app

# 複製當前目錄所有內容到容器中
COPY . .

# 安裝 Flask 及其他需求的包
RUN pip install --no-cache-dir -r requirements.txt

# 開放 5000 端口
EXPOSE 5000

# 設定環境變量
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# 定義容器啟動時執行的命令
CMD ["python3", "app.py"]
