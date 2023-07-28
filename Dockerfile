FROM python:3.11-slim

MAINTAINER Dmitry P. <turgenevski@yandex.ru>

WORKDIR /app

COPY . .

RUN pip3 install --upgrade pip

RUN pip3 install -r /app/requirements.txt --no-cache-dir


CMD ["python3", "app.py", "0:5050" ]

LABEL  version=1.1
