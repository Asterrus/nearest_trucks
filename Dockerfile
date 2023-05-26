FROM python:3.11.1-alpine

WORKDIR /web

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

EXPOSE 8000
