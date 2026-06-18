// Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
// SPDX-License-Identifier: MIT

#include <embree4/rtcore.h>
#include <cstdio>

int main() {
    RTCDevice device = rtcNewDevice(nullptr);
    if (!device) {
        std::fprintf(stderr, "rtcNewDevice failed: error %d\n",
                     (int)rtcGetDeviceError(nullptr));
        return 1;
    }
    std::printf("Embree device created OK (Embree version: %d.%d.%d)\n",
                RTC_VERSION_MAJOR, RTC_VERSION_MINOR, RTC_VERSION_PATCH);
    rtcReleaseDevice(device);
    return 0;
}
