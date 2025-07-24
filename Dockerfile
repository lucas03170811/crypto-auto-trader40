FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y git
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONUNBUFFERED=1
CMD ["python", "main.py"]
# trigger rebuild - 2025-07-24
