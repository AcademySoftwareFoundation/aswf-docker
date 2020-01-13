PACKAGES = {
    "clang": ["1"],
    "python": ["2018", "2019", "2020"],
    "boost": ["2018", "2019", "2020"],
    "tbb": ["2018", "2019", "2020"],
    "cppunit": ["2018", "2019", "2020"],
    "glew": ["2018", "2019", "2020"],
    "glfw": ["2018", "2019", "2020"],
    "log4cplus": ["2018", "2019", "2020"],
    "qt": ["2018", "2019", "2020"],
    "pyside": ["2018", "2019", "2020"],
    "blosc": ["2018", "2019", "2020"],
    "openexr": ["2018", "2019", "2020"],
    "alembic": ["2018", "2019"],
    "ocio": ["2018", "2019"],
    "oiio": ["2018", "2019"],
    "opensubdiv": ["2018", "2019"],
    "ptex": ["2018", "2019"],
    "openvdb": ["2019"],
    "usd": ["2019"],
}

PACKAGE_GROUPS = {
    "common": ["clang"],
    "base": ["python", "boost", "tbb", "cppunit", "glew", "glfw", "log4cplus"],
    "baseqt": ["qt"],
    "basepyside": ["pyside"],
    "vfx": [
        "blosc",
        "openexr",
        "alembic",
        "ocio",
        "oiio",
        "opensubdiv",
        "ptex",
        "openvdb",
        "usd",
    ],
}

PYTHON_VERSIONS = {"2018": "2.7", "2019": "2.7", "2020": "3.7"}
