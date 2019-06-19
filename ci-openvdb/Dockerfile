FROM aswfstaging/ci-base:2019

COPY scripts/* /tmp/

RUN /tmp/install_openexr.sh 2.3.0 && \
    /tmp/install_log4cplus.sh 1.1.2 && \
    /tmp/install_glfw.sh 3.0.4 && \
    /tmp/install_blosc.sh 1.5.0
