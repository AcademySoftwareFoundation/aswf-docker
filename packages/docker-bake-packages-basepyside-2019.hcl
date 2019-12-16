group "default" {
	targets = [
		"package-pyside",
	]
}

target "settings" {
	dockerfile = "packages/Dockerfile"
}

target "package-pyside" {
	target = "ci-base-pyside-package"
	inherits = ["settings", "settings-2019"]
	tags = ["docker.io/aswftesting/ci-package-pyside:2019"]
}
