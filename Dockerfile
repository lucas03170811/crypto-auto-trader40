FROM python:3.11-slim

WORKDIR /app

# 安裝依賴
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    wget \
    git \
    && apt-get clean

# 安裝 ta-lib 的 wheel 版本（兼容 numpy）
RUN pip install --upgrade pip
RUN pip install numpy==1.23.5
RUN pip install ta-lib-bin

# 安裝其餘依賴
COPY requirements.txt .
RUN pip install -r requirements.txt

# 複製程式碼
COPY . .

ENV PYTHONUNBUFFERED=1
CMD ["python", "main.py"]
