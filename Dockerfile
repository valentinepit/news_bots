FROM python:3.8 as builder

RUN mkdir app
WORKDIR app

COPY ./requirements.txt ./
RUN python -m pip install -r requirements.txt

COPY . .
