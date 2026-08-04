# Conan Package Recipes

Many of these recipes are borrowed from the [Conan Center Index](https://github.com/conan-io/conan-center-index/tree/master/recipes),
but a few modifications to allow all the VFX versions to build, avoid ABI mixes with the Conan Center packages.
The `python` setting has been added to better separate packages by python minor version.

As the Conan Center Index is MIT licensed the whole subfolder here is also MIT licensed for consistency.

## Adding new Conan packages

Follow the instructions in [CONTRIBUTING](../../../CONTRIBUTING.md#building-conan-packages)

## Tracking upstream Conan Center Index state

[`conan-center-index-upstream.json`](conan-center-index-upstream.json) is the source of
truth for which upstream CCI SHA each vendored recipe was last synced from — see
[CONTRIBUTING.md](../../../CONTRIBUTING.md) for the `aswfdocker conandiff` workflow
(checking, merging, and migrating). The `# From: ...` header comments still present in
individual recipe files are legacy/informational only.
