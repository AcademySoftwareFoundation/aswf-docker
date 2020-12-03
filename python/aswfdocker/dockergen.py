# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Migration of ASWF Docker images between Docker organizations
"""
import logging
import os
import requests
import yaml
from jinja2 import Environment, PackageLoader

from aswfdocker import utils, index, constants


logger = logging.getLogger(__name__)


class DockerGen:
    def __init__(self, image_name):
        self.image_name = image_name
        self.env = Environment(loader=PackageLoader("aswfdocker", "data"))
        self.image_data = self._get_image_data()

    def _get_image_data(self):
        image_data_path = os.path.join(
            utils.get_git_top_level(), f"ci-{self.image_name}/image.yaml"
        )
        with open(image_data_path) as f:
            image_data = yaml.load(f, Loader=yaml.FullLoader)
        image_data["index"] = index.Index()
        image_data["constants"] = constants
        return image_data

    def _render_template(self, template_name, path):
        template = self.env.get_template(template_name)
        dockerfile_path = os.path.join(
            utils.get_git_top_level(), f"ci-{self.image_name}/{path}"
        )
        return dockerfile_path, template.render(self.image_data)

    def _render_dockerfile(self):
        return self._render_template("ci-image-dockerfile.jinja2", "Dockerfile")

    def _render_readme(self):
        return self._render_template("ci-image-readme.jinja2", "README.md")

    def _generate(self, path, content):
        with open(path, "w") as f:
            f.write(content)
        return path

    def _check(self, path, content):
        with open(path) as f:
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
            url, json=body, headers={"Authorization": f"JWT {token}"},
        )
        if response.status_code == 200:
            return True
        logger.error("Failed to update description: %s", response.json())
        return False
