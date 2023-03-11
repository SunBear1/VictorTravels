FROM python:3.11.2-alpine as build-stage

WORKDIR /user-handler

COPY . .

RUN apk update && apk add --no-cache mariadb-dev gcc musl-dev libpq-dev

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--access-log", "--proxy-headers"]
