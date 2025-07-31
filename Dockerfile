# 使用官方 Python 基底映像
FROM python:3.12-slim

# 設定工作目錄
WORKDIR /app

# 複製所有檔案
COPY . .

# 安裝系統級套件與 Python 依賴
RUN apt-get update && \
    apt-get install -y gcc build-essential && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 執行 main.py
CMD ["python", "main.py"]
