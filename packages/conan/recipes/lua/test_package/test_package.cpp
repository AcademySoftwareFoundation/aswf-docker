// Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
// SPDX-License-Identifier: Apache-2.0

extern "C" {
#include <lua.h>
#include <lualib.h>
#include <lauxlib.h>
}
#include <cstdio>

int main() {
    lua_State* L = luaL_newstate();
    luaL_openlibs(L);
    // Execute a simple Lua expression
    if (luaL_dostring(L, "return 6 * 7") != LUA_OK) {
        std::fprintf(stderr, "Lua error: %s\n", lua_tostring(L, -1));
        lua_close(L);
        return 1;
    }
    int result = (int)lua_tonumber(L, -1);
    std::printf("6 * 7 = %d\n", result);
    lua_close(L);
    return (result == 42) ? 0 : 1;
}
