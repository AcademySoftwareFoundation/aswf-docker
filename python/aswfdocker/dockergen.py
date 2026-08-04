# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Generation of Dockerfiles, READMEs and Conan profiles from Jinja2 templates.
"""
import logging
import os
import typing
import requests
import yaml
from jinja2 import Environment, PackageLoader

from aswfdocker import utils, index, constants


logger = logging.getLogger(__name__)


def conan_profile_version_keys(idx: index.Index) -> typing.List[str]:
    """Return version keys for which Conan profiles should be generated.

    Scans versions.yaml for entries marked ``generate_profile: true`` (the
    VFX Platform year entries) and collects their ``ci_common_version`` values
    so the matching ci_common profiles are generated automatically.  Adding a
    new VFX Platform year to versions.yaml with ``generate_profile: true``
    is all that is needed — no code change required.
    """
    ci_common_keys: typing.Set[str] = set()
    vfx_keys: typing.List[str] = []
    for vi in idx.iter_version_info():
        if vi.generate_profile:
            vfx_keys.append(vi.version)
            if vi.ci_common_version:
                ci_common_keys.add(vi.ci_common_version)
    return sorted(ci_common_keys) + sorted(vfx_keys)


class ConanProfileGen:
    """Generates a single Conan profile file from a Jinja2 template.

    Conan 2.x supports native Jinja2 rendering in profiles; this means the
    generated files themselves contain ``{% set org = os.getenv(...) %}`` and
    ``{{ org }}`` expressions that Conan resolves at runtime from the
    ``ASWF_PKG_ORG`` environment variable.  To avoid conflict, the aswfdocker
    templates use alternate delimiters (``[[ ]]`` / ``[% %]``) so the Conan
    Jinja2 syntax passes through the aswfdocker render step unchanged.
    """

    # Separate Jinja2 environment with non-standard delimiters so that
    # {{ }} / {% %} in the template are treated as literal text and land
    # verbatim in the generated file for Conan to render at runtime.
    _env = Environment(
        loader=PackageLoader("aswfdocker", "data"),
        block_start_string="[%",
        block_end_string="%]",
        variable_start_string="[[",
        variable_end_string="]]",
        comment_start_string="[#",
        comment_end_string="#]",
        # Remove the newline after block tags so [% if %] / [% endif %]
        # don't introduce extra blank lines in the rendered profile.
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )

    def __init__(self, version_key: str):
        self._idx = index.Index()
        self.version_info = self._idx.version_info(version_key)

    def _template_context(self) -> typing.Dict[str, typing.Any]:
        # Resolve OS-distro–specific package versions (bison, flex, etc.) from
        # the ASWF_BASEOS_DISTRO value inherited by this version entry.  For
        # vfx year entries the value is inherited from the ci_common parent
        # (e.g. "6" carries ASWF_BASEOS_DISTRO: "rockylinux8").  The distro
        # entry in versions.yaml is keyed by that distro name.
        baseos_distro = self.version_info.all_package_versions.get("ASWF_BASEOS_DISTRO")
        distro_versions: typing.Dict[str, str] = {}
        if baseos_distro:
            distro_versions = self._idx.version_info(baseos_distro).package_versions
        ci_common_version = self.version_info.ci_common_version
        clang_versions: typing.Dict[str, str] = {}
        if ci_common_version:
            prefix = f"{ci_common_version}-clang"
            for vi in self._idx.iter_version_info():
                if vi.version.startswith(prefix):
                    major = vi.package_versions.get("ASWF_CLANG_MAJOR_VERSION")
                    full = vi.package_versions.get("ASWF_CLANG_VERSION")
                    if major and full:
                        clang_versions[major] = full
        return {
            "versions": self.version_info.all_package_versions,
            "distro_versions": distro_versions,
            "conan_profile": self.version_info.conan_profile,
            "ci_common_version": ci_common_version,
            "clang_versions": clang_versions,
        }

    def _output_path(self) -> str:
        return os.path.join(
            utils.get_git_top_level(),
            "packages/conan/settings/profiles",
            self.version_info.conan_profile,
        )

    def _template_name(self) -> str:
        if self.version_info.conan_profile.startswith("ci_common"):
            return "conan-profile-ci-common.jinja2"
        return "conan-profile-vfx.jinja2"

    def _render(self) -> typing.Tuple[str, str]:
        tmpl = self._env.get_template(self._template_name())
        return self._output_path(), tmpl.render(self._template_context())

    def generate(self) -> str:
        """Render template and write the profile file; return its path."""
        path, content = self._render()
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def check(self) -> typing.Tuple[str, bool]:
        """Return (path, True) if the on-disk file matches the rendered output."""
        path, content = self._render()
        with open(path, encoding="utf-8") as f:
            return path, f.read() == content


class DockerGen:
    def __init__(self, image_name):
        self.image_name = image_name
        self.env = Environment(loader=PackageLoader("aswfdocker", "data"))
        self.image_data = self._get_image_data()

    def _get_image_data(self):
        image_data_path = os.path.join(
            utils.get_git_top_level(), f"ci-{self.image_name}/image.yaml"
        )
        with open(image_data_path, encoding="utf-8") as f:
            image_data = yaml.load(f, Loader=yaml.FullLoader)
        image_data["index"] = index.Index()
        image_data["constants"] = constants
        return image_data

    def _render_template(self, template_name, path):
        template = self.env.get_template(template_name)
        logger.debug("_render_template template=%s", template)
        dockerfile_path = os.path.join(
            utils.get_git_top_level(), f"ci-{self.image_name}/{path}"
        )
        return dockerfile_path, template.render(self.image_data)

    def _render_dockerfile(self):
        return self._render_template("ci-image-dockerfile.jinja2", "Dockerfile")

    def _render_readme(self):
        return self._render_template("ci-image-readme.jinja2", "README.md")

    def _generate(self, path, content):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def _check(self, path, content):
        with open(path, encoding="utf-8") as f:
            ok = f.read() == content
        return path, ok

    def generate_dockerfile(self):
        return self._generate(*self._render_dockerfile())

    def check_dockerfile(self):
        return self._check(*self._render_dockerfile())

    def generate_readme(self):
        return self._generate(*self._render_readme())

    def check_readme(self):
        return self._check(*self._render_readme())

    def push_overview(self, docker_org, token):
        _, readme = self._render_readme()

        description = self.image_data["title"] + "\n" + self.image_data["description"]
        if len(description) > 99:
            description = description[:96] + "..."
        body = {
            "description": description,
            "full_description": readme,
        }
        url = (
            f"https://hub.docker.com/v2/repositories/{docker_org}/ci-{self.image_name}/"
        )
        logger.debug("Patching description url %s", url)
        response = requests.patch(
            url,
            json=body,
            headers={"Authorization": f"JWT {token}"},
            timeout=5,
        )
        if response.status_code == 200:
            return True
        logger.error("Failed to update description: %s", response.json())
        return False
