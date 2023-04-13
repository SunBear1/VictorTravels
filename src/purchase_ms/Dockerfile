FROM python:3.11.2-alpine as build-stage

WORKDIR /purchases

RUN pip install --upgrade pip

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8002

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002", "--workers", "2", "--access-log", "--proxy-headers"]
