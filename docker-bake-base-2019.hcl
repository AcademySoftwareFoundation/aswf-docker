group "default" {
	targets = [
		"ci-base",
		"ci-baseqt",
	]
}

target "ci-base" {
	inherits = ["settings", "settings-2019"]
	target = "ci-base"
	dockerfile = "ci-base/Dockerfile"
	tags = [
		"docker.io/aswftesting/ci-base:2019",
		"docker.io/aswftesting/ci-base:2019.1",
		"docker.io/aswftesting/ci-base:latest",
	]
}

target "ci-baseqt" {
	inherits = ["settings", "settings-2019"]
	target = "ci-baseqt"
	dockerfile = "ci-baseqt/Dockerfile"
	tags = [
		"docker.io/aswftesting/ci-baseqt:2019",
		"docker.io/aswftesting/ci-baseqt:2019.2",
		"docker.io/aswftesting/ci-baseqt:latest",
	]
}
