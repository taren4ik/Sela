FROM python:3.11-slim

RUN mkdir /app

COPY . .

RUN pip3 install -r /app/requirements.txt --no-cache-dir

WORKDIR /app
CMD ["python3, "app.py" ]

LABEL author='D turgenevski@yandex.ru' version=1.0