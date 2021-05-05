FROM python:3.7-slim-buster
LABEL maintainer "Chebrolu Harika <bala-sai-harika.chebrolu@hpe.com>"
WORKDIR /root

# Some optional but recommended packages
RUN DEBAIN_FRONTEND=noninteractive \
    apt-get update -y \
    && apt-get install --no-install-recommends -y \
    vim \
    curl \
    && pip install ansible hpeOneView hpICsp

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
