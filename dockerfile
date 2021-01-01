FROM python:3.9

RUN mkdir -p /odt/app
RUN pip install pipenv

COPY . /odt/app

WORKDIR /odt/app

RUN pipenv install

ENTRYPOINT pipenv run moodtracker/bot.py
