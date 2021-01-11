FROM python:3.8

EXPOSE 5000

ADD requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
ADD . /app