FROM python:3.10.13

WORKDIR /crud_database

COPY app.py .
COPY requirements.txt .

RUN pip install -r requirements.txt