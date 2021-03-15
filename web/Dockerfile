FROM python:3.6.8

WORKDIR /

RUN apt-get update -q
RUN apt-get -yq install tcsh make \
               gcc gfortran \
               bc xorg-dev libbz2-dev wget \
               protobuf-compiler libprotobuf-dev build-essential swig libboost-all-dev libeigen3-dev netcat
RUN pip install --upgrade pip cmake

ADD https://github.com/openbabel/openbabel/archive/openbabel-2-4-1.tar.gz /
RUN tar xvzf /openbabel-2-4-1.tar.gz -C /
RUN rm -r /openbabel-2-4-1.tar.gz

WORKDIR /openbabel-openbabel-2-4-1
RUN mkdir build && cd build && cmake .. && make -j4 && make install

WORKDIR /web
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
