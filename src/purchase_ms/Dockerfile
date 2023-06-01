FROM base-python:dev as serve-stage

WORKDIR /purchases

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8002

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002", "--access-log", "--proxy-headers"]
