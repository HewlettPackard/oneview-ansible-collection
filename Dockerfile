FROM python:3.9-slim-buster

ARG http_proxy
ARG https_proxy
ARG no_proxy

ENV http_proxy=${http_proxy}
ENV https_proxy=${https_proxy}
ENV no_proxy=${no_proxy}

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /root

RUN apt-get update -y && \
    apt-get install --no-install-recommends -y vim curl git && \
    pip install --no-cache-dir \
        ansible \
        hpeOneView \
        hpICsp && \
    apt-get autoremove -y && apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /root/.cache/pip

RUN mkdir -p /etc/ansible && \
    echo -e "[localhost]\nlocalhost ansible_python_interpreter=python3 ansible_connection=local" > /etc/ansible/hosts

ADD . oneview-ansible-collection/
WORKDIR /root/oneview-ansible-collection

RUN ansible-galaxy collection build --force . && \
    ansible-galaxy collection install *.tar.gz

WORKDIR /root/.ansible/collections/ansible_collections/hpe/oneview

CMD ["ansible-playbook", "--version"]
