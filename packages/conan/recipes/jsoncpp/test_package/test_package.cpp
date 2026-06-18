// Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
// SPDX-License-Identifier: Apache-2.0

#include <json/json.h>
#include <cstdio>
#include <sstream>
#include <string>

int main() {
    // Parse a simple JSON value
    const std::string raw = R"({"name": "OpenMoonRay", "version": 1})";
    Json::CharReaderBuilder builder;
    Json::Value root;
    std::string errs;
    std::istringstream stream(raw);
    if (!Json::parseFromStream(builder, stream, &root, &errs)) {
        std::fprintf(stderr, "Parse error: %s\n", errs.c_str());
        return 1;
    }
    std::printf("name=%s version=%d\n",
                root["name"].asCString(),
                root["version"].asInt());
    return 0;
}
