FROM python:3.9-slim-bullseye
LABEL maintainer="Chebrolu Harika <bala-sai-harika.chebrolu@hpe.com>"

# Set working directory
WORKDIR /root

# Install system packages and Python packages
RUN DEBIAN_FRONTEND=noninteractive \
    apt-get update -y && \
    apt-get install --no-install-recommends -y vim curl git && \
    pip install --no-cache-dir ansible hpeOneView hpICsp && \
    apt-get autoremove -y && apt-get clean -y && \
    rm -rf /var/lib/apt/lists/* /tmp/* /root/.cache

# Configure Ansible for localhost execution
RUN mkdir -p /etc/ansible && \
    echo "[localhost]" >> /etc/ansible/hosts && \
    echo "localhost ansible_python_interpreter=python3 ansible_connection=local" >> /etc/ansible/hosts

# Add the OneView Ansible Collection source code to the image
ADD . oneview-ansible-collection/
WORKDIR /root/oneview-ansible-collection

# Install collection dependencies
RUN pip3 install -r requirements.txt

# Build the collection
RUN ansible-galaxy collection build --force .

# Install the collection into the correct Ansible default path
RUN mkdir -p /root/.ansible/collections && \
    ansible-galaxy collection install hpe-oneview-*.tar.gz -p /root/.ansible/collections

# Switch to the installed collection directory
WORKDIR /root/.ansible/collections/ansible_collections/hpe/oneview

# Cleanup
RUN DEBIAN_FRONTEND=noninteractive \
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/cache/apt/* /tmp/* /root/.cache

# Default command
CMD ["ansible-playbook", "--version"]
