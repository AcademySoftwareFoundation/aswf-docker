// Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
// SPDX-License-Identifier: MIT

#include <rawtoaces/rawtoaces_core.h>

#include <cstdlib>
#include <iostream>

int main()
{
    // Minimal smoke test: compile against a public header, link against
    // rawtoaces_core, and exercise a self-contained calculation that
    // doesn't need a RAW file, camera metadata, or any other setup.
    rta::core::Spectrum spectrum;
    rta::core::calculate_daylight_SPD( 6500, spectrum );

    if ( spectrum.values.empty() )
    {
        std::cerr << "rawtoaces_core: calculate_daylight_SPD produced no samples"
                   << std::endl;
        return EXIT_FAILURE;
    }

    std::cout << "rawtoaces_core: calculated a " << spectrum.values.size()
               << "-sample daylight SPD for 6500K (integral "
               << spectrum.integrate() << ")" << std::endl;
    return EXIT_SUCCESS;
}
