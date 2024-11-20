/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/22dfbd2b42eed730eca55e14025e8ffa65f723b2/recipes/glfw/all/test_package/test_package.c
*/

#include <GLFW/glfw3.h>

int main (void)
{
    GLFWwindow* window;
    GLFWmonitor* monitor = NULL;

    monitor = glfwGetPrimaryMonitor();

    window = glfwCreateWindow(640, 480, "Window name", monitor, NULL);

    glfwDestroyWindow(window);
    glfwTerminate();

    return 0;
}
