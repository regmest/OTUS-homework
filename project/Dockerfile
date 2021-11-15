FROM python:3.7

WORKDIR /app

RUN pip install -U pip
RUN pip install setuptools wheel

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/