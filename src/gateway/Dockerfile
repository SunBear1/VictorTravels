FROM python:3.11.2-alpine as build-stage

WORKDIR /gateway

RUN pip install --upgrade pip

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4", "--access-log", "--proxy-headers"]
