#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

# The nvidia/cuda:x.y.z-devel-rockylinux8 are layered on top of the nvidia/cuda:x.y.z-runtime-rockylinux8
# images but include large components which are not needed for our build images.
# Specifically we want to skip installing (sizes are for version 12.6.3)
# - cuda-nsight-compute-x-y : 1GB (GUI profiling tool)
# - libcublas-devel-x-y : 930MB (large static libraries)
# - libcusparse-devel-x-y : 620MB (large static libraries)
# - libcufft-devel-x-y : 580MB (large static libraries)
# - libnpp-devel-x-y : 257MB (large static libraries)
# - libcusolver-devel-x-y : 195MB (large static libraries)
#
# A further complication is that these -devel RPMs are packaged as a meta RPM package,
# cuda-libraries-devel-x-y so we have to pick apart that meta package in order to install
# as many reasonably sized sub components as possible.
#
# This script is based on the Dockerfile which layers the -devel image on top of the -runtime image:
# https://gitlab.com/nvidia/container-images/cuda/-/raw/master/dist/12.6.3/rockylinux8/devel/Dockerfile
#
# Versions will need to be updated when a new version of CUDA is selected.
#

NV_CUDA_LIB_VERSION="${ASWF_CUDA_VERSION}-1"
IFS='.' read -r CUDA_MAJOR CUDA_MINOR CUDA_PATCH <<< "${ASWF_CUDA_VERSION}"
declare -A NV_NVPROF_VERSION=( [12.6.1]=12.6.68-1 [12.6.3]=12.6.80-1 )
NV_NVPROF_DEV_PACKAGE=cuda-nvprof-${CUDA_MAJOR}-${CUDA_MINOR}-${NV_NVPROF_VERSION[$ASWF_CUDA_VERSION]}
declare -A NV_NVML_DEV_VERSION=( [12.6.1]=12.6.68-1 [12.6.3]=12.6.77-1 )
NV_NVML_DEV_PACKAGE=cuda-nvml-devel-${CUDA_MAJOR}-${CUDA_MINOR}-${NV_NVML_DEV_VERSION[$ASWF_CUDA_VERSION]}
declare -A NV_LIBNCCL_DEV_PACKAGE_VERSION=( [12.6.1]=2.22.3-1 [12.6.3]=2.23.4-1 )
NV_LIBNCCL_DEV_PACKAGE=libnccl-devel-${NV_LIBNCCL_DEV_PACKAGE_VERSION[$ASWF_CUDA_VERSION]}+cuda${CUDA_MAJOR}.${CUDA_MINOR}

# Query and filter the list of packages we want to install from the cuda-libraries-devel meta package

NV_FILTERED_LIBRARIES_DEVEL=$(dnf repoquery --quiet --requires --resolve cuda-libraries-devel-${CUDA_MAJOR}-${CUDA_MINOR} | \
    sed -E '/(libcublas|libcusparse|libcufft|libnpp|libcusolver)-devel/d')

# This is what the nvidia/cuda Dockerfile does, there is some redundancy since some of the packages
# are part of the cuda-libraries-devel meta package.
#
#RUN yum install -y \
#    make \
#    findutils \
#    cuda-command-line-tools-12-6-${NV_CUDA_LIB_VERSION} \
#    cuda-libraries-devel-12-6-${NV_CUDA_LIB_VERSION} \
#    cuda-minimal-build-12-6-${NV_CUDA_LIB_VERSION} \
#    cuda-cudart-devel-12-6-${NV_CUDA_CUDART_DEV_VERSION} \
#    ${NV_NVPROF_DEV_PACKAGE} \
#    cuda-nvml-devel-12-6-${NV_NVML_DEV_VERSION} \
#    libcublas-devel-12-6-${NV_LIBCUBLAS_DEV_VERSION} \
#    ${NV_LIBNPP_DEV_PACKAGE} \
#    ${NV_LIBNCCL_DEV_PACKAGE} \
#    ${NV_CUDA_NSIGHT_COMPUTE_DEV_PACKAGE} \
#    && yum clean all \
#    && rm -rf /var/cache/yum/*

dnf install -y \
    make \
    findutils \
    cuda-command-line-tools-${CUDA_MAJOR}-${CUDA_MINOR}-${NV_CUDA_LIB_VERSION} \
    $NV_FILTERED_LIBRARIES_DEVEL \
    cuda-minimal-build-${CUDA_MAJOR}-${CUDA_MINOR}-${NV_CUDA_LIB_VERSION} \
    ${NV_NVPROF_DEV_PACKAGE} \
    ${NV_NVML_DEV_PACKAGE} \
    ${NV_LIBNCCL_DEV_PACKAGE} \
    && dnf clean all \
    && rm -rf /var/cache/yum/*
