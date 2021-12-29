# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
WORKDIR /
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN python3 -m textblob.download_corpora
COPY . .
RUN apt-get update && apt-get install -y cron
RUN apt-get install -y vim
COPY crawlcrontab /etc/cron.d/crawlcrontab
RUN chmod 0644 /etc/cron.d/crawlcrontab
RUN crontab /etc/cron.d/crawlcrontab
CMD ["python3", "run.py"]
