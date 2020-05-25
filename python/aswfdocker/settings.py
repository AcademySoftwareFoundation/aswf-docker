# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

import os
import yaml


class Settings:
    def __init__(self, settings_path="~/.aswfdocker"):
        self.settings_path = os.path.expanduser(settings_path)
        self.github_access_token = ""
        self.load()

    def load(self):
        if os.path.exists(self.settings_path):
            with open(self.settings_path) as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                self.github_access_token = data.get("github_access_token", "")

    def save(self):
        data = {"github_access_token": self.github_access_token}
        with open(self.settings_path, "w") as f:
            yaml.dump(data, f)
