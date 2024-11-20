/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/6aeda9d870a1253535297cb50b01bebfc8c62910/recipes/gtest/all/test_package/test_package.cpp
*/

// Thanks to http://joeyates.info/2010/05/26/googletest-hello-world/ for the example!

/////////////////////////////
// In the header file

#include <sstream>
using namespace std;

class Salutation
{
public:
  static string greet(const string& name);
};

///////////////////////////////////////
// In the class implementation file

string Salutation::greet(const string& name) {
  ostringstream s;
  s << "Hello " << name << "!";
  return s.str();
}

///////////////////////////////////////////
// In the test file
#include <gtest/gtest.h>

#ifdef WITH_GMOCK
#include <gmock/gmock.h>

class Example
{
public:
    virtual void foo() = 0;
};

class MockExample : public Example
{
public:
    MOCK_METHOD0(foo, void());
};

#endif

TEST(SalutationTest, Static) {

#ifdef WITH_GMOCK
  MockExample m;
#endif

  EXPECT_EQ(string("Hello World!"), Salutation::greet("World"));
}
