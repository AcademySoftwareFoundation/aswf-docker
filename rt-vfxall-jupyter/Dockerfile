# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
ARG ASWF_ORG=aswftesting
ARG ASWF_PKG_ORG=aswftesting
ARG VFXPLATFORM_VERSION=2019
ARG ASWF_VERSION
ARG NB_USER=jovyan
ARG NB_UID=1000

FROM ${ASWF_ORG}/rt-vfxall:${VFXPLATFORM_VERSION}

LABEL maintainer="aloys.baillet@gmail.com"
LABEL com.vfxplatform.version=$VFXPLATFORM_VERSION
LABEL org.opencontainers.image.name="$ASWF_ORG/base-vfxall"
LABEL org.opencontainers.image.description="All VFX Packages CI Docker Image"
LABEL org.opencontainers.image.url="http://aswf.io/"
LABEL org.opencontainers.image.source="https://github.com/AcademySoftwareFoundation/aswf-docker"
LABEL org.opencontainers.image.vendor="AcademySoftwareFoundation"
LABEL org.opencontainers.image.version=$ASWF_VERSION

RUN pip install --no-cache-dir jupyterlab

ARG NB_USER
ARG NB_UID

RUN useradd -m -u ${NB_UID} ${NB_USER} && \
    su -c "echo '%${NB_USER} ALL=(ALL:ALL) NOPASSWD:ALL' >> /etc/sudoers"

ENV USER=${NB_USER} \
    NB_UID=${NB_UID} \
    HOME=/home/${NB_USER}

COPY rt-vfxall-jupyter/jupyter_notebook_config.py /etc/jupyter/

USER ${NB_USER}

RUN mkdir /home/${NB_USER}/work
WORKDIR /home/${NB_USER}/work

EXPOSE 8888

ENTRYPOINT [ "jupyter", "lab" ]
