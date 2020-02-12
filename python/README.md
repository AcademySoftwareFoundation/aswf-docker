# ASWF Python Utilities

`build-packages` builds packages
Example use:
```bash
# Build and push USD package to aswftesting
build-images --image-type PACKAGE --group-name vfx --group-version 2019 --target usd --verbose --push
# Build and push ci-vfxall image to aswftesting
build-images --image-type IMAGE --group-name vfx --group-version 2019 --target vfxall --verbose --push
```

`migrate-packages` can migrate packages between docker organisations

