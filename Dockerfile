FROM python:3.9-slim-bullseye

LABEL maintainer="HPE SDK Automation"

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /root

# Install minimal dependencies
RUN apt-get update -y && \
    apt-get install --no-install-recommends -y \
        curl \
        git \
    && pip install --no-cache-dir \
        ansible \
        hpeOneView \
        hpICsp \
    && apt-get clean -y && \
    rm -rf /var/lib/apt/lists/* /tmp/* /root/.cache

# Setup ansible localhost
RUN mkdir -p /etc/ansible && \
    echo "[localhost]" > /etc/ansible/hosts && \
    echo "localhost ansible_connection=local ansible_python_interpreter=python3" >> /etc/ansible/hosts

# Copy ONLY required files (critical for speed)
COPY ansible.cfg ./oneview-ansible-collection/
COPY galaxy.yml ./oneview-ansible-collection/
COPY roles ./oneview-ansible-collection/roles
COPY playbooks ./oneview-ansible-collection/playbooks
COPY plugins ./oneview-ansible-collection/plugins
COPY sdkAutomator ./oneview-ansible-collection/sdkAutomator
COPY auto_config.json ./oneview-ansible-collection/

WORKDIR /root/oneview-ansible-collection

# Build and install collection locally
RUN ansible-galaxy collection build --force . && \
    ansible-galaxy collection install *.tar.gz -p ./ansible_collections

# Final working directory (important fix)
WORKDIR /root/oneview-ansible-collection

CMD ["bash"]
