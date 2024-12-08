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

# enableing doc
%define with_doc       %{?_without_doc:       0} %{?!_without_doc:       1}
# use OpenMP parallelization backaend
%define with_omp       %{?_without_omp:       0} %{?!_without_omp:       1}

%ifarch x86_64
%bcond_without rocm
%define with_x64 1
%else
%bcond_with rocm
%endif

%ifarch %{ix86}
%define with_x64 0
%endif

Summary:	LLM inference in C/C++ - with OpenMP parallelization
Name:		llama-cpp
License:        MIT AND Apache-2.0 AND LicenseRef-Fedora-Public-Domain
Epoch:		1
Version:	b4288
ExclusiveArch:  x86_64 aarch64
Release:        %autorelease
URL:            https://github.com/ggerganov/llama.cpp
Source0:        %{url}/archive/%{version}.tar.gz#/llama.cpp-%{version}.tar.gz
# https://github.com/ggerganov/llama.cpp/pull/10706
# ctest will fail test-eval-callback: curl 
# found in `examples/eval-callback/CMakeLists.txt`
Patch0:		0001-fix-for-building-with-no-internet-connection.patch
Provides:       llama-cpp-full = %{version}-%{release}
Provides:	bundled(ggml) = %{version}-%{release}

# Build Required packages
BuildRequires:  git-core
BuildRequires:  xxd
BuildRequires:  cmake
BuildRequires:  wget
BuildRequires:  langpacks-en
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
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
BuildRequires:	valgrind
BuildRequires:	valgrind-devel
BuildRequires:	valgrind-tools-devel
BuildRequires:	csmock-plugin-valgrind
BuildRequires:  gcc-c++
BuildRequires:	libstdc++
BuildRequires:	libstdc++-devel
BuildRequires:	libstdc++-static
BuildRequires:	g++
BuildRequires:  make
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:  clang
BuildRequires:  cpp
BuildRequires:  gdb
BuildRequires:  gcc-gdb-plugin
BuildRequires:  gcc-plugin-devel
BuildRequires:  gplugin-devel
BuildRequires:  gcc
BuildRequires:  glib
BuildRequires:  glib-devel
BuildRequires:  glibc
BuildRequires:  glibc-devel
BuildRequires:  multilib-rpm-config
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Fortran/
# https://gcc.gnu.org/wiki/GFortran
BuildRequires:	gcc-gfortran
BuildRequires:	libgfortran
BuildRequires:	libgfortran-static
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Web_Assets/
# GCC __float128 shared support library
BuildRequires:  libquadmath
BuildRequires:  libquadmath-devel
BuildRequires:  libquadmath-static
# GNU Atomic library
BuildRequires:  libatomic
BuildRequires:  libatomic-static
BuildRequires:  libatomic_ops
BuildRequires:  libatomic_ops-devel
BuildRequires:  libatomic_ops-static
# Address, Thread, Undefined, Leak Sanitizer
BuildRequires:  libasan
BuildRequires:  libasan-static
BuildRequires:  libhwasan
BuildRequires:  libhwasan-static
BuildRequires:  libtsan
BuildRequires:  libtsan-static
BuildRequires:  libubsan
BuildRequires:  libubsan-static
BuildRequires:  liblsan
BuildRequires:  liblsan-static
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# user required package
Requires:	curl
Requires:       pkgconfig(libcurl)
Requires:       pkgconfig(pthread-stubs)

# to use --numa numactl
# options: `common/arg.cpp`
Recommends:     numactl
BuildRequires:	numactl

# python
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python
# python requirements from:
# .devops/full.Dockerfile
# ./requirements/requirements-*
Recommends:	python3
BuildRequires:	python3-devel
BuildRequires:  python3dist(pip)
BuildRequires:  python3dist(poetry)
# TODO

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# hardware accelerate framework:
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# parallelization
# multiprocessing paradigms (OpenMP/pthread):

%if %{with_omp}
## OpenMP (Open Multi-Processing)
# option: GGML_OPENMP=ON
BuildRequires:	libgomp
# https://gcc.gnu.org/wiki/OpenACC
# Nvidia PTX and AMD Radeon devices.
Recommends:	libgomp-offload-nvptx
BuildRequires:	libgomp-offload-nvptx
%else
## pthread
Requires:	pthreadpool
BuildRequires:	pthreadpool
BuildRequires:  pthreadpool-devel
BuildRequires:  pkgconfig(pthread-stubs)
%endif
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
## High Bandwidth Memory (HBM):
# option: GGML_CPU_HBM=ON
Requires:       memkind
BuildRequires:  memkind
BuildRequires:  memkind-devel

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
## Blas (Basic Linear Algebra System)
# GGML_BLAS_VENDOR=
# OpenBLAS, FLAME, ATLAS, FlexiBLAS, Intel, NVHPC
# OpenBLAS
BuildRequires:  openblas
BuildRequires:  openblas-devel
%if %{with_omp}
### Blas + openmp
#BuildRequires:	openblas-openmp
BuildRequires:	openblas-openmp64
BuildRequires:	openblas-openmp64_
%else
### Blas + pthreads
#BuildRequires:	openblas-threads
BuildRequires:	openblas-threads64
BuildRequires:	openblas-threads64_
%endif
# these OpenBLAS packages may not be needed:
BuildRequires:  openblas-static
#BuildRequires:  openblas-serial
#BuildRequires:  openblas-serial64
#BuildRequires:  openblas-serial64_
BuildRequires:  openblas-srpm-macros
BuildRequires:  pkgconfig(liblas)
BuildRequires:  pkgconfig(cblas)
BuildRequires:  pkgconfig(cblas64)
BuildRequires:  pkgconfig(cblas64_)
## lapack
BuildRequires:	lapack
BuildRequires:	lapack-devel
BuildRequires:	lapack-static
BuildRequires:	lapack64
BuildRequires:	lapack64_

