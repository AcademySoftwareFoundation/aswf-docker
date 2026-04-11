/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
*/

#include <iostream>

#include <opentimelineio/clip.h>
#include <opentimelineio/timeline.h>

int main(int argc, char *argv[])
{
    OTIO_NS::SerializableObject::Retainer<OTIO_NS::Timeline> tl(
            dynamic_cast<OTIO_NS::Timeline*>(
                OTIO_NS::Timeline::from_json_file(argv[1])
        )
    );
    for (const auto& cl : tl->find_clips())
    {
        OTIO_NS::RationalTime dur = cl->duration();
        std::cout << "Name: " << cl->name() << " [";
        std::cout << dur.value() << "/" << dur.rate() << "]" << std::endl;
    }
    exit(EXIT_SUCCESS);
}
