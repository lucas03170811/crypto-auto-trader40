FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN apt-get update && \
    apt-get install -y gcc build-essential && \
    pip install --upgrade pip && \
    pip uninstall -y numpy && \
    pip install --no-cache-dir numpy==1.24.4 && \
    pip install --no-cache-dir --force-reinstall -r requirements.txt

CMD ["python", "main.py"]
