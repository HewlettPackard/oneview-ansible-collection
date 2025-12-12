FROM python:3.9-slim-bullseye
LABEL maintainer="Chebrolu Harika <bala-sai-harika.chebrolu@hpe.com>"

WORKDIR /root

RUN DEBIAN_FRONTEND=noninteractive apt-get update -y && \
    apt-get install --no-install-recommends -y vim curl && \
    pip install --no-cache-dir ansible hpeOneView hpICsp && \
    apt-get autoremove -y && apt-get clean -y && \
    rm -rf /var/lib/apt/lists/* /tmp/* /root/.cache

# Adding hosts for convenience
RUN mkdir -p /etc/ansible
RUN echo "[localhost]" >> /etc/ansible/hosts
RUN echo "localhost ansible_python_interpreter=python3 ansible_connection=local" >> /etc/ansible/hosts

ADD . oneview-ansible-collection/
WORKDIR /root/oneview-ansible-collection

# Build & install collection
RUN ansible-galaxy collection build --force .

RUN mkdir -p /root/.ansible/collections/ansible_collections && \
    ansible-galaxy collection install *.tar.gz -p /root/.ansible/collections/ansible_collections

WORKDIR /root/.ansible/collections/ansible_collections/hpe/oneview

# Cleanup
RUN DEBIAN_FRONTEND=noninteractive \
    apt-get autoremove -y && apt-get clean -y && \
    rm -rf /var/cache/apt/* /tmp/* /root/.cache

CMD ["ansible-playbook", "--version"]
