/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/2a3cb93885141024c1b405a01a79fb3abc239b12/recipes/opensubdiv/all/test_package/test_package.cpp
*/

#include <opensubdiv/far/topologyDescriptor.h>

static int g_nverts = 8,
    g_nfaces = 6;

static int g_vertsperface[6] = {4, 4, 4, 4, 4, 4};

static int g_vertIndices[24] = {0, 1, 3, 2,
                                2, 3, 5, 4,
                                4, 5, 7, 6,
                                6, 7, 1, 0,
                                1, 7, 5, 3,
                                6, 0, 2, 4};

using namespace OpenSubdiv;

//------------------------------------------------------------------------------
int main(int, char **) {
    typedef Far::TopologyDescriptor Descriptor;

    Sdc::SchemeType type = OpenSubdiv::Sdc::SCHEME_CATMARK;

    Sdc::Options options;
    options.SetVtxBoundaryInterpolation(Sdc::Options::VTX_BOUNDARY_EDGE_ONLY);

    Descriptor desc;
    desc.numVertices = g_nverts;
    desc.numFaces = g_nfaces;
    desc.numVertsPerFace = g_vertsperface;
    desc.vertIndicesPerFace = g_vertIndices;

    Far::TopologyRefiner *refiner =
        Far::TopologyRefinerFactory<Descriptor>::Create(desc,
                                                        Far::TopologyRefinerFactory<Descriptor>::Options(type,
                                                                                                         options));

    refiner->RefineUniform(Far::TopologyRefiner::UniformOptions(2));

    delete refiner;
    return 0;
}
