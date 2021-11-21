# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
from setuptools import setup, find_packages

with open("python/README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="aswfdocker",
    version="0.6.0",
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
        "bottle==0.12.19",
        "certifi==2021.10.8",
        "charset-normalizer==2.0.7; python_version >= '3'",
        "click==8.0.3",
        "colorama==0.4.4; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "conan==1.42",
        "deprecated==1.2.13; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "distro==1.6.0",
        "fasteners==0.16.3",
        "idna==3.3; python_version >= '3'",
        "importlib-resources==5.4.0",
        "jinja2==2.11.3",
        "markupsafe==2.0.1; python_version >= '3.6'",
        "node-semver==0.6.1",
        "patch-ng==1.17.4",
        "pluginbase==1.0.1",
        "pygithub==1.53",
        "pygments==2.10.0; python_version >= '3.5'",
        "pyjwt==1.7.1",
        "python-dateutil==2.8.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "pyyaml==5.4.1",
        "requests==2.26.0",
        "six==1.16.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "tqdm==4.62.3; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "urllib3==1.26.7; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4' and python_version < '4'",
        "wrapt==1.13.3; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "zipp==3.6.0; python_version < '3.10'",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "aswfdocker=aswfdocker.cli.aswfdocker:cli",
        ],
    },
)
