[![Build Status](https://dev.azure.com/academysoftwarefoundation/Academy%20Software%20Foundation/_apis/build/status/AZP%20aswf-docker?branchName=master)](https://dev.azure.com/academysoftwarefoundation/Academy%20Software%20Foundation/_build/latest?definitionId=2&branchName=master)

# Docker Images for the Academy Software Foundation

## CI Images
`aswf/ci-base:2019`: A base CentOS-7 image with devtoolset-6, clang-7 and most common VFX Platform requirements pre-installed.
`aswf/ci-ocio:2019`: Based on `aswf/ci-base`, comes with all OpenColorIO upstream dependencies pre-installed.
`aswf/ci-openvdb:2019`: Based on `aswf/ci-base`, comes with all OpenVDB upstream dependencies pre-installed.
