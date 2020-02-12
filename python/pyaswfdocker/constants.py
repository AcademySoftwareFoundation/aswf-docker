import enum
from . import versioninfo


class IMAGE_TYPE(enum.Enum):
    IMAGE = "image"
    PACKAGE = "package"


VERSIONS = {
    IMAGE_TYPE.PACKAGE: {
        "clang": ["1"],
        "python": ["2018.1", "2019.1", "2020.1"],
        "boost": ["2018.1", "2019.1", "2020.1"],
        "tbb": ["2018.1", "2019.1", "2020.1"],
        "cppunit": ["2018.1", "2019.1", "2020.1"],
        "glew": ["2018.1", "2019.1", "2020.1"],
        "glfw": ["2018.1", "2019.1", "2020.1"],
        "log4cplus": ["2018.1", "2019.1", "2020.1"],
        "qt": ["2018.1", "2019.1", "2020.1"],
        "pyside": ["2018.1", "2019.1", "2020.1"],
        "blosc": ["2018.1", "2019.1", "2020.1"],
        "openexr": ["2018.1", "2019.1", "2020.1"],
        "alembic": ["2018.1", "2019.1"],
        "ocio": ["2018.1", "2019.1"],
        "oiio": ["2018.1", "2019.1"],
        "opensubdiv": ["2018.1", "2019.1"],
        "ptex": ["2018.1", "2019.1"],
        "openvdb": ["2019.1"],
        "usd": ["2019.2"],
    },
    IMAGE_TYPE.IMAGE: {
        "common": ["1.1"],
        "base": ["2018.1", "2019.1", "2020.1"],
        "openexr": ["2018.1", "2019.1", "2020.1"],
        "openvdb": ["2018.1", "2019.1", "2020.1"],
        "ocio": ["2018.1", "2019.1"],
        "opencue": ["2018.1", "2019.1", "2020.1"],
        "usd": ["2019.1"],
        "vfxall": ["2019.2"],
    },
}

GROUPS = {
    IMAGE_TYPE.PACKAGE: {
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
    },
    IMAGE_TYPE.IMAGE: {
        "common": ["common"],
        "base": ["base"],
        "vfx": ["openexr", "openvdb", "ocio", "opencue", "usd", "vfxall"],
    },
}

VERSION_INFO = {
    "2018": versioninfo.VersionInfo(
        version="2018", label=None, ciCommonVersion="1", pythonVersion="2.7",
    ),
    "2019": versioninfo.VersionInfo(
        version="2019", label="latest", ciCommonVersion="1", pythonVersion="2.7",
    ),
    "2020": versioninfo.VersionInfo(
        version="2020", label="preview", ciCommonVersion="1", pythonVersion="3.7",
    ),
}

PUBLISH_DOCKER_ORG = "aswf"
TESTING_DOCKER_ORG = "aswftesting"
# this org is not valid, but this ensures that the test will not accidently pull an existing image
FAKE_DOCKER_ORG = "aswflocaltesting"
