FROM python:3.9-slim-bullseye
LABEL maintainer="Chebrolu Harika <bala-sai-harika.chebrolu@hpe.com>"

WORKDIR /root

RUN DEBIAN_FRONTEND=noninteractive apt-get update -y && \
    apt-get install --no-install-recommends -y vim curl && \
    pip install --no-cache-dir ansible hpeOneView hpICsp && \
    apt-get autoremove -y && apt-get clean -y && \
    rm -rf /var/lib/apt/lists/* /tmp/* /root/.cache

# Adding hosts
RUN mkdir -p /etc/ansible
RUN echo "[localhost]" >> /etc/ansible/hosts
RUN echo "localhost ansible_python_interpreter=python3 ansible_connection=local" >> /etc/ansible/hosts

# Copy repo
ADD . oneview-ansible-collection/
WORKDIR /root/oneview-ansible-collection

# 🔥 IMPORTANT: Install all required python modules for sdkAutomator
RUN pip install --no-cache-dir -r requirements.txt

# Build and install collection
RUN ansible-galaxy collection build --force .
RUN ansible-galaxy collection install *.tar.gz

WORKDIR /root/.ansible/collections/ansible_collections/hpe/oneview

# Cleanup
RUN DEBIAN_FRONTEND=noninteractive \
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/cache/apt/archives/* /var/cache/apt/lists* /tmp/* /root/cache/.

# Keep container alive for sdkAutomator
CMD ["bash"]
