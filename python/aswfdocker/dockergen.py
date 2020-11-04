# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Migration of ASWF docker images between docker organisations
"""
import logging
import os

import yaml
from jinja2 import Environment, PackageLoader

from aswfdocker import utils, index, constants


logger = logging.getLogger(__name__)


class DockerGen:
    def __init__(self, image_name):
        self.image_name = image_name
        self.env = Environment(loader=PackageLoader("aswfdocker", "data"))

    def generate_dockerfile(self):
        image_data_path = os.path.join(
            utils.get_git_top_level(), f"ci-{self.image_name}/data.yaml"
        )
        with open(image_data_path) as f:
            image_data = yaml.load(f, Loader=yaml.FullLoader)

        template = self.env.get_template("ci-image-dockerfile.tmpl")

        dockerfile_path = os.path.join(
            utils.get_git_top_level(), f"ci-{self.image_name}/Dockerfile"
        )

        with open(dockerfile_path, "w") as f:
            f.write(template.render(image_data))
        return dockerfile_path

    def generate_readme(self):
        image_data_path = os.path.join(
            utils.get_git_top_level(), f"ci-{self.image_name}/data.yaml"
        )
        with open(image_data_path) as f:
            image_data = yaml.load(f, Loader=yaml.FullLoader)

        template = self.env.get_template("ci-image-readme.tmpl")

        readme_path = os.path.join(
            utils.get_git_top_level(), f"ci-{self.image_name}/Readme.md"
        )

        image_data["index"] = index.Index()
        image_data["constants"] = constants

        with open(readme_path, "w") as f:
            f.write(template.render(image_data))
        return readme_path
