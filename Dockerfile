FROM python:3.9-slim-bullseye

LABEL maintainer="Chebrolu Harika <bala-sai-harika.chebrolu@hpe.com>"

WORKDIR /root

# Install system dependencies
RUN DEBIAN_FRONTEND=noninteractive apt-get update -y && \
    apt-get install --no-install-recommends -y vim curl && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching)
COPY requirements.txt .

# Install Python dependencies (INCLUDING ansible)
RUN pip install --no-cache-dir -r requirements.txt

# 🔥 Ensure ansible-galaxy is available
RUN ansible --version && ansible-galaxy --version

# Setup Ansible hosts
RUN mkdir -p /etc/ansible && \
    echo "[localhost]" >> /etc/ansible/hosts && \
    echo "localhost ansible_python_interpreter=python3 ansible_connection=local" >> /etc/ansible/hosts

# Copy project
COPY . oneview-ansible-collection/

WORKDIR /root/oneview-ansible-collection

# Build and install collection
RUN ansible-galaxy collection build --force . && \
    ansible-galaxy collection install *.tar.gz

WORKDIR /root/.ansible/collections/ansible_collections/hpe/oneview

# Cleanup
RUN apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/cache/apt/archives/* /tmp/* /root/.cache

CMD ["ansible-playbook", "--version"]
