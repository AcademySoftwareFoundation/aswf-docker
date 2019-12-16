#!/usr/bin/env bash

# Downloads a given versioned package into the packages folder
# Usage: ./download-package.sh aswftesting boost 2019

set -ex

docker_org=${1}
package_name=${2}
package_version=${3}

mkdir -p packages/${package_version}

docker pull ${docker_org}/ci-package-${package_name}:${package_version}

container_id=`docker create ${docker_org}/ci-package-${package_name}:${package_version} null`

docker export --output="packages/${package_version}/${package_name}.tar" ${container_id}

gzip -9 packages/${package_version}/${package_name}.tar

docker rm ${container_id}
