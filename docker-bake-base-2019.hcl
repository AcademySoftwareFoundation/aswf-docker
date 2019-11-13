group "default" {
	targets = [
		"ci-common",
		"ci-base",
		"ci-baseqt",
	]
}

target "ci-common" {
	inherits = ["settings-nopush", "settings-2018"]
	target = "ci-common"
	dockerfile = "ci-common/Dockerfile"
	tags = [
		"docker.io/aswftesting/ci-common:1"
	]
}

target "ci-base" {
	inherits = ["settings", "settings-2019"]
	target = "ci-base"
	dockerfile = "ci-base/Dockerfile"
	tags = [
		"docker.io/aswftesting/ci-base:2019",
		"docker.io/aswftesting/ci-base:2019.0",
	]
}

target "ci-baseqt" {
	inherits = ["settings", "settings-2019"]
	target = "ci-baseqt"
	dockerfile = "ci-baseqt/Dockerfile"
	tags = [
		"docker.io/aswftesting/ci-baseqt:2019",
		"docker.io/aswftesting/ci-baseqt:2019.0",
	]
}
