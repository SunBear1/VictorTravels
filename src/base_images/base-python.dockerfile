FROM python:3.11.2-alpine as build-stage

WORKDIR /base-python

RUN pip install --upgrade pip

RUN apk --no-cache add curl
