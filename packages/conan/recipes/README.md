# Conan Package Recipes

Many of these recipes are borrowed from the [Conan Center Index](https://github.com/conan-io/conan-center-index/tree/master/recipes),
but with quite a few modifications to allow the VFX versions to build, and with added settings to only allow Conan to resolve
ASWF-made packages and avoid ABI mixes with the Conan Center packages.

As the Conan Center Index is MIT licensed the whole subfolder here is also MIT licensed for consistency.

## Adding new Conan packages

Follow the great instructions there: [Conan Center Index - How to add Packages](https://github.com/conan-io/conan-center-index/blob/master/docs/how_to_add_packages.md).

Then ensure the ASWF-specific settings are added in the `conanfile.py` such as: `python`, `devtoolset`, `ci_common` and `vfx_platform`.
