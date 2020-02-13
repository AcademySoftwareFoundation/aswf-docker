import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyaswfdocker",
    version="0.1.0",
    author="Aloys Baillet",
    author_email="aloys.baillet+github@gmail.com",
    description="ASWF Docker Utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AcademySoftwareFoundation/aswf-docker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache 2 License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'Click',
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "aswfdocker=pyaswfdocker.cli.aswfdocker:cli",
        ],
    },
)
