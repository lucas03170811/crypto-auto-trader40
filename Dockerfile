FROM python:3.11-slim

WORKDIR /app

# 安裝系統相依套件與建構工具
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    wget \
    git \
    python3-dev \
    gcc \
    && apt-get clean

# 安裝 Python 套件建構工具
RUN pip install --upgrade pip setuptools wheel

# 安裝 numpy 與 ta-lib-bin（先裝 numpy 兼容 ta-lib-bin）
RUN pip install numpy==1.23.5
RUN pip install ta-lib-bin==0.4.0.1

# 複製 requirements 並安裝其餘依賴
COPY requirements.txt .
RUN pip install -r requirements.txt

# 複製程式碼
COPY . .

# 啟用非快取模式（避免 stdout 被緩存）
ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
