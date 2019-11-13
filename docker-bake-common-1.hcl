group "default" {
	targets = [
		"ci-common-1"
	]
}

target "ci-common-1" {
	inherits = ["settings", "settings-2018"]
	target = "ci-common"
	dockerfile = "ci-common/Dockerfile"
	tags = [
		"docker.io/aswftesting/ci-common:1",
		"docker.io/aswftesting/ci-common:1.1",
		"docker.io/aswftesting/ci-common:latest",
	]
}
