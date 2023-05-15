FROM base-python:dev as serve-stage

WORKDIR /payments

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8003

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003", "--workers", "2", "--access-log", "--proxy-headers"]
