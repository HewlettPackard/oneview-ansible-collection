FROM python:3.9-slim-bullseye
LABEL maintainer="Chebrolu Harika <bala-sai-harika.chebrolu@hpe.com>"

# ----------------------------------------------------
# System dependencies + pip deps required by Ansible and sdkAutomator
# ----------------------------------------------------
RUN DEBIAN_FRONTEND=noninteractive apt-get update -y && \
    apt-get install --no-install-recommends -y \
        vim curl git && \
    pip install --no-cache-dir \
        ansible \
        hpeOneView \
        hpICsp \
        gitpython \
        requests \
        pyvmomi \
        docker \
        beautifulsoup4 \
        jmespath && \
    apt-get autoremove -y && apt-get clean -y && \
    rm -rf /var/lib/apt/lists/* /tmp/* /root/.cache

# ----------------------------------------------------
# Configure Ansible localhost
# ----------------------------------------------------
RUN mkdir -p /etc/ansible && \
    echo "[localhost]" >> /etc/ansible/hosts && \
    echo "localhost ansible_connection=local ansible_python_interpreter=/usr/bin/python3" >> /etc/ansible/hosts

# ----------------------------------------------------
# Copy the entire repo into container
# ----------------------------------------------------
WORKDIR /root
ADD . /root/oneview-ansible-collection/

WORKDIR /root/oneview-ansible-collection

# ----------------------------------------------------
# Install requirements.txt for sdkAutomator
# ----------------------------------------------------
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# ----------------------------------------------------
# Build & Install Ansible Collection into the CORRECT PATH
# ----------------------------------------------------
RUN ansible-galaxy collection build --force . && \
    mkdir -p /root/.ansible/collections && \
    ansible-galaxy collection install hpe-oneview-*.tar.gz -p /root/.ansible/collections

# ----------------------------------------------------
# Switch to installed Ansible Collection directory
# sdkAutomator will run from here
# ----------------------------------------------------
WORKDIR /root/.ansible/collections/ansible_collections/hpe/oneview

# ----------------------------------------------------
# Clean final unnecessary cache
# ----------------------------------------------------
RUN DEBIAN_FRONTEND=noninteractive apt-get autoremove -y && apt-get clean -y && \
    rm -rf /var/cache/apt/* /tmp/* /root/.cache

CMD ["ansible-playbook", "--version"]
