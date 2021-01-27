FROM ubuntu:18.04

# USER root

# set LANG
RUN apt-get update && apt-get -y install locales
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8  

WORKDIR /home
COPY . hicbin

RUN cp /home/hicbin/hicbin.sh /usr/local/bin && \
    chmod +x /usr/local/bin/hicbin.sh

# get python, java, hmmer
RUN apt-get install -y --no-install-recommends \
    python-dev  \
    build-essential libssl-dev libffi-dev \
    libxml2-dev libxslt1-dev zlib1g-dev \
    python-pip \
    default-jdk \
    python3 \
    python3-pip \
    git \
    hmmer \
    wget \
    unzip \
    ca-certificates \
    && update-ca-certificates \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# checkm
WORKDIR /home
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools	
RUN pip3 install -r hicbin/requirementspy3.txt
RUN pip3 install checkm-genome --upgrade --no-deps

# Prodigal
WORKDIR /home/checkmrequire
RUN git clone https://github.com/hyattpd/Prodigal.git && \
    cd Prodigal && \
    make install 

# pplacer
WORKDIR /home/checkmrequire
RUN wget https://github.com/matsen/pplacer/releases/download/v1.1.alpha19/pplacer-linux-v1.1.alpha19.zip && \
    unzip pplacer-linux-v1.1.alpha19.zip && \
    cd pplacer-Linux-v1.1.alpha19 && \
    cp guppy pplacer rppr /usr/local/bin/

# checkm data
RUN mkdir checkmdata && cd checkmdata && \
    wget https://data.ace.uq.edu.au/public/CheckM_databases/checkm_data_2015_01_16.tar.gz && \
    tar xzf checkm_data_2015_01_16.tar.gz && \
    checkm data setRoot /home/checkmrequire/checkmdata
    
# pip install requirements for bin3C
WORKDIR /home
RUN python -m pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r hicbin/requirements.txt


# get bin3C
RUN git clone https://github.com/cerebis/bin3C.git && \
    cp -r /home/hicbin/* /home/bin3C/ 
