#include <OpenEXR/ImfVersion.h>
#include <iostream>

int main(int argc, char *argv[])
{
  std::cout << "isImfMagic()=" << Imf::isImfMagic("") << "\n" << std::endl;
  return 0;
}
