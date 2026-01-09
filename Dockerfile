FROM python:3.9-slim-bullseye
LABEL maintainer="Chebrolu Harika <bala-sai-harika.chebrolu@hpe.com>"

# Work directory
WORKDIR /root

# Install base packages + ansible + required SDKs
RUN DEBIAN_FRONTEND=noninteractive apt-get update -y && \
    apt-get install --no-install-recommends -y vim curl git && \
    pip install --no-cache-dir ansible hpeOneView hpICsp && \
    apt-get autoremove -y && apt-get clean -y && \
    rm -rf /var/lib/apt/lists/* /tmp/* /root/.cache

# ansible hosts config
RUN mkdir -p /etc/ansible && \
    echo "[localhost]" >> /etc/ansible/hosts && \
    echo "localhost ansible_python_interpreter=python3 ansible_connection=local" >> /etc/ansible/hosts

# Copy repository into container
ADD . /root/oneview-ansible-collection/

# Move into repo
WORKDIR /root/oneview-ansible-collection

# Install Python dependencies for sdkAutomator
RUN pip3 install -r requirements.txt

# Build and install the Ansible collection *into ~/.ansible*
RUN ansible-galaxy collection build --force . && \
    ansible-galaxy collection install hpe-oneview-*.tar.gz -p /root/.ansible/collections

# Switch into installed collection (sdkAutomator will expect this path)
WORKDIR /root/.ansible/collections/ansible_collections/hpe/oneview

# Cleanup
RUN DEBIAN_FRONTEND=noninteractive apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/cache/apt/* /tmp/* /root/.cache

CMD ["ansible-playbook", "--version"]
