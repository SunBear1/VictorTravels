FROM base-python:dev as serve-stage

WORKDIR /reservations

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "3", "--access-log", "--proxy-headers"]
