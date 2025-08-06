# Dockerfile

FROM python:3.11-slim

WORKDIR /app

# 安裝系統依賴與編譯工具
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    python3-setuptools \
    wget \
    git \
    && apt-get clean

# 清除 Python 快取與 __pycache__
RUN find . -name "*.pyc" -delete && find . -name "__pycache__" -type d -exec rm -r {} +

# 升級 pip + 安裝 numpy（與 ta-lib 相容版本）
RUN pip install --upgrade pip
RUN pip install numpy==1.23.5

# 安裝 ta-lib 二進位版本
RUN pip install ta-lib-bin

# 複製 requirements.txt 並安裝依賴
COPY requirements.txt .
RUN echo "======= REQUIREMENTS CONTENT =======" && cat requirements.txt
RUN pip install -r requirements.txt

# 複製全部原始碼
COPY . .
RUN echo "===== STRATEGY DIR CONTENT =====" && ls -l strategy/

# 啟用即時 log 輸出
ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
