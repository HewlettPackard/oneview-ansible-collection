FROM python:3.9-slim-bullseye
LABEL maintainer="Chebrolu Harika <bala-sai-harika.chebrolu@hpe.com>"

WORKDIR /root

RUN DEBIAN_FRONTEND=noninteractive apt-get update -y && \
    apt-get install --no-install-recommends -y vim curl git && \
    pip install --no-cache-dir ansible hpeOneView hpICsp && \
    apt-get autoremove -y && apt-get clean -y && \
    rm -rf /var/lib/apt/lists/* /tmp/* /root/.cache

# ansible hosts config
RUN mkdir -p /etc/ansible && \
    echo "[localhost]" >> /etc/ansible/hosts && \
    echo "localhost ansible_python_interpreter=python3 ansible_connection=local" >> /etc/ansible/hosts

# COPY REPO FIRST
ADD . /root/oneview-ansible-collection/

WORKDIR /root/oneview-ansible-collection

# Build and install collection INTO ~/.ansible
RUN ansible-galaxy collection build --force . && \
    ansible-galaxy collection install hpe-oneview-*.tar.gz -p /root/.ansible/collections

WORKDIR /root/.ansible/collections/ansible_collections/hpe/oneview

RUN DEBIAN_FRONTEND=noninteractive apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/cache/apt/* /tmp/* /root/.cache

CMD ["ansible-playbook", "--version"]
