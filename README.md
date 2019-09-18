# Docker Images for the Academy Software Foundation

| Docker Images | Build Status |
| ---:         |     :---      |
| `aswf/ci-*`        | [![Build Status - aswf](https://dev.azure.com/academysoftwarefoundation/Academy%20Software%20Foundation/_apis/build/status/AZP%20aswf-docker?branchName=master)](https://dev.azure.com/academysoftwarefoundation/Academy%20Software%20Foundation/_build/latest?definitionId=2&branchName=master)
| `aswftesting/ci-*` | [![Build Status - aswf](https://dev.azure.com/academysoftwarefoundation/Academy%20Software%20Foundation/_apis/build/status/AZP%20aswf-docker?branchName=testing)](https://dev.azure.com/academysoftwarefoundation/Academy%20Software%20Foundation/_build/latest?definitionId=2&branchName=testing)


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

### Versions

The `VFXPLATFORM_VERSION` is the calendar year mentioned in the VFX Platform, e.g. `2019`.

The `ASWF_VERSION` is a semantic version made of the `VFXPLATFORM_VERSION` as the major version number, and a minor version number to indicate minor changes in the Docker Image that still point to the same calendar year version, e.g. `2019.0` would be followed if necessary by a `2019.1` version.
The minor version here does *not* point to a calendar month or quarter, it is solely to express that the image has changed internally. We could also have a patch version.

### Image Tags

The most precise version tag is the `ASWF_VERSION` of the image, e.g. `aswf/ci-base:2019.0`, but it is recommended to use the `VFXPLATFORM_VERSION` as the tag to use in CI pipelines, e.g. `aswf/ci-openexr:2019`.

The `latest` tag is pointing to the current VFX Platorm year images, e.g. `aswf/ci-openexr:latest` points to `aswf/ci-openexr:2019.0` but will be updated to point to `aswf/ci-openexr:2020.0` in the calendar year 2020.


## Testing Images

There is another dockerhub organisations with copies of the `aswf` docker images `aswftesting`: Images published there are for general testing and experimentations. Images can be pushed by any fork of the official repo as long as the branch is called `testing`. Images in this org will change without notice and could be broken in many unexpected ways!

To get write access to the `aswftesting` dockerhub organisation you can open a jira issue [there](jira.aswf.io).

### Status
As of September 2019 there are 2018 and 2019 VFX Platform. The 2020 version are experimental and mostly only contains base packages (such as python-3.7 and boost).
