FROM python:3.10.7

WORKDIR /usr/src/stripe_api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/stripe_api/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/stripe_api