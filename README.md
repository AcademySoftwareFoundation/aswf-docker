[![Build Status](https://dev.azure.com/academysoftwarefoundation/Academy%20Software%20Foundation/_apis/build/status/AZP%20aswf-docker?branchName=master)](https://dev.azure.com/academysoftwarefoundation/Academy%20Software%20Foundation/_build/latest?definitionId=2&branchName=master)

# Docker Images for the Academy Software Foundation

More information:
* [VFXPlatform](https://vfxplatform.com)
* [ASWF](https://aswf.io)

## CI Images

These images are for Continuous Integration testing of various project managed by the ASWF.
Each image (apart from `ci-common`) is available for multiple VFX Platform Years.

* `aswf/ci-common:1.0`: A base CentOS-7 image with devtoolset-6, clang-7 and cuda.
* `aswf/ci-base:20XX`: Based on `aswf/ci-common` with most most VFX Platform requirements pre-installed.
* `aswf/ci-openexr:20XX`: Based on `aswf/ci-common`, comes with all OpenEXR upstream dependencies pre-installed.
* `aswf/ci-ocio:20XX`: Based on `aswf/ci-common`, comes with all OpenColorIO upstream dependencies pre-installed.
* `aswf/ci-openvdb:20XX`: Based on `aswf/ci-common`, comes with all OpenVDB upstream dependencies pre-installed.

### Image Tags

The most precise version tag is the `ASWF_VERSION` of the image, e.g. `aswf/ci-base:2019.0`, but it is recommended to use the `VFXPLATFORM_VERSION` as the tag to use in CI pipelines, e.g. `aswf/ci-openexr:2019`.

The `latest` tag is pointing to the current VFX Platorm year images, e.g. `aswf/ci-openexr:latest` points to `aswf/ci-openexr:2019.0` but will be updated to point to `aswf/ci-openexr:2020.0` in the calendar year 2020.


### Status
As of June 2019 there are 2018 and 2019 VFX Platform. The 2020 version only contains base packages (such as python-3.7 and boost).
