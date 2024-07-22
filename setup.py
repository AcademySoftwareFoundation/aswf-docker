# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
from setuptools import setup, find_packages

with open("python/README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="aswfdocker",
    version="0.7.0",
    author="Aloys Baillet",
    author_email="aloys.baillet+github@gmail.com",
    description="ASWF Docker Utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AcademySoftwareFoundation/aswf-docker",
    packages=find_packages(where="python"),
    package_dir={"": "python"},
    package_data={"aswfdocker": ["data/*.yaml", "data/*.jinja2"]},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    # Empty list of requirements before running `pipenv update` to avoid conflicts
    install_requires=[
        "bottle==0.12.20",
        "certifi==2022.5.18.1; python_version >= '3.6'",
        "charset-normalizer==2.0.12; python_version >= '3'",
        "click==8.1.3",
        "colorama==0.4.4; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "conan==1.47",
        "deprecated==1.2.13; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "distro==1.6.0; sys_platform == 'linux' or sys_platform == 'linux2'",
        "fasteners==0.17.3; python_version >= '3.6'",
        "idna==3.3; python_version >= '3'",
        "importlib-resources==5.7.1",
        "jinja2==3.1.2",
        "markupsafe==2.1.1; python_version >= '3.7'",
        "node-semver==0.6.1",
        "patch-ng==1.17.4",
        "pluginbase==1.0.1",
        "pygithub==1.54.1",
        "pygments==2.12.0; python_version >= '3.6'",
        "pyjwt==1.7.1",
        "python-dateutil==2.8.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2'",
        "pyyaml==5.4.1",
        "requests==2.27.1",
        "six==1.16.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2'",
        "tqdm==4.64.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "urllib3==1.26.9; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4' and python_version < '4'",
        "wrapt==1.14.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "zipp==3.8.0; python_version < '3.10'",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "aswfdocker=aswfdocker.cli.aswfdocker:cli",
        ],
    },
)
