FROM rockylinux:9
LABEL maintainer="Chebrolu Harika <bala-sai-harika.chebrolu@hpe.com>"

WORKDIR /root

# RockyLinux 9.4+ ships OpenSSL 3.2.2, which supports PQC hybrid key exchange
# once the OQS provider is installed and active (PQC checklist Section 1.1).
RUN dnf install -y vim curl python3 python3-pip oqsprovider && \
    pip3 install --no-cache-dir ansible hpeOneView hpICsp && \
    dnf clean all && rm -rf /var/cache/dnf

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
RUN dnf clean all && rm -rf /var/cache/dnf /tmp/* /root/cache/.
 
CMD ["ansible-playbook", "--version"]
