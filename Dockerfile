FROM python:3.6

MAINTAINER Dmitriy Salman

RUN apt-get -y update
RUN pip install uvloop

RUN  mkdir -p /home/server
COPY . /home/server

WORKDIR /home/server

EXPOSE 80
CMD python3 main.py