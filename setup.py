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
        "bottle==0.12.25",  # caps at py3.7
        "certifi==2024.7.4; python_version >= '3.7'",
        "charset-normalizer==3.3.2; python_version >= '3'",
        "click==8.1.7",
        "colorama==0.4.6; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6'",
        "conan==1.65.0",  # this can jump a lot but can change a lot too
        "deprecated==1.2.14; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "distro==1.8.0; sys_platform == 'linux' or sys_platform == 'linux2'",
        "fasteners==0.19; python_version >= '3.7'",
        "idna==3.7; python_version >= '3'",
        "importlib-resources==5.12.0",  # above this drops 3.7
        "jinja2==3.1.4",
        "markupsafe==2.1.5; python_version >= '3.7'",
        "node-semver==0.6.1",  # capped by conan
        "patch-ng==1.17.4",
        "pluginbase==1.0.1",
        "pygithub==2.2.0",
        "pygments==2.17.2; python_version >= '3.7'",
        "pyjwt==2.8.0",
        "python-dateutil==2.9.0.post0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2'",
        "pyyaml==5.4.1",  # capped by conan
        "requests==2.32.0",
        "six==1.16.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2'",
        "typing_extensions==4.7.1; python_version >= '3.7'",
        "tqdm==4.66.3; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6'",
        "urllib3==1.26.19; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4, 3.5' and python_version < '4'",  # capped by conan
        "wrapt==1.16.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4, 3.5'",
        "zipp==3.19.1; python_version < '3.10'",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "aswfdocker=aswfdocker.cli.aswfdocker:cli",
        ],
    },
)
