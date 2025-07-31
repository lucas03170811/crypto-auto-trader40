FROM python:3.12-slim

WORKDIR /app
COPY . .

# 清除 pip 快取與 numpy 舊版本，強制指定正確版本
RUN apt-get update && \
    apt-get install -y gcc build-essential && \
    pip install --upgrade pip setuptools wheel && \
    pip uninstall -y numpy pandas pandas-ta || true && \
    pip cache purge && \
    pip install numpy==1.24.4 && \
    pip install pandas==1.5.3 && \
    pip install pandas-ta==0.3.14b0 && \
    pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
