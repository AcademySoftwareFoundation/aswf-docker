// Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
// SPDX-License-Identifier: Apache-2.0

#include <Random123/philox.h>
#include <Random123/threefry.h>
#include <cstdio>

int main() {
    // Exercise the Philox 4x32 CBRNG
    philox4x32_key_t key = {{0, 1}};
    philox4x32_ctr_t ctr = {{0, 1, 2, 3}};
    philox4x32_ctr_t result = philox4x32(ctr, key);
    std::printf("philox4x32: %u %u %u %u\n",
                result.v[0], result.v[1], result.v[2], result.v[3]);

    // Exercise the Threefry 4x64 CBRNG
    threefry4x64_key_t key2 = {{0, 1, 2, 3}};
    threefry4x64_ctr_t ctr2 = {{0, 1, 2, 3}};
    threefry4x64_ctr_t result2 = threefry4x64(ctr2, key2);
    std::printf("threefry4x64: %llu %llu %llu %llu\n",
                (unsigned long long)result2.v[0], (unsigned long long)result2.v[1],
                (unsigned long long)result2.v[2], (unsigned long long)result2.v[3]);

    return 0;
}
