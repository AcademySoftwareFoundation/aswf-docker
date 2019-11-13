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
	inherits = ["settings", "settings-2020"]
	tags = ["docker.io/aswftesting/ci-package-pyside:2020"]
}
