# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
WORKDIR /
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN python3 -m textblob.download_corpora
COPY . .
CMD ["python3", "run.py"]
