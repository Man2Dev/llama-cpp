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
%define with_doc	%{?_without_doc:	0} %{?!_without_doc:	1}
# enable {ADDRESS, THREAD, UNDEFINED} sanitizer (THREAD is broken)
%define with_san	%{?_without_san:	0} %{?!_without_san:	1}
# ADDRESS sanitizer
%define with_san_add	%{?_without_san:	0} %{?!_without_san:	1}
# THREAD sanitizer
%define with_san_thr	%{?_without_san:	0} %{?!_without_san:	1}
# UNDEFINED sanitizer
%define with_san_und	%{?_without_san:	0} %{?!_without_san:	1}
# use the 64 bit (OpenMP)/Pthreads parallelization backaend
%define with_omp	%{?_without_omp:	0} %{?!_without_omp:	1}
# use the HBM backaend
%define with_hbm	%{?_without_hbm:	0} %{?!_without_hbm:	1}
# use Blis backaend
%define with_blis	%{?_without_blis:	0} %{?!_without_blis:	1}
# use Blas backaend
%define with_blas	%{?_without_blas:	0} %{?!_without_blas:	1}
# use (OpenBlas)/FlexiBlas backaend
%define with_openblas	%{?_without_blas:       0} %{?!_without_blas:   1}
# use Rocm backaend
%define with_rocm	%{?_without_rocm:	0} %{?!_without_rocm:	1}
# with clients
%define with_exa	%{?_without_exa:	0} %{?!_without_exa:	1}
# with tests
%define with_test	%{?_without_test:	0} %{?!_without_test:	1}
# with package python-guff-py
%define with_guffpy	%{?_without_guffpy:	0} %{?!_without_guffpy:	1}

%define with_guffpy 0

# use only 64 bit version of backend
%if 0%{?__isa_bits} == 64
%define with_x64 1
%endif

%ifarch x86_64
%bcond_without rocm
%else
%bcond_with rocm
%endif

Summary:	LLM inference in C/C++ - OpenMP parallelization
Name:		llama-cpp
License:        MIT AND Apache-2.0 AND LicenseRef-Fedora-Public-Domain
Epoch:		1
Version:	b4304
ExclusiveArch:  x86_64 aarch64
Release:        %autorelease
URL:            https://github.com/ggerganov/llama.cpp
Source0:        %{url}/archive/%{version}.tar.gz#/llama.cpp-%{version}.tar.gz
# https://github.com/ggerganov/llama.cpp/pull/10706
# ctest will fail test-eval-callback: curl 
# found in `examples/eval-callback/CMakeLists.txt`
Patch0:		0001-fix-for-building-with-no-internet-connection.patch
Requires:	ggml

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
%ifarch x86_64
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Web_Assets/
# GCC __float128 shared support library
BuildRequires:  libquadmath
BuildRequires:  libquadmath-devel
BuildRequires:  libquadmath-static
%endif
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
# to use --numa numactl
# options: `common/arg.cpp`
Requires:	curl
Recommends:     numactl
BuildRequires:	numactl

