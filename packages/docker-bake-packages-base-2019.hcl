group "default" {
	targets = [
		"package-python",
		"package-boost",
		"package-tbb",
		"package-cppunit",
		"package-log4cplus",
		"package-glew",
		"package-glfw",
	]
}

target "settings" {
	dockerfile = "packages/Dockerfile"
}

target "package-python" {
	target = "ci-base-python-package"
	inherits = ["settings", "settings-2019"]
	tags = ["docker.io/aswftesting/ci-package-python:2019"]
}

target "package-boost" {
	target = "ci-base-boost-package"
	inherits = ["settings", "settings-2019"]
	tags = ["docker.io/aswftesting/ci-package-boost:2019"]
}

target "package-tbb" {
	target = "ci-base-tbb-package"
	inherits = ["settings", "settings-2019"]
	tags = ["docker.io/aswftesting/ci-package-tbb:2019"]
}

target "package-cppunit" {
	target = "ci-base-cppunit-package"
	inherits = ["settings", "settings-2019"]
	tags = ["docker.io/aswftesting/ci-package-cppunit:2019"]
}

target "package-glew" {
	target = "ci-base-glew-package"
	inherits = ["settings", "settings-2019"]
	tags = ["docker.io/aswftesting/ci-package-glew:2019"]
}

target "package-glfw" {
	target = "ci-base-glfw-package"
	inherits = ["settings", "settings-2019"]
	tags = ["docker.io/aswftesting/ci-package-glfw:2019"]
}

target "package-log4cplus" {
	target = "ci-base-log4cplus-package"
	inherits = ["settings", "settings-2019"]
	tags = ["docker.io/aswftesting/ci-package-log4cplus:2019"]
}
