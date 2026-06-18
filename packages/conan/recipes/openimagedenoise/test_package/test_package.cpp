// Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
// SPDX-License-Identifier: Apache-2.0

#include <OpenImageDenoise/oidn.hpp>
#include <cstdio>

int main() {
    oidn::DeviceRef device = oidn::newDevice(oidn::DeviceType::CPU);
    device.commit();

    const char* errorMessage = nullptr;
    if (device.getError(errorMessage) != oidn::Error::None) {
        std::fprintf(stderr, "OIDN device error: %s\n", errorMessage);
        return 1;
    }

    std::printf("OpenImageDenoise CPU device created OK (version: %d.%d.%d)\n",
                OIDN_VERSION_MAJOR, OIDN_VERSION_MINOR, OIDN_VERSION_PATCH);
    return 0;
}
