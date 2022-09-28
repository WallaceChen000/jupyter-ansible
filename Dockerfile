FROM phusion/baseimage:focal-1.1.0

MAINTAINER Wallace.Chen

ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8
ENV DEBIAN_FRONTEND noninteractive

EXPOSE 2222

# Install basic system
RUN apt-get update && apt-get install -y software-properties-common
RUN apt-get update && apt-get install -qq -y \
    cron \
    wget \
    curl \
    vim \
    python3-pip \
    iproute2

# Install docker 20.10
RUN curl https://releases.rancher.com/install-docker/20.10.sh | sh


# ssh enable
RUN dpkg-reconfigure openssh-server && echo 'root:SystemControl' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PermitRootLogin yes/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/#Port 22/Port 2223/' /etc/ssh/sshd_config && \
    rm -f /etc/service/sshd/down

# Install runservice.sh
#COPY ./runservice.sh /usr/local/bin/

#Install rke 1.3.12
RUN wget -O /usr/local/bin/rke https://github.com/rancher/rke/releases/download/v1.3.12/rke_linux-amd64 && chmod +x /usr/local/bin/rke;

#Install kubectl (the latest)
RUN wget -O /usr/local/bin/kubectl "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && chmod +x /usr/local/bin/kubectl; 


#Install helm (the latest)
RUN curl -fsSL -o /usr/local/bin/get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3; chmod +x /usr/local/bin/get_helm.sh; /usr/local/bin/get_helm.sh; 

#Install git
RUN apt-get update && apt-get install -qq -y \
        git

#Install notebook
RUN pip install notebook

#Install ansible
RUN pip install ansible

# Create RSA key pair & install public key to server
#RUN /usr/bin/ssh-keygen "-q -m PEM -t rsa -b 4096 -f /root/.ssh/id_rsa" <<<y <<<""; /bin/cat /root/.ssh/id_rsa.pub > /root/.ssh/authorized_keys; exit 0;
RUN /bin/mkdir -p /root/.ssh/; /usr/bin/ssh-keygen -q -m PEM -t rsa -b 4096 -f /root/.ssh/id_rsa; /bin/cat /root/.ssh/id_rsa.pub > /root/.ssh/authorized_keys;


# install usage cmd
#COPY ./rke.sh /root/

WORKDIR /root

# Set cron job


RUN mkdir -p /etc/service/runservice/ && \
    printf '#!/bin/sh\nset -e\n\nexec /usr/local/bin/runservice.sh\n' > /etc/service/runservice/run && \
    chmod a+x /etc/service/runservice/run

# Install rootfs
COPY ./rootfs.tar.gz /root/
RUN tar -xvf /root/rootfs.tar.gz -C / && rm -f /root/rootfs.tar.gz

# Use baseimage-docker's init system.
CMD ["/sbin/my_init"]

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

