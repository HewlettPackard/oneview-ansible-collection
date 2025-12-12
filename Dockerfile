FROM python:3.9-slim-bullseye
LABEL maintainer="Chebrolu Harika <bala-sai-harika.chebrolu@hpe.com>"

WORKDIR /root

# Install dependencies + Ansible + OneView SDKs
RUN DEBIAN_FRONTEND=noninteractive apt-get update -y && \
    apt-get install --no-install-recommends -y vim curl git && \
    pip install --no-cache-dir ansible hpeOneView hpICsp && \
    apt-get autoremove -y && apt-get clean -y && \
    rm -rf /var/lib/apt/lists/* /tmp/* /root/.cache

# Configure Ansible local host
RUN mkdir -p /etc/ansible && \
    echo "[localhost]" >> /etc/ansible/hosts && \
    echo "localhost ansible_python_interpreter=python3 ansible_connection=local" >> /etc/ansible/hosts

# Copy repo into container
ADD . oneview-ansible-collection/
WORKDIR /root/oneview-ansible-collection

# Build & install the collection into the correct location
RUN ansible-galaxy collection build --force .

RUN mkdir -p /root/.ansible/collections && \
    ansible-galaxy collection install *.tar.gz -p /root/.ansible/collections

# Switch to installed collection directory (optional but harmless)
WORKDIR /root/.ansible/collections/ansible_collections/hpe/oneview

# Cleanup
RUN DEBIAN_FRONTEND=noninteractive apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/cache/apt/* /tmp/* /root/.cache

CMD ["ansible-playbook", "--version"]
