FROM python:3.11.2-alpine as build-stage

WORKDIR /data-init

RUN apk update && apk add --no-cache mariadb-dev gcc musl-dev libpq-dev

RUN pip install --upgrade pip

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "main.py"]