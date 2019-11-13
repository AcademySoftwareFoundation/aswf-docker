group "default" {
	targets = [
		"ci-base",
		"ci-baseqt",
	]
}

target "ci-base" {
	inherits = ["settings", "settings-2020"]
	target = "ci-base"
	dockerfile = "ci-base/Dockerfile"
	tags = [
		"docker.io/aswftesting/ci-base:2020",
		"docker.io/aswftesting/ci-base:2020.1",
	]
}

target "ci-baseqt" {
	inherits = ["settings", "settings-2020"]
	target = "ci-baseqt"
	dockerfile = "ci-baseqt/Dockerfile"
	tags = [
		"docker.io/aswftesting/ci-baseqt:2020",
		"docker.io/aswftesting/ci-baseqt:2020.1",
	]
}
