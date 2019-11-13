target "settings" {
	args {
		BUILD_DATE = "dev"
        VCS_REF = "dev"
		ASWF_ORG = "aswftesting"
		ASWF_PKG_ORG = "aswftesting"
	}
}

target "settings-2018" {
	args {
		CI_COMMON_VERSION = "1"
		VFXPLATFORM_VERSION = "2018"
		ASWF_VERSION = "2018.0"
		PYTHON_VERSION = "2.7"
	}
}

target "settings-2019" {
	args {
		CI_COMMON_VERSION = "1"
		VFXPLATFORM_VERSION = "2019"
		ASWF_VERSION = "2019.0"
		PYTHON_VERSION = "2.7"
	}
}

target "settings-2020" {
	args {
		CI_COMMON_VERSION = "1"
		VFXPLATFORM_VERSION = "2020"
		ASWF_VERSION = "2020.0"
		PYTHON_VERSION = "3.7"
	}
}
