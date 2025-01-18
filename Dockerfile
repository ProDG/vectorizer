FROM python:3.13.1-slim

RUN pip install torch==2.5.1

WORKDIR /app

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
