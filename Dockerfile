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
VOLUME /root/.ssh

############################################################

WORKDIR /clowder

############################################################

# Install GIT
RUN apt-get update -y && apt-get install python-dev -y

############################################################

CMD ["/usr/bin/env bash"]
