FROM python:3.12-slim

WORKDIR /app

COPY . .

# 先安裝 numpy 相容版本，才能讓 pandas-ta 安裝成功
RUN pip install --upgrade pip \
 && pip install numpy==1.23.5 \
 && pip install -r requirements.txt

CMD ["python", "main.py"]
