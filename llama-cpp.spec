# Licensecheck reports
#
# *No copyright* The Unlicense
# ----------------------------
# common/base64.hpp
# common/stb_image.h
# These are public domain
#
# MIT License
# -----------
# LICENSE
# ...
# This is the main license

%global summary LLM inference in C/C++

%global _description %{expand:
The main goal of llama.cpp is to enable LLM inference with minimal setup and state-of-the-art performance on a wide variety of hardware - locally and in the cloud.

* Plain C/C++ implementation without any dependencies
* Apple silicon is a first-class citizen - optimized via ARM NEON, Accelerate and Metal frameworks
* AVX, AVX2, AVX512 and AMX support for x86 architectures
* 1.5-bit, 2-bit, 3-bit, 4-bit, 5-bit, 6-bit, and 8-bit integer quantization for faster inference and reduced memory use
* Custom CUDA kernels for running LLMs on NVIDIA GPUs (support for AMD GPUs via HIP and Moore Threads MTT GPUs via MUSA)
* Vulkan and SYCL backend support
* CPU+GPU hybrid inference to partially accelerate models larger than the total VRAM capacity}

Summary:	LLM inference in C/C++
Name:		llama-cpp
License:        MIT AND Apache-2.0 AND LicenseRef-Fedora-Public-Domain
Epoch:		1
Version:	b4267
ExclusiveArch:  x86_64 aarch64
Release:        %autorelease
URL:            https://github.com/ggerganov/llama.cpp
Source0:        %{url}/archive/%{version}.tar.gz#/llama.cpp-%{version}.tar.gz
Provides:       llama-cpp-full = %{version}-%{release}

# Build Required packages
BuildRequires:  xxd
BuildRequires:  cmake
BuildRequires:  wget
BuildRequires:  langpacks-en
# glibc packages added just in case
# glibc-all-langpacks and glibc-langpack-is are needed for GETTEXT_LOCALE and
# GETTEXT_ISO_LOCALE test prereq's, glibc-langpack-en ensures en_US.UTF-8.
BuildRequires:  glibc-all-langpacks
BuildRequires:  glibc-langpack-en
BuildRequires:  glibc-langpack-is
BuildRequires:  glibc-all-langpacks
# packages found in .github/workflows/server.yml
BuildRequires:  curl
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  libcurl-devel
# packages that either are or possibly needed
BuildRequires:  gcc-c++
BuildRequires:	gcc-gfortran
BuildRequires:  make
BuildRequires:  clang
BuildRequires:  gdb
BuildRequires:  gcc
BuildRequires:  glib
BuildRequires:  glib-devel
BuildRequires:  glibc
BuildRequires:  glibc-devel
BuildRequires:  multilib-rpm-config

# user required package
Requires:	curl
Requires:       pkgconfig(libcurl)
Requires:       pkgconfig(pthread-stubs)

# to use --numa numactl
# options: `common/arg.cpp`
Recommends:     numactl
BuildRequires:	numactl

# hardware acceleration / optimization packages:
blis-threads.i686
## memkind
Requires:       memkind
BuildRequires:  memkind
BuildRequires:  memkind-devel
## pthread
Requires:	pthreadpool
BuildRequires:	pthreadpool
BuildRequires:  pthreadpool-devel
BuildRequires:  pkgconfig(pthread-stubs)
## openmp
Requires:	openmpi
BuildRequires:  openmpi
BuildRequires:	openmpi-devel
# .devops/full.Dockerfile
BuildRequires:	libgomp

## Blas
Requires:	openblas
BuildRequires:  openblas
BuildRequires:  openblas-devel
BuildRequires:  openblas-srpm-macros
BuildRequires:  pkgconfig(liblas)
BuildRequires:  pkgconfig(cblas)
BuildRequires:  pkgconfig(cblas64)
BuildRequires:  pkgconfig(cblas64_)
### Blas + openmp
Requires:	openblas-openmp
BuildRequires:	openblas-openmp
BuildRequires:	openblas-openmp64
BuildRequires:	openblas-openmp64_
### Blas + pthreads
Requires:	openblas-threads
BuildRequires:	openblas-threads
BuildRequires:	openblas-threads64
BuildRequires:	openblas-threads64_

