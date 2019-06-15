FROM aswfstaging/aswf-vfx-base:2019

COPY scripts/* /tmp/

RUN /tmp/install_boost.sh 1.66.0 && \
    /tmp/install_tbb.sh 2018 && \
    /tmp/install_openexr.sh 2.3.0 && \
    /tmp/install_blosc.sh 1.5.0
