group "default" {
	targets = [
		"package-clang",
	]
}

target "settings" {
	dockerfile = "packages/Dockerfile"
}

target "package-clang" {
	target = "ci-common-clang-package"
	inherits = ["settings", "settings-2018"]
	tags = ["docker.io/aswftesting/ci-package-clang:1"]
}
