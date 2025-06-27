FROM python:3.9-slim

ARG http_proxy
ARG https_proxy
ARG no_proxy

ENV http_proxy=${http_proxy}
ENV https_proxy=${https_proxy}
ENV no_proxy=${no_proxy}


ENV DEBIAN_FRONTEND=noninteractive


RUN apt-get update -y && \
    apt-get install --no-install-recommends -y \
    vim \
    curl \
    git && \
    pip install --no-cache-dir ansible hpeOneView hpICsp && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

CMD [ "bash" ]
