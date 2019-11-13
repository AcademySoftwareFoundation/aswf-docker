group "default" {
	targets = [
		"package-qt",
	]
}

target "settings" {
	dockerfile = "packages/Dockerfile"
}

target "package-qt" {
	target = "ci-base-qt-package"
	inherits = ["settings", "settings-2019"]
	tags = ["docker.io/aswftesting/ci-package-qt:2019"]
}
