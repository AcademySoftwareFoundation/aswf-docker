#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

if [ ! -f "$DOWNLOADS_DIR/osl-${ASWF_OSL_VERSION}.tar.gz" ]; then
    curl --location "https://github.com/AcademySoftwareFoundation/OpenShadingLanguage/archive/refs/tags/v${ASWF_OSL_VERSION}.tar.gz" -o "$DOWNLOADS_DIR/osl-${ASWF_OSL_VERSION}.tar.gz"
fi

tar -zxf "$DOWNLOADS_DIR/osl-${ASWF_OSL_VERSION}.tar.gz"
cd "OpenShadingLanguage-${ASWF_OSL_VERSION}"

if [[ $ASWF_DTS_VERSION == 9 && $ASWF_CUDA_VERSION == 10* ]]; then
    CUDA_COMPUTE_VERSION=compute_30
else
    CUDA_COMPUTE_VERSION=compute_50
fi

# From https://github.com/AcademySoftwareFoundation/OpenShadingLanguage/pull/2010
# Resolve issues wth C++20 and fmt
if [[ $ASWF_OSL_VERSION == 1.14.6.0 ]]; then
    cat << 'EOF' | patch -p1
diff --git a/src/include/OSL/oslconfig.h.in b/src/include/OSL/oslconfig.h.in
index 6cf74b219a1..501394deede 100644
--- a/src/include/OSL/oslconfig.h.in
+++ b/src/include/OSL/oslconfig.h.in
@@ -123,7 +123,11 @@
 OSL_NODISCARD inline std::string
 fmtformat(const Str& fmt, Args&&... args)
 {
+#if OSL_CPLUSPLUS_VERSION >= 20 || FMT_VERSION >= 100000
+    return ::fmt::vformat(fmt, ::fmt::make_format_args(args...));
+#else
     return OIIO::Strutil::fmt::format(fmt, std::forward<Args>(args)...);
+#endif
 }

 // TODO: notice the fmt argument is not templatised, this is because
@@ -132,13 +136,18 @@
 // OIIO should fix this if possible.
 template<typename OutIt, typename... Args>
 OSL_NODISCARD inline auto
-fmtformat_to_n(OutIt &out, size_t n, const string_view& fmt, Args&&... args)
+fmtformat_to_n(OutIt& out, size_t n, string_view fmt, Args&&... args)
 {
     // DOES NOT EXIST AS PUBLIC API
     //return OIIO::Strutil::fmt::format_to_n(out, n, fmt, std::forward<Args>(args)...);
     // So call directly into underlying fmt library OIIO is using
     // TODO:  Add format_to_n as a public API in OIIO
+#if OSL_CPLUSPLUS_VERSION >= 20 || FMT_VERSION >= 100000
+    std::string str = fmtformat(fmt, std::forward<Args>(args)...);
+    return ::fmt::format_to_n(out, n, "{}", str);
+#else
     return ::fmt::format_to_n(out, n, ::fmt::string_view{fmt.begin(), fmt.length()}, std::forward<Args>(args)...);
+#endif
 }
 
 
diff --git a/src/liboslcomp/oslcomp_pvt.h b/src/liboslcomp/oslcomp_pvt.h
index 6cf74b219a1..501394deede 100644
--- a/src/liboslcomp/oslcomp_pvt.h
+++ b/src/liboslcomp/oslcomp_pvt.h
@@ -365,7 +365,8 @@
     template<typename... Args>
     inline void osofmt(const char* fmt, Args&&... args) const
     {
-        fmt::print(*m_osofile, fmt, std::forward<Args>(args)...);
+        *m_osofile << OIIO::Strutil::fmt::format(fmt,
+                                                 std::forward<Args>(args)...);
     }

     void track_variable_lifetimes()
diff --git a/src/liboslexec/llvm_util.cpp b/src/liboslexec/llvm_util.cpp
index 6cf74b219a1..501394deede 100644
--- a/src/liboslexec/llvm_util.cpp
+++ b/src/liboslexec/llvm_util.cpp
@@ -17,6 +17,11 @@
 #    error "LLVM minimum version required for OSL is 11.0"
 #endif

+OSL_PRAGMA_WARNING_PUSH
+#if OSL_GNUC_VERSION >= 140000
+OSL_GCC_PRAGMA(GCC diagnostic ignored "-Wmaybe-uninitialized")
+#endif
+
 #include "llvm_passes.h"

 #include <llvm/InitializePasses.h>
EOF
fi

OSL_CXX_STANDARD=$ASWF_CXX_STANDARD
## OSL 1.14.6.0 does not build with C++20
#if [[ $ASWF_OSL_VERSION == 1.14.6.0 && $ASWF_CXX_STANDARD == 20 ]]; then
#    OSL_CXX_STANDARD=17
#fi

mkdir build
cd build

cmake -DCMAKE_INSTALL_PREFIX="${ASWF_INSTALL_PREFIX}" \
      -DBoost_USE_STATIC_LIBS=OFF \
      -DBUILD_SHARED_LIBS=ON \
      -DCMAKE_CXX_STANDARD=$OSL_CXX_STANDARD \
      -Dpybind11_DIR="${ASWF_INSTALL_PREFIX}/lib/cmake/pybind11" \
      -DOSL_USE_OPTIX=ON \
      -DOPTIX_VERSION=${ASWF_OPTIX_VERSION} \
      -DOPTIXHOME=${ASWF_INSTALL_PREFIX}/NVIDIA-OptiX-SDK-${ASWF_OPTIX_VERSION} \
      ../.

# Multithread build of OSL 1.14.6.0 build fails in OptiX / CUDA section. Or maybe not?
if [[ $ASWF_OSL_VERSION == 1.14.6.0 ]]; then
#    cmake --build . -j1 --verbose
    cmake --build . -j$(nproc) --verbose
else
    cmake --build . -j$(nproc) --verbose
fi
cmake --install .

cd ../..
rm -rf "OpenShadingLanguage-${ASWF_OSL_VERSION}"
