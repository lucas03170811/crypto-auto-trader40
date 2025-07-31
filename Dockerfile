FROM python:3.12-slim

WORKDIR /app

COPY . .

# 先升級 pip，再明確安裝 numpy 正確版本，最後再裝其餘依賴
RUN pip install --upgrade pip \
 && pip install numpy==1.24.4 \
 && pip install -r requirements.txt

CMD ["python", "main.py"]
