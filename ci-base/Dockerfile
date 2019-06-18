FROM centos/devtoolset-6-toolchain-centos7
LABEL com.vfxplatform.version="CY2019"

USER root

RUN yum install -y \
    bzip2-devel \
    file \
    make \
    which \
    zlib-devel \
    git \
    ca-certificates \
    sudo \
    openssl-devel \
    libxcb libxcb-devel \
    libXrender libXrender-devel \
    xcb-util-wm xcb-util-wm-devel \
    xcb-util xcb-util-devel \
    xcb-util-image xcb-util-image-devel \
    xcb-util-keysyms xcb-util-keysyms-devel \
    pulseaudio-libs-devel \
    gperf \
    ruby \
    libcap-devel \
    libXtst-devel \
    pciutils-devel \
    bison \
    libv4l libv4l-devel \
    libcap-devel \
    mesa-libGL-devel \
    mesa-libEGL-devel \
    libxml2 libxml2-devel \
    libxslt libxslt-devel \
    nss nss-devel \
    dbus dbus-devel \
    fontconfig fontconfig-devel \
    freetype freetype-devel \
    ncurses ncurses-devel \
    readline readline-devel \
    libpng libpng-devel \
    libjpeg libjpeg-devel \
    libXrandr libXrandr-devel \
    libXcomposite libXcomposite-devel \
    libXScrnSaver libXScrnSaver-devel \
    libXcursor libXcursor-devel \
    libXp libXp-devel \
    libXpm libXpm-devel \
    libXmu libXmu-devel \
    libXi libXi-devel \
    glut-devel \
    pulseaudio-libs pulseaudio-libs-devel \
    alsa-lib alsa-lib-devel \
    libtiff libtiff-devel \
    tcsh \
    fam \
    wget \
    patch \
    csh \
    java-1.8.0-openjdk \
    doxygen \
    pkgconfig \
    automake autoconf \
    && \
    yum clean all

# Install base build toolset
COPY scripts/install_ninja.sh \
     scripts/install_cmake.sh \
     scripts/install_clang.sh \
     scripts/install_sonar.sh \
     /tmp/

RUN /tmp/install_ninja.sh 1.9.0 && \
    /tmp/install_cmake.sh 3.11.4 && \
    /tmp/install_clang.sh 7.0.1 && \
    /tmp/install_sonar.sh 3.3.0.1492

ENV PYTHON_VERSION=2.7 \
    PYTHON_VERSION_FULL=2.7.15 \
    PYTHONPATH=/usr/local/lib/python${PYTHON_VERSION}/site-packages:${PYTHONPATH} \
    LD_LIBRARY_PATH=/usr/local/lib:/usr/local/lib64:${LD_LIBRARY_PATH}

COPY scripts/install_python.sh /tmp/
RUN /tmp/install_python.sh ${PYTHON_VERSION_FULL}

# Install most common dependencies
COPY scripts/install_boost.sh \
     scripts/install_tbb.sh \
     scripts/install_numpy.sh \
     scripts/install_cppunit.sh \
     scripts/install_glew.sh \
     /tmp/

RUN /tmp/install_boost.sh 1.66.0 && \
    /tmp/install_tbb.sh 2018 && \
    /tmp/install_numpy.sh 1.14 && \
    /tmp/install_cppunit.sh 1.14.0 && \
    /tmp/install_glew.sh 2.1.0
