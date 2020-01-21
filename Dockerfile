FROM python:3.6.8

WORKDIR /

RUN apt-get update -q && apt-get install -yq netcat
RUN apt-get update && apt-get -y install protobuf-compiler libprotobuf-dev cmake

RUN cd open-babel && mkdir build && cd build
RUN cmake ../openbabel
RUN make && make install

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
