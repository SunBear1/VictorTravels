FROM base-python:dev as serve-stage

WORKDIR /gateway

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4", "--access-log", "--proxy-headers"]
