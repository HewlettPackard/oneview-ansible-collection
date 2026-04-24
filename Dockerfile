FROM python:3.9-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /root

# Install system dependencies
RUN apt-get update -y && \
    apt-get install --no-install-recommends -y \
        curl \
        git \
    && apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

# Install ansible explicitly
RUN pip install --no-cache-dir ansible

# Install project dependencies
COPY requirements.txt /root/requirements.txt
RUN pip install --no-cache-dir -r /root/requirements.txt

# Sanity check (fail fast)
RUN ansible --version && ansible-galaxy --version

# Setup localhost inventory
RUN mkdir -p /etc/ansible && \
    echo "[localhost]" > /etc/ansible/hosts && \
    echo "localhost ansible_connection=local ansible_python_interpreter=python3" >> /etc/ansible/hosts

# Copy repo content (no ansible.cfg anymore)
COPY galaxy.yml ./oneview-ansible-collection/
COPY roles ./oneview-ansible-collection/roles
COPY playbooks ./oneview-ansible-collection/playbooks
COPY plugins ./oneview-ansible-collection/plugins
COPY sdkAutomator ./oneview-ansible-collection/sdkAutomator
COPY auto_config.json ./oneview-ansible-collection/

WORKDIR /root/oneview-ansible-collection

# Build + install collection into default ansible path
RUN ansible-galaxy collection build --force . && \
    ansible-galaxy collection install *.tar.gz

CMD ["bash"]
