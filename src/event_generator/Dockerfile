FROM base-python:dev as serve-stage

WORKDIR /event_generator

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8006", "--access-log", "--proxy-headers"]
