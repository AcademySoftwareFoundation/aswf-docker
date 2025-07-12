# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT

from conan import ConanFile

class SystemOpenSSLConan(ConanFile):
    name = "openssl"
    version = "system"
    
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
    }
    default_options = {
        "shared": True,
    }
   
    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.system_libs = ["ssl", "crypto"]
        
        self.cpp_info.set_property("cmake_file_name", "OpenSSL")
        self.cpp_info.set_property("cmake_target_name", "OpenSSL::OpenSSL")
