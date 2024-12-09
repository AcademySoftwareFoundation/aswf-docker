# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

from conan import ConanFile

class SystemSqlite3Conan(ConanFile):
    name = "sqlite3"
    version = "wrapper"
    
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "enable_column_metadata": [True, False],
        "omit_load_extension": [True, False],
    }
    default_options = {
        "enable_column_metadata": True,
        "omit_load_extension": False,
    }
   
    def package_info(self):
        self.cpp_info.includedirs = ["/usr/include"]
        self.cpp_info.libdirs = ["/usr/lib64"]
        self.cpp_info.libs = ["sqlite3"]
        
        self.cpp_info.set_property("cmake_file_name", "SQLite3")
        self.cpp_info.set_property("cmake_target_name", "SQLite::SQLite3")
