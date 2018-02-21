FROM            smetj/wishbone:develop
MAINTAINER      Jelle Smet
ARG             branch
RUN             LC_ALL=en_US.UTF-8 /usr/bin/pip3 install --process-dependency-link https://github.com/smetj/wishbone-input-httpserver/archive/$branch.zip
