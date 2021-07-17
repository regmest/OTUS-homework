FROM python:3.9.5-buster

WORKDIR /app

RUN pip install -U pip setuptools

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./my_app .

ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]

# docker build . -t my_app
# docker run -p 5000:5000 my_app