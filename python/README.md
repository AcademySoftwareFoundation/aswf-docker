# ASWF Python Utilities

`aswfdocker` is available to help with package and image building and manipulations.

`aswfdocker build` builds images:
Example use:
```bash
# Build and push USD package to aswftesting
aswfdocker --verbose build -t PACKAGE --group-name vfx --group-version 2019 --target usd --push
# Build and push ci-vfxall image to aswftesting
aswfdocker --verbose build -t IMAGE --group-name vfx --group-version 2019 --target vfxall --push
```

`aswfdocker migrate` can migrate packages between docker organisations

