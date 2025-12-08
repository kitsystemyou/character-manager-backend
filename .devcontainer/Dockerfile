FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

# Install Python and required dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
        python3.12 \
        python3-pip \
        python3-venv \
        default-libmysqlclient-dev \
        build-essential \
        pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create symlinks for python and pip
RUN ln -s /usr/bin/python3.12 /usr/bin/python \
    && ln -s /usr/bin/pip3 /usr/bin/pip
