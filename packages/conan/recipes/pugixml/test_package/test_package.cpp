/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# https://github.com/conan-io/conan-center-index/blob/f83ca9df2f14d01f49b186cb279740c295ae09c9/recipes/pugixml/all/test_package/test_package.cpp
*/

#include <sstream>
#include <iostream>
#include "pugixml.hpp"

int main() {
    const unsigned majorVersion = PUGIXML_VERSION / 1000;
    const unsigned minorVersion = PUGIXML_VERSION % 1000 / 10;
    const unsigned maintenanceVersion = PUGIXML_VERSION % 1000 % 10;

    std::basic_stringstream<PUGIXML_CHAR> version;
    version << majorVersion << '.' << minorVersion;
    if (maintenanceVersion)
        version << '.' << maintenanceVersion;

    pugi::xml_document doc;
    pugi::xml_node node = doc.append_child(PUGIXML_TEXT("PugiXml"));
    node.append_attribute(PUGIXML_TEXT("Version"))
        .set_value(version.str().c_str());

    node.append_attribute(PUGIXML_TEXT("wchar_mode"))
        .set_value(sizeof(PUGIXML_CHAR) != 1);

    node.append_attribute(PUGIXML_TEXT("header_only"))
#ifdef PUGIXML_HEADER_ONLY
        .set_value(true);
#else
        .set_value(false);
#endif

    node.append_attribute(PUGIXML_TEXT("no_exceptions"))
#ifdef PUGIXML_NO_EXCEPTIONS
        .set_value(true);
#else
        .set_value(false);
#endif

    doc.print(std::cout);
}
