FROM python:3.7-slim-buster
LABEL maintainer "Chebrolu Harika <bala-sai-harika.chebrolu@hpe.com>"
WORKDIR /root
RUN DEBAIN_FRONTEND=noninteractive \
    apt-get update -y \
    && apt-get install --no-install-recommends -y \
    vim \
    curl \
    && pip install ansible hpeOneView hpICsp
RUN mkdir -p /etc/ansible
RUN echo [localhost] >> /etc/ansible/hosts
RUN echo localhost ansible_python_interpreter=python3 ansible_connection=local >> /etc/ansible/hosts
ADD . oneview-ansible-collection/
WORKDIR /root/oneview-ansible-collection
RUN DEBAIN_FRONTEND=noninteractive \
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/cache/apt/archives/* /var/cache/apt/lists* /tmp/* /root/cache/.
CMD ["ansible-playbook", "--version"]
