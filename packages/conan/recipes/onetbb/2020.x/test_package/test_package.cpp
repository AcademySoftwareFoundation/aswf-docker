/*
# Copyright (c) Contributors to the conan-center-index Project. All rights reserved.
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: MIT
#
# From: https://github.com/conan-io/conan-center-index/blob/cceee569179c10fa56d1fd9c3582f3371944ba59/recipes/onetbb/2020.x/test_package/test_package.cpp
*/

#include "tbb/task_group.h"
#include "tbb/flow_graph.h"
#include "tbb/compat/tuple"
#include <iostream>

using namespace tbb;
using namespace tbb::flow;

int Fib(int n) {
    if( n<2 ) {
        return n;
    } else {
        int x, y;
        task_group g;
        g.run([&]{x=Fib(n-1);}); // spawn a task
        g.run([&]{y=Fib(n-2);}); // spawn another task
        g.wait();                // wait for both tasks to complete
        return x+y;
    }
}

int main(){
    std::cout<<"Fib 6="<<Fib(6)<<"\n";

    graph g;
    continue_node< continue_msg> hello( g,
      []( const continue_msg &) {
          std::cout << "Hello";
      }
    );
    continue_node< continue_msg> world( g,
      []( const continue_msg &) {
          std::cout << " World\n";
      }
    );
    make_edge(hello, world);
    hello.try_put(continue_msg());
    g.wait_for_all();
    return 0;
}
