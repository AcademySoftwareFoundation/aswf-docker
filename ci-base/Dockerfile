FROM centos/devtoolset-6-toolchain-centos7
LABEL com.vfxplatform.version="CY2019"

USER root

RUN yum install -y \
    bzip2-devel \
    file \
    make \
    python-devel \
    which \
    zlib-devel \
    git \
    ca-certificates \
    ssh \
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
    && \
    yum clean all

RUN curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py" &&\
    python get-pip.py

RUN pip install \
    nose \
    epydoc

COPY scripts/* /tmp/

# Install base build toolset
RUN /tmp/install_ninja.sh 1.9.0 && \
    /tmp/install_cmake.sh 3.11.4 && \
    /tmp/install_clang.sh 7.0.1 && \
    /tmp/install_sonar.sh 3.3.0.1492

# Install most common dependencies
RUN /tmp/install_boost.sh 1.66.0 && \
    /tmp/install_tbb.sh 2018 && \
    /tmp/install_numpy.sh 1.14 && \
    /tmp/install_cppunit.sh 1.14.0
