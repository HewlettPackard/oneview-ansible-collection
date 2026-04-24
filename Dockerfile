FROM python:3.9-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /root

# Install minimal system deps
RUN apt-get update -y && \
    apt-get install --no-install-recommends -y \
        curl \
        git \
    && apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

# Copy EXACT requirements file (important)
COPY requirements.txt /root/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /root/requirements.txt

# Verify ansible exists (fail fast if broken)
RUN ansible --version && ansible-galaxy --version

# Setup ansible localhost
RUN mkdir -p /etc/ansible && \
    echo "[localhost]" > /etc/ansible/hosts && \
    echo "localhost ansible_connection=local ansible_python_interpreter=python3" >> /etc/ansible/hosts

# Copy only required repo content
COPY ansible.cfg ./oneview-ansible-collection/
COPY galaxy.yml ./oneview-ansible-collection/
COPY roles ./oneview-ansible-collection/roles
COPY playbooks ./oneview-ansible-collection/playbooks
COPY plugins ./oneview-ansible-collection/plugins
COPY sdkAutomator ./oneview-ansible-collection/sdkAutomator
COPY auto_config.json ./oneview-ansible-collection/

WORKDIR /root/oneview-ansible-collection

# Build + install collection locally
RUN ansible-galaxy collection build --force . && \
    ansible-galaxy collection install *.tar.gz -p ./ansible_collections

CMD ["bash"]
