FROM ubuntu:24.04
LABEL maintainer="Chebrolu Harika <bala-sai-harika.chebrolu@hpe.com>"

WORKDIR /root

# Ubuntu 24.04 ships OpenSSL 3.5, which natively supports PQC hybrid key
# exchange (ML-KEM) without requiring the OQS provider (PQC checklist Section 1.1).
RUN DEBIAN_FRONTEND=noninteractive apt-get update -y && \
    apt-get install --no-install-recommends -y vim curl python3 python3-pip python3-venv && \
    # pip install --no-cache-dir ansible hpeOneView hpICsp && \
    # pip install --no-cache-dir --break-system-packages ansible "hpeOneView>=12.0.0" && \
    pip install --no-cache-dir --break-system-packages ansible hpeOneView hpICsp && \
    apt-get autoremove -y && apt-get clean -y && \
    rm -rf /var/lib/apt/lists/* /tmp/* /root/.cache

# Adding hosts for convenience
RUN mkdir -p /etc/ansible
RUN echo [localhost] >> /etc/ansible/hosts
RUN echo localhost ansible_python_interpreter=python3 ansible_connection=local >> /etc/ansible/hosts
ADD . oneview-ansible-collection/
WORKDIR /root/oneview-ansible-collection

# Building and Installing hpe.oneview collection
RUN ansible-galaxy collection build --force .
RUN ansible-galaxy collection install *.tar.gz
WORKDIR /root/.ansible/collections/ansible_collections/hpe/oneview

# Clean and remove not required packages
RUN DEBAIN_FRONTEND=noninteractive \
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/cache/apt/archives/* /var/cache/apt/lists* /tmp/* /root/cache/.
 
CMD ["ansible-playbook", "--version"]
