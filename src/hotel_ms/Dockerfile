FROM python:3.11.2-alpine as build-stage

WORKDIR /hotels

RUN pip install --upgrade pip

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "main.py"]
