group "default" {
	targets = [
		"ci-openexr",
		"ci-openvdb",
		# "ci-ocio",
		"ci-opencue",
		# "ci-usd",
		# "ci-vfxall",
	]
}

target "ci-openexr" {
	inherits = ["settings", "settings-2020"]
	target = "ci-openexr"
	dockerfile = "ci-openexr/Dockerfile"
	tags = [
		"docker.io/aswftesting/ci-openexr:2020",
		"docker.io/aswftesting/ci-openexr:2020.1",
	]
}

target "ci-openvdb" {
	inherits = ["settings", "settings-2020"]
	target = "ci-openvdb"
	dockerfile = "ci-openvdb/Dockerfile"
	tags = [
		"docker.io/aswftesting/ci-openvdb:2020",
		"docker.io/aswftesting/ci-openvdb:2020.1",
	]
}

target "ci-ocio" {
	inherits = ["settings", "settings-2020"]
	target = "ci-ocio"
	dockerfile = "ci-ocio/Dockerfile"
	tags = [
		"docker.io/aswftesting/ci-ocio:2020",
		"docker.io/aswftesting/ci-ocio:2020.1",
	]
}

target "ci-opencue" {
	inherits = ["settings", "settings-2020"]
	target = "ci-opencue"
	dockerfile = "ci-opencue/Dockerfile"
	tags = [
		"docker.io/aswftesting/ci-opencue:2020",
		"docker.io/aswftesting/ci-opencue:2020.1",
	]
}

target "ci-usd" {
	inherits = ["settings", "settings-2020"]
	target = "ci-usd"
	dockerfile = "ci-usd/Dockerfile"
	tags = [
		"docker.io/aswftesting/ci-usd:2020",
		"docker.io/aswftesting/ci-usd:2020.1",
	]
}

target "ci-vfxall" {
	inherits = ["settings", "settings-2020"]
	target = "ci-vfxall"
	dockerfile = "ci-vfxall/Dockerfile"
	tags = [
		"docker.io/aswftesting/ci-vfxall:2020",
		"docker.io/aswftesting/ci-vfxall:2020.1",
	]
}
