#Dockerfile for a milter service
FROM centos:latest
MAINTAINER João Reis joao@7lan.net

#RUN dnf update -y
#RUN dnf groupinstall -y "Development Tools" && \
RUN dnf install -y epel-release && \
    dnf install -y python3-pymilter python3-pip && \
    rm -rf /var/cache/dnf/* && \
    dnf clean all && \
    mkdir -p /var/tmp/cache

COPY requirements.txt /
RUN pip install -r requirements.txt
COPY milter-template.py /

EXPOSE 8801/tcp
ENTRYPOINT ["/usr/bin/python3", "-u", "/milter-template.py"]
