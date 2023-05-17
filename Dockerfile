FROM ubuntu:20.04
MAINTAINER hancyber<hancyber75@gmail.com>

ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV TZ=Asia/Seoul

RUN apt update && apt install -y sudo
RUN useradd -rm -d /home/hgb -s /bin/bash -g root -G sudo -u 1001 hgb
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER hgb
WORKDIR /home/hgb

RUN sudo apt update && sudo apt install -y openjdk-8-jdk curl
RUN curl --create-dirs -o ~/.embulk/bin/embulk -L "https://dl.embulk.org/embulk-latest.jar"
RUN chmod +x ~/.embulk/bin/embulk
ENV PATH /home/hgb/.embulk/bin:$PATH

RUN embulk gem install embulk-input-mysql
RUN embulk gem install representable -v 3.0.4 \
&& embulk gem install google-cloud-env -v 1.2.1 \
&& embulk gem install google-cloud-core -v 1.3.0 \
&& embulk gem install embulk-input-bigquery
RUN embulk gem install embulk-output-s3
RUN embulk gem install embulk-input-azure_blob_storage
RUN embulk gem install embulk-input-postgresql
RUN embulk gem install embulk-input-oracle
RUN embulk gem install embulk-input-sqlserver
RUN embulk gem install embulk-input-bigquery

RUN sudo apt install -y \
make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget llvm libncurses5-dev \
libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev git

RUN git clone https://github.com/pyenv/pyenv.git ~/.pyenv
ENV PYENV_ROOT /home/hgb/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH
RUN pyenv install 3.9.5 && pyenv global 3.9.5

COPY package-relay /home/hgb/package-relay
RUN sudo chmod u+x /home/hgb/package-relay/setup_relay.sh
RUN /bin/bash /home/hgb/package-relay/setup_relay.sh

COPY package-redis /home/hgb/package-redis
RUN sudo chmod u+x /home/hgb/package-redis/setup_redis.sh
RUN /bin/bash /home/hgb/package-redis/setup_redis.sh

COPY src/openopsdata /home/hgb/openopsdata
COPY src/main.py /home/hgb/main.py
COPY requirements.txt /home/hgb/requirements.txt
RUN pip install -r requirements.txt
COPY template /home/hgb/template
COPY bin /home/hgb/bin

RUN sudo apt update && sudo apt install -y unattended-upgrades
RUN sudo unattended-upgrade
RUN sudo apt-get clean && sudo rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY lib /home/hgb/lib

ENV APITEST_PORT 8000
COPY apitest /home/hgb/apitest
COPY apitest.sh /home/hgb/apitest.sh

COPY tls /etc/tls
COPY conf.d /home/hgb/conf.d

ENV CONF_FILE /home/hgb/conf.d/config.conf
COPY entrypoint.sh /home/hgb/entrypoint.sh

RUN sudo chown -R hgb /home/hgb
RUN sudo chmod u+x /home/hgb/bin/*
RUN sudo chmod u+x /home/hgb/apitest.sh
RUN sudo chmod u+x /home/hgb/entrypoint.sh

ENTRYPOINT /home/hgb/entrypoint.sh $CONF_FILE
