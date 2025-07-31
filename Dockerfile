FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip \
 && pip uninstall -y numpy \
 && pip install numpy==1.24.4 \
 && pip install -r requirements.txt

CMD ["python", "main.py"]
