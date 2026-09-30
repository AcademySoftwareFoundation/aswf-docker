// Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
// Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
// SPDX-License-Identifier: MIT

#include <embree4/rtcore.h>

#include <iostream>
#include <limits>

int main() {
  RTCDevice device = rtcNewDevice(NULL);
  RTCScene scene = rtcNewScene(device);
  RTCGeometry geom = rtcNewGeometry(device, RTC_GEOMETRY_TYPE_TRIANGLE);

  rtcReleaseGeometry(geom);
  rtcReleaseScene(scene);
  rtcReleaseDevice(device);

  return 0;
}
