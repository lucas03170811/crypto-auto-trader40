FROM python:3.11-slim

WORKDIR /app

# 安裝系統依賴 + setuptools 解決 pip build_meta 問題
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    python3-setuptools \
    wget \
    git \
    && apt-get clean

# 升級 pip + 安裝 numpy（與 ta-lib 相容版本）
RUN pip install --upgrade pip
RUN pip install numpy==1.23.5

# 安裝 ta-lib 二進位套件
RUN pip install ta-lib-bin

# 安裝其餘依賴
COPY requirements.txt .
RUN echo "======= REQUIREMENTS CONTENT =======" && cat requirements.txt
RUN pip install -r requirements.txt

# 複製程式碼
COPY . .
RUN echo "===== STRATEGY DIR CONTENT =====" && ls -l strategy/

ENV PYTHONUNBUFFERED=1
CMD ["python", "main.py"]
