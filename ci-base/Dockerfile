FROM centos/devtoolset-6-toolchain-centos7
LABEL com.vfxplatform.version="CY2019"

USER root

RUN yum install -y \
    alsa-lib alsa-lib-devel \
    automake autoconf \
    bison \
    bzip2-devel \
    ca-certificates \
    csh \
    db4-devel \
    dbus dbus-devel \
    doxygen \
    expat-devel \
    fam \
    file \
    fontconfig fontconfig-devel \
    freetype freetype-devel \
    gdbm-devel \
    git \
    glut-devel \
    gperf \
    java-1.8.0-openjdk \
    libcap-devel \
    libcap-devel \
    libjpeg libjpeg-devel \
    libpcap-devel \
    libpng libpng-devel \
    libtiff libtiff-devel \
    libv4l libv4l-devel \
    libxcb libxcb-devel \
    libXcomposite libXcomposite-devel \
    libXcursor libXcursor-devel \
    libXi libXi-devel \
    libxml2 libxml2-devel \
    libXmu libXmu-devel \
    libXp libXp-devel \
    libXpm libXpm-devel \
    libXrandr libXrandr-devel \
    libXrender libXrender-devel \
    libXScrnSaver libXScrnSaver-devel \
    libxslt libxslt-devel \
    libXtst-devel \
    make \
    mesa-libEGL-devel \
    mesa-libGL-devel \
    ncurses ncurses-devel \
    nss nss-devel \
    openssl-devel \
    patch \
    pciutils-devel \
    pkgconfig \
    pulseaudio-libs pulseaudio-libs-devel \
    pulseaudio-libs-devel \
    readline readline-devel \
    ruby \
    sqlite-devel \
    sudo \
    tcsh \
    tk-devel \
    wget \
    which \
    xcb-util xcb-util-devel \
    xcb-util-image xcb-util-image-devel \
    xcb-util-keysyms xcb-util-keysyms-devel \
    xcb-util-wm xcb-util-wm-devel \
    xz-devel \
    zlib-devel \
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
