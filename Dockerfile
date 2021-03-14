FROM python:3.9.2-slim-buster

RUN apt-get update && apt-get install apt-utils -y && apt-get install gcc -y

RUN mkdir -p /app/api
WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY api /app/api
