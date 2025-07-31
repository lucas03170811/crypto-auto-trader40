FROM python:3.11-slim

WORKDIR /app

# 安裝系統構建工具和 Python 編譯相關依賴
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    python3-dev \
    gcc \
    git \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 安裝 setuptools 與 wheel（解決 pip install 失敗）
RUN pip install --upgrade pip setuptools wheel

# 安裝 ta-lib 相容版本（先裝 numpy 再裝 ta-lib）
RUN pip install numpy==1.23.5
RUN pip install ta-lib-bin==0.4.0.1

# 複製需求與程式碼
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
CMD ["python", "main.py"]
