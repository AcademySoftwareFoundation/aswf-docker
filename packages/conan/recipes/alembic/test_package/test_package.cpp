/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/2a3cb93885141024c1b405a01a79fb3abc239b12/recipes/alembic/all/test_package/test_package.cpp
*/

#include <iostream>

#include <Alembic/Abc/All.h>
#include <Alembic/AbcCoreOgawa/All.h>
#include <Alembic/AbcCollection/All.h>

void write()
{
    Alembic::Abc::OArchive archive(Alembic::AbcCoreOgawa::WriteArchive(), "Collection.abc");
    Alembic::Abc::OObject root(archive, Alembic::Abc::kTop);
    Alembic::Abc::OObject test(root, "test");
}

void read()
{
    Alembic::Abc::IArchive archive(Alembic::AbcCoreOgawa::ReadArchive(), "Collection.abc");
    Alembic::Abc::IObject test(archive.getTop(), "test");
}

int main() {
    write();
    read();
    return EXIT_SUCCESS;
}
