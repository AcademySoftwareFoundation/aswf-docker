group "default" {
	targets = [
		"ci-base",
		"ci-baseqt",
	]
}

target "ci-base" {
	inherits = ["settings", "settings-2018"]
	target = "ci-base"
	dockerfile = "ci-base/Dockerfile"
	tags = [
		"docker.io/aswflocaltesting/ci-base:2018",
		"docker.io/aswflocaltesting/ci-base:2018.1",
	]
}

target "ci-baseqt" {
	inherits = ["settings", "settings-2018"]
	target = "ci-baseqt"
	dockerfile = "ci-baseqt/Dockerfile"
	tags = [
		"docker.io/aswflocaltesting/ci-baseqt:2018",
		"docker.io/aswflocaltesting/ci-baseqt:2018.1",
	]
}