# python
# For the extra python package gguf that comes with llama-cpp
# .github/workflows/gguf-publish.yml
# .devops/full.Dockerfile
# scripts/check-requirements.sh
# .devops/tools.sh
%global pypi_name gguf
%global pypi_version 0.1.0
Recommends:	python3
BuildRequires:	python3-devel
BuildRequires:	python3-huggingface-hub
BuildRequires:  python3dist(pip)
BuildRequires:  python3dist(poetry)
BuildRequires:  python3dist(pillow)
BuildRequires:  python3dist(torch)
BuildRequires:  python3dist(torchvision)
BuildRequires:  python3dist(torchvision)
BuildRequires:  python3dist(matplotlib)
BuildRequires:  python3dist(requests)
BuildRequires:  python3dist(aiohttp)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(numpy)
BuildRequires:  python3dist(prometheus-client)
BuildRequires:  python3dist(sentencepiece)
BuildRequires:  python3dist(cffi)
# https://pypi.org/project/openai/
# https://pypi.org/project/transformers/

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# hardware accelerate framework:
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# parallelization
# multiprocessing paradigms (OpenMP/pthread):
%if %{with_omp}
## OpenMP (Open Multi-Processing)
# option: GGML_OPENMP=ON
BuildRequires:	libgomp
%ifarch x86_64
# https://gcc.gnu.org/wiki/OpenACC
# Nvidia PTX and AMD Radeon devices.
BuildRequires:	libgomp-offload-nvptx
%endif
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
%if %{with_hbm}
Requires:       memkind
BuildRequires:  memkind
BuildRequires:  memkind-devel
%endif
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
## Blas (Basic Linear Algebra System)
# GGML_BLAS_VENDOR=
# OpenBLAS, FLAME, ATLAS, FlexiBLAS, Intel, NVHPC
%if %{with_blas}
## OpenBLAS
%if %{with_openblas}
BuildRequires:  openblas
BuildRequires:  openblas-devel
BuildRequires:	openblas-static
BuildRequires:  openblas-srpm-macros
BuildRequires:  pkgconfig(liblas)
### Blas + openmp
%if %{with_omp}
%if %{with_x64}
BuildRequires:	openblas-openmp64
BuildRequires:	openblas-openmp64_
BuildRequires:  pkgconfig(cblas64)
BuildRequires:  pkgconfig(cblas64_)
%else
BuildRequires:	openblas-openmp
BuildRequires:  pkgconfig(cblas)
%endif
%else
### Blas + Pthreads
%if %{with_x64}
BuildRequires:	openblas-threads64
BuildRequires:	openblas-threads64_
%else
BuildRequires:	openblas-threads
%endif
%endif
# TODO
# these OpenBLAS packages may not be needed:
## lapack
BuildRequires:  lapack
BuildRequires:  lapack-devel
BuildRequires:  lapack-static
%if %{with_x64}
BuildRequires:	openblas-serial64
BuildRequires:  openblas-serial64_
## lapack
BuildRequires:	lapack64
BuildRequires:	lapack64_
%else
BuildRequires:  openblas-serial
%endif
%else
## FlexiBLAS
flexiblas
%endif
%endif

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
## Blis
%if %{with_blis}
Requires:	blis
BuildRequires:	blis
BuildRequires:	blis-devel
BuildRequires:	blis-srpm-macros
%if %{with_omp}
### Blis + openmp
Requires:	blis-openmp
BuildRequires:  blis-openmp
BuildRequires:  blis-openmp64
%else
### Blis + pthreads
Requires:	blis-threads
BuildRequires:	blis-threads
BuildRequires:	blis-threads64
%endif
%endif

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
%ifarch x86_64
# BuildRequires:	rocsolver
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

%package convert-hf-to-gguf
Summary:        %{summary} - convert-hf-to-gguf

%description convert-hf-to-gguf
%{_description}

# TODO
%if %{with_guffpy}
%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
Tool to interact and enumerate LDAP instances.
%endif

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
export LLAMA_VERSION=0.0."$(git rev-list --count HEAD)"
# export LLAMA_BUILD_COMMIT=d9c3ba2b
export SHORT_HASH="$(git rev-parse --short=7 HEAD)"
export LLAMA_BUILD_NUMBER="$(git rev-list --count HEAD)"
export BRANCH_NAME=%{version}
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

# pyhton setup
%if %{with_guffpy}
rm -rf %{pypi_name}.egg-info
%generate_buildrequires
%pyproject_buildrequires -r
%endif

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
# -DLLAMA_ALL_WARNINGS_3RD_PARTY=ON \
%cmake \
	-DCMAKE_BUILD_TYPE:STRING="-DNDEBUG" \
	-DCMAKE_C_FLAGS_RELEASE:STRING="-DNDEBUG" \
	-DCMAKE_CXX_FLAGS_RELEASE:STRING="-DNDEBUG" \
	-DCMAKE_Fortran_FLAGS_RELEASE:STRING="-DNDEBUG" \
	-DLLAMA_CURL:BOOL=ON \
	-DGGML_CPU_ALL_VARIANTS:BOOL=ON \
	-DGGML_NATIVE:BOOL=OFF \
	-DGGML_BACKEND_DL:BOOL=ON \
	-DLLAMA_FATAL_WARNINGS:BOOL=ON \
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
%if %{with_hbm}

%endif
%if %{with_omp}
%if %{with_openblas}
	-DGGML_BLAS=ON \
	-DGGML_BLAS_VENDOR=OpenBLAS \
%else
	-DGGML_BLAS=ON \
	-DGGML_BLAS_VENDOR=FlexiBLAS \
%endif
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
# ./scripts/debug-test.sh
# ./scripts/compare-commits.sh
# ./scripts/compare-llama-bench.py --check
%check
%ctest

# -----------------------------------------------------------------------------
# Files
# -----------------------------------------------------------------------------
%files
%license LICENSE
%{_bindir}/llama-*
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

%files convert-hf-to-gguf
%{_bindir}/convert_hf_to_gguf.py

%changelog
%autochangelog