# FlexiBLAS

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
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

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Vulkan
# set(GGML_VULKAN_CHECK_RESULTS OFF)
# set(GGML_VULKAN_DEBUG         OFF)
# set(GGML_VULKAN_MEMORY_DEBUG  OFF)
# set(GGML_VULKAN_SHADER_DEBUG_INFO OFF)
# set(GGML_VULKAN_PERF      OFF)
# set(GGML_VULKAN_VALIDATE  OFF)
# set(GGML_VULKAN_RUN_TESTS OFF)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Rocm
# GGML_HIP_UMA
# BuildRequires:	rocsolver
%ifarch %{ix86} x86_64
# BuildRequires:	libgomp-offload-amdgcn
%endif

%description %_description
# -----------------------------------------------------------------------------
# sub packages
# -----------------------------------------------------------------------------

%package ggml
Summary:        %{summary} - ggml

%description ggml
%{_description}

%package devel
Summary:        %{summary} - devel

%description devel
%{_description}

%package test
Summary:        %{summary} - test

%description test
%{_description}

# TODO

# -----------------------------------------------------------------------------
# prep
# -----------------------------------------------------------------------------
%prep
%autosetup -p1 -n llama.cpp-%{version}
# pyhton fix
find . -name \*.py -exec sed -i 's|/usr/bin/env python3|/usr/bin/python3|' {} \;
# verson the *.so
find . -iname "CMakeLists.*" -exec sed -i 's|POSITION_INDEPENDENT_CODE ON|POSITION_INDEPENDENT_CODE ON SOVERSION %{version}|' '{}' \;
# shared libs need to be Off to enable hardware accelerate framework:
# sed -i -e 's/@BUILD_SHARED_LIBS@/OFF/' cmake/llama-config.cmake.in

# add environment variables manually to avoid cmake issue with `FindGit`
# export LLAMA_VERSION=0.0.4284
# export LLAMA_BUILD_COMMIT=d9c3ba2b
# export LLAMA_BUILD_NUMBER=4284
# export BRANCH_NAME=${{ github.head_ref || github.ref_name }}
export GGML_NLOOP=3
export GGML_N_THREADS=1
export LLAMA_LOG_COLORS=1
export LLAMA_LOG_PREFIX=1
export LLAMA_LOG_TIMESTAMPS=1

# remove phone packages
rm -rf exmples/llma.android
rm -rf examples/llama.swiftui
# remove documentation
# find . -name '*.md' -exec rm -rf {} \;
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
# -DBUILD_SHARED_LIBS:BOOL=OFF \
# -DCMAKE_SKIP_RPATH:BOOL=ON \
%cmake \
	-DCMAKE_BUILD_TYPE:STRING="-DNDEBUG" \
        -DCMAKE_C_FLAGS_RELEASE:STRING="-DNDEBUG" \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="-DNDEBUG" \
        -DCMAKE_Fortran_FLAGS_RELEASE:STRING="-DNDEBUG" \
	-DLLAMA_CURL:BOOL=ON \
	-DGGML_CPU_ALL_VARIANTS:BOOL=ON \
	-DGGML_NATIVE:BOOL=OFF \
	-DGGML_BACKEND_DL:BOOL=ON \
	-DSHARE_INSTALL_PREFIX:PATH=%{_prefix} \
	-DINCLUDE_INSTALL_DIR:PATH=%{_includedir} \
	-DLIB_INSTALL_DIR:PATH=%{_libdir} \
	-DSYSCONF_INSTALL_DIR:PATH=%{_sysconfdir} \
	-DCMAKE_INSTALL_DO_STRIP:BOOL=ON \
%if 0%{?__isa_bits} == 64
        -DLIB_SUFFIX=64
%else
        -DLIB_SUFFIX=""
%endif

%cmake_build --config Release

# -----------------------------------------------------------------------------
# Install
# -----------------------------------------------------------------------------
%install
%cmake_install --prefix %{_prefix}

# -----------------------------------------------------------------------------
# Verify
# -----------------------------------------------------------------------------
# other tests in: `scripts/`
%check
%ctest

# -----------------------------------------------------------------------------
# Files
# -----------------------------------------------------------------------------
%files
%license LICENSE
%{_bindir}/llama-*
%{_bindir}/convert_hf_to_gguf.py
%{_libdir}/libggml-base.so.%{version}
%{_libdir}/libggml.so.%{version}
%{_libdir}/libllama.so.%{version}

%files devel
%{_libdir}/libllama.so
%{_includedir}/llama.h
%{_includedir}/llama-cpp.h
%{_libdir}/cmake/llama/llama-config.cmake
%{_libdir}/cmake/llama/llama-version.cmake
%{_prefix}/lib/pkgconfig/llama.pc

%files ggml
%{_includedir}/ggml.h
%{_includedir}/ggml-*.h
%{_libdir}/libggml-base.so
%{_libdir}/libggml.so

%files test
%{_bindir}/test-*

%changelog
%autochangelog
