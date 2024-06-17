FROM python:3.12-bullseye

WORKDIR /shell-random-coffee
COPY . .
RUN pip3 install -r requirements.txt
ENTRYPOINT python3 bot.py