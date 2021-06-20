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

# Prepare xpra folder for new user
RUN mkdir -p /run/user/${NB_UID}/xpra && \
    mkdir -p /run/xpra && \
    chown ${NB_USER}:${NB_USER} /run/user/${NB_UID}/xpra && \
    chown ${NB_USER}:${NB_USER} /run/xpra && \
    chown ${NB_USER}:${NB_USER} /etc/xpra/ssl-cert.pem

USER ${NB_USER}

RUN mkdir /home/${NB_USER}/work
WORKDIR /home/${NB_USER}/work

COPY rt-vfxall-jupyter/jupyter-entry-point.sh /usr/local/bin/

EXPOSE 8888

ENV ASWF_XPRA_COMMAND=/usr/local/bin/jupyter-entry-point.sh

#ENTRYPOINT [ "/usr/local/bin/xpra-entry-point.sh" ]
