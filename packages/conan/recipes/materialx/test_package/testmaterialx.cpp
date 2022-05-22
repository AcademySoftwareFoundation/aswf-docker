#include <MaterialXCore/Types.h>
#include <iostream>

namespace mx = MaterialX;

int main(int argc, char *argv[])
{
  mx::Vector3 v(1, 2, 3);
  std::cerr << "res=" << v.getMagnitude() << std::endl; 
  std::cout << "ok\n" << std::endl;
  return 0;
}
