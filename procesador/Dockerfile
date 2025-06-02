FROM openjdk:8-jdk-slim

ENV PIG_VERSION=0.17.0

WORKDIR /app

RUN apt-get update && \
    apt-get install -y wget tar python && \
    rm -rf /var/lib/apt/lists/*

RUN wget https://downloads.apache.org/pig/pig-${PIG_VERSION}/pig-${PIG_VERSION}.tar.gz && \
    tar -xzf pig-${PIG_VERSION}.tar.gz && \
    mv pig-${PIG_VERSION} /opt/pig && \
    rm pig-${PIG_VERSION}.tar.gz

ENV PATH="/opt/pig/bin:$PATH"

COPY . .

CMD ["bash"]

RUN useradd -ms /bin/bash piguser
USER piguser