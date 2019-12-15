FROM python:3.6.8

WORKDIR /

RUN apt-get update -q && apt-get install -yq netcat && apt-get install -yq python-openbabel

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
