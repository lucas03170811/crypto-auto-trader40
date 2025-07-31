# 使用輕量級 python 環境
FROM python:3.12-slim

# 設定工作目錄
WORKDIR /app

# 複製檔案
COPY . .

# 安裝套件
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# 執行程式
CMD ["python", "main.py"]
