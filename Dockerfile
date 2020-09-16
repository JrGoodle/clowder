############################################################
# Dockerfile for clowder project
############################################################
FROM python:3.8.5

# File Author / Maintainer
LABEL maintainer "Joe DeCapo <joe@polka.cat>"

############################################################

# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH
ENV PYTHONPATH $PYTHONPATH:/clowder

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

############################################################

VOLUME /clowder
COPY $HOME/.ssh /root/.ssh

############################################################

WORKDIR /clowder

############################################################

# Update package list
RUN apt-get update -y

# Install netstat and route
RUN apt-get install net-tools -y

# Install git
RUN apt-get install python-dev -y

# Install git-lfs
RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
RUN apt-get install git-lfs

# Set up git config
RUN git config --global user.email "joe@polka.cat"
RUN git config --global user.name "Clowder Docker"
RUN git config --global push.default simple
# RUN git config --global --unset url.ssh://git@github.com.insteadOf
RUN git config --system --unset-all filter.lfs.clean
RUN git config --system --unset-all filter.lfs.smudge
RUN git config --system --unset-all filter.lfs.process
RUN git config --system --unset-all filter.lfs.required

############################################################

CMD ["/usr/bin/env bash"]
