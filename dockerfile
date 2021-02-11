FROM python:3.9-alpine

RUN mkdir -p /odt/app

COPY . /odt/app

WORKDIR /odt/app

RUN apk add --no-cache \
        libressl-dev \
        musl-dev \
        libffi-dev \
        gcc \
        python3-dev \
        openssl-dev && \
    pip install pipenv

RUN pipenv install

RUN apk del \
        libressl-dev \
        musl-dev \
        libffi-dev \
        gcc \
        python3-dev \
        openssl-dev

ENTRYPOINT pipenv run moodtracker/__main__.py
