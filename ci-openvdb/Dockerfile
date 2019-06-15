FROM aswfstaging/ci-base:2019

COPY scripts/* /tmp/

RUN /tmp/install_boost.sh 1.66.0 && \
    /tmp/install_tbb.sh 2018 && \
    /tmp/install_openexr.sh 2.3.0 && \
    /tmp/install_log4cplus.sh 2.0.4 && \
    /tmp/install_glfw.sh 3.3 && \
    /tmp/install_blosc.sh 1.5.0
