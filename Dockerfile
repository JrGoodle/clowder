############################################################
# Dockerfile for clowder project
# Based on python:3.4.7-wheezy
############################################################
FROM python:3.4.7-wheezy

# File Author / Maintainer
LABEL maintainer "John Lane <john.lane93@gmail.com>"

############################################################

# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

############################################################

ADD . /src

############################################################

# Install GIT
RUN apt-get update -y && apt-get install python-dev -y

############################################################

WORKDIR /src
RUN pip install -e .
CMD ["/bin/bash"]