## Blis
Requires:	blis
BuildRequires:	blis
BuildRequires:	blis-devel
BuildRequires:	blis-srpm-macros
### Blis + openmp
Requires:	blis-openmp
BuildRequires:  blis-openmp
BuildRequires:  blis-openmp64
### Blis + pthreads
Requires:	blis-threads
BuildRequires:	blis-threads
BuildRequires:	blis-threads64

%ifarch %{ix86} x86_64
# https://gcc.gnu.org/wiki/OpenACC
# Nvidia PTX and AMD Radeon devices.
BuildRequires:	libgomp-offload-nvptx
# AMD rocm
# BuildRequires:	libgomp-offload-amdgcn
%endif

# python requirements from:
# .devops/full.Dockerfile
# ./requirements/requirements-*

%description %_description
# -----------------------------------------------------------------------------
# sub packages
# -----------------------------------------------------------------------------

%package -n llama-cpp-devel
Summary:        %{summary} - devel

%description -n llama-cpp-devel
%{_description}

# TODO

# -----------------------------------------------------------------------------
# prep
# -----------------------------------------------------------------------------
%prep
%autosetup -p1 -n llama.cpp-%{version}
find . -name \*.py -exec sed -i 's|/usr/bin/env python3|/usr/bin/python3|' {} \;
# verson the *.so
find . -iname "CMakeLists.*" -exec sed -i 's|POSITION_INDEPENDENT_CODE ON|POSITION_INDEPENDENT_CODE ON SOVERSION %{version}|' '{}' \;

# remove phone packages
rm -rf exmples/llma.android
rm -rf examples/llama.swiftui
# remove documentation
find . -name '*.md' -exec rm -rf {} \;
# git cruft
find . -name '.gitignore' -exec rm -rf {} \;

# -----------------------------------------------------------------------------
# build
# -----------------------------------------------------------------------------
%build
# https://github.com/ggerganov/llama.cpp/pull/10627
# -DOAI_FULL_COMPAT
# build options:
# ggml/CMakeLists.txt
# .devops/full.Dockerfile
%cmake \
	-DCMAKE_BUILD_TYPE=Release \
	-DLLAMA_CURL=ON \
	-DGGML_CPU_ALL_VARIANTS=ON \
	-DGGML_NATIVE=OFF \
	-DGGML_BACKEND_DL=ON \
	-DCMAKE_INSTALL_BINDIR=%{_bindir} \
	-DCMAKE_INSTALL_LIBDIR=%{_libdir} \
	-DINCLUDE_INSTALL_DIR=%{_includedir} \
	-DLIB_INSTALL_DIR=%{_libdir} \
	-DSHARE_INSTALL_PREFIX=%{_datadir} \
	-DSYSCONF_INSTALL_DIR=%{_sysconfdir} \
	-DCMAKE_INSTALL_DO_STRIP=ON \
	-DCMAKE_Fortran_FLAGS_RELEASE=ON \
%if "%{_lib}" == "lib64"
        -DLIB_SUFFIX=64
%else
        -DLIB_SUFFIX=""
%endif

%cmake_build --config Release

# -----------------------------------------------------------------------------
# Install
# -----------------------------------------------------------------------------
%install
%cmake_install

# -----------------------------------------------------------------------------
# Verify
# -----------------------------------------------------------------------------
# will fail test-eval-callback: curl eval-callback

%if 0%{?with_check}
%check
%ctest
%endif

# -----------------------------------------------------------------------------
# Files
# -----------------------------------------------------------------------------
%files
%license LICENSE
%{_bindir}/convert_hf_to_gguf.py
%{_bindir}/llama-*
%{_bindir}/test-*
%{_includedir}/ggml.h
%{_includedir}/ggml-*.h
%{_includedir}/llama.h
%{_includedir}/llama-cpp.h
%{_libdir}/cmake/llama/llama-config.cmake
%{_libdir}/cmake/llama/llama-version.cmake
%{_libdir}/libggml-base.so
%{_libdir}/libggml-base.so.%{version}
%{_libdir}/libggml.so
%{_libdir}/libggml.so.%{version}
%{_libdir}/libllama.so
%{_libdir}/libllama.so.%{version}
%{_prefix}/lib/pkgconfig/llama.pc

%changelog
%autochangelog
