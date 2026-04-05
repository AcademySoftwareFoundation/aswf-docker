# CLAUDE.md - AI Assistant Guide for aswf-docker

## Project Overview

**aswf-docker** builds and manages Docker CI images and Conan packages for the
[Academy Software Foundation (ASWF)](https://www.aswf.io/) VFX Platform. It
provides standardized build environments for VFX software across multiple
platform years (2019-2026).

## Repository Structure

```
aswf-docker/
├── ci-*/                  # Docker image directories (18 images)
│   ├── Dockerfile         # AUTO-GENERATED - do not edit manually
│   ├── README.md          # AUTO-GENERATED - do not edit manually
│   └── image.yaml         # Source specification for the image
├── python/
│   └── aswfdocker/        # Main Python package
│       ├── cli/           # Click CLI entry point (aswfdocker.py)
│       ├── data/          # Jinja2 templates, versions.yaml
│       ├── tests/         # Unit tests (pytest)
│       ├── builder.py     # Docker buildx bake orchestration
│       ├── dockergen.py   # Jinja2 template rendering
│       ├── index.py       # Version/package index from YAML
│       ├── releaser.py    # GitHub release automation
│       └── ...
├── packages/
│   ├── conan/recipes/     # 116+ Conan package recipes (vendored)
│   ├── conan/settings/    # Conan profile settings
│   └── common/            # Shared build utilities
├── scripts/               # Shell utilities, VFX scripts, tests
├── .github/workflows/     # CI: python.yml, docker-builds.yml, release.yml, python-sonar.yml
├── versions.yaml          # Symlink to python/aswfdocker/data/versions.yaml
└── pyproject.toml         # Python project config (uv, pytest, black)
```

### Key Concepts

- **versions.yaml**: Central version registry defining package versions per VFX
  Platform year. Versions use inheritance (e.g., `2-clang10` inherits from `2`).
- **image.yaml**: Per-image specs listing packages, base image, and metadata.
- **Dockerfiles are generated**: From Jinja2 templates via `aswfdocker dockergen`.
  Never edit `ci-*/Dockerfile` or `ci-*/README.md` directly.
- **Docker buildx bake**: Builds are orchestrated via JSON bake files generated
  by `python/aswfdocker/builder.py`.

## Development Setup

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install all dependencies (including dev)
uv sync --all-extras

# Run the CLI
uv run aswfdocker --help
```

## Common Commands

### Testing & Linting

```bash
# Run unit tests
uv run pytest python/aswfdocker

# Type checking
uv run mypy python/aswfdocker

# Linting (score must be >= 8.0)
uv run pylint python/aswfdocker

# Formatting (Black, targets Python 3.10)
uv run black python/ packages/conan/recipes/

# Run all pre-commit hooks
uv run pre-commit run --all-files

# Verify generated Dockerfiles are up to date
uv run aswfdocker dockergen --check
```

### Building Images

```bash
# Build a specific image group and version
uv run aswfdocker build --ci-image-type IMAGE --group base --version 2026-clang20 --push NO

# Build Conan packages
uv run aswfdocker build --ci-image-type PACKAGE --group common --version 2026-clang20 --push NO

# Dry run (show commands without executing)
uv run aswfdocker build --ci-image-type IMAGE --group base --version 2026-clang20 --dry-run
```

### Regenerating Dockerfiles

```bash
# Regenerate all Dockerfiles and READMEs from templates
uv run aswfdocker dockergen

# Check that generated files are up to date (used in CI)
uv run aswfdocker dockergen --check
```

## Code Conventions

### Python

- **Python >= 3.10** required
- **Black** formatting (target: py310). Vendored Conan recipes in
  `packages/conan/recipes/` are excluded from Black.
- **MyPy** strict type checking (Python 3.11 target)
- **Pylint** with fail-under score of 8.0
- **Naming**: PascalCase classes, snake_case functions/variables, UPPER_CASE constants
- **Copyright header** on all files:
  `# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.`
  `# SPDX-License-Identifier: Apache-2.0`

### Docker Images

- Image names: `ci-{name}` (e.g., `ci-base`, `ci-openexr`)
- Tags: `{major_version}` or `{major_version}-clang{N}` (e.g., `2026-clang20`)
- Docker orgs: `aswf` (production), `aswftesting` (testing), `aswflocaltesting` (local)
- OCI metadata labels are set automatically from templates

### Version Management

- All package versions are defined in `versions.yaml`
- Versions use parent inheritance: variant versions (e.g., `6-clang18`) inherit
  from base versions (e.g., `6`) and override specific fields
- The `major_version` field maps to VFX Platform years

## CI/CD Workflows

| Workflow | Trigger | Purpose |
|---|---|---|
| `python.yml` | Push/PR | Pre-commit hooks: black, pytest, mypy, pylint, dockergen --check |
| `docker-builds.yml` | Push/PR | Build Docker images and Conan packages (matrix by VFX year) |
| `python-sonar.yml` | Push to main | Code quality analysis with SonarCloud |
| `release.yml` | GitHub Release | Full build + push to Docker Hub |

## Git Conventions

- **Signed-off commits required**: Use `git commit -s`
- **Rebase-only merging** (no squash/merge commits) for linear history
- **Branch model**: OneFlow - all work on `main`, release branches for bug fixes
- **Release tags**: `v{major}.{minor}.{patch}`
- **Release branches**: `RB-{major}.{minor}`

## Important Warnings

1. **Never edit `ci-*/Dockerfile` or `ci-*/README.md` directly** - these are
   generated from Jinja2 templates. Edit the templates in
   `python/aswfdocker/data/` and the specs in `ci-*/image.yaml` instead, then
   run `uv run aswfdocker dockergen`.
2. **Conan recipes in `packages/conan/recipes/` are vendored** from Conan Center
   Index. They are excluded from Black formatting and SonarCloud analysis.
3. **`versions.yaml` is a symlink** to `python/aswfdocker/data/versions.yaml`.
4. The `migrate` and `download` CLI commands are **deprecated**.
