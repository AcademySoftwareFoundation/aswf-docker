group "default" {
	targets = [
		"ci-base",
		"ci-openexr",
		"ci-openvdb",
		"ci-ocio",
		"ci-opencue",
		# "ci-usd",
		# "ci-vfxall",
	]
}

target "ci-base" {
	inherits = ["settings", "settings-2018"]
	target = "ci-base"
	tags = [
		"docker.io/aswftesting/ci-base:2018",
		"docker.io/aswftesting/ci-base:2018.0",
	]
}

target "ci-openexr" {
	inherits = ["settings", "settings-2018"]
	target = "ci-openexr"
	tags = [
		"docker.io/aswftesting/ci-openexr:2018",
		"docker.io/aswftesting/ci-openexr:2018.0",
	]
}

target "ci-openvdb" {
	inherits = ["settings", "settings-2018"]
	target = "ci-openvdb"
	tags = [
		"docker.io/aswftesting/ci-openvdb:2018",
		"docker.io/aswftesting/ci-openvdb:2018.0",
	]
}

target "ci-ocio" {
	inherits = ["settings", "settings-2018"]
	target = "ci-ocio"
	tags = [
		"docker.io/aswftesting/ci-ocio:2018",
		"docker.io/aswftesting/ci-ocio:2018.0",
	]
}

target "ci-opencue" {
	inherits = ["settings", "settings-2018"]
	target = "ci-opencue"
	tags = [
		"docker.io/aswftesting/ci-opencue:2018",
		"docker.io/aswftesting/ci-opencue:2018.0",
	]
}

target "ci-usd" {
	inherits = ["settings", "settings-2018"]
	target = "ci-usd"
	tags = [
		"docker.io/aswftesting/ci-usd:2018",
		"docker.io/aswftesting/ci-usd:2018.0",
	]
}

target "ci-vfxall" {
	inherits = ["settings", "settings-2018"]
	target = "ci-vfxall"
	tags = [
		"docker.io/aswftesting/ci-vfxall:2018",
		"docker.io/aswftesting/ci-vfxall:2018.0",
	]
}
