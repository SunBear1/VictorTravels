FROM base-python:dev as serve-stage

WORKDIR /transports

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "main.py"]
