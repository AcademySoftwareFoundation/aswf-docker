FROM aswfstaging/ci-base:2019

COPY scripts/* /tmp/

RUN /tmp/install_openexr.sh 2.3.0 && \
    /tmp/install_oiio.sh 2.0.8
