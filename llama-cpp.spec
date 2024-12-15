# Licensecheck reports
#
# *No copyright* The Unlicense
# ----------------------------
# common/base64.hppTHREAD
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

# enableing doc [breaks python package]
%define with_doc	%{?_without_doc:	0} %{?!_without_doc:	1}
%define with_doc 1
# enableing ssl
%define with_ssl	%{?_without_ssl:	0} %{?!_without_ssl:	1}
%define with_ssl 0
# with examples (clients)
%define with_exa	%{?_without_exa:	0} %{?!_without_exa:	1}
%define with_exa 1
# with tests
%define with_test	%{?_without_test:	0} %{?!_without_test:	1}
%define with_test 1
# use the HBM backaend [breaks build]
%define with_hbm	%{?_without_hbm:	0} %{?!_without_hbm:	1}
%define with_hbm 0
# with a parallelization backaend
%define with_par	%{?_without_par:	0} %{?!_without_par:	1}
%define with_par 1
# keep lapack at build
%define with_lapack	%{?_without_lapack:	0} %{?!_without_lapack:	1}
%define with_lapack 1
# use 64 bit (OpenMP)/Pthreads parallelization (ON=OpenMP / OFF=Pthreads)
%define with_omp	%{?_without_omp:	0} %{?!_without_omp:	1}
%define with_omp 1
# with nvptx parallelization backaend
%define with_nvptx	%{?_without_nvptx:	0} %{?!_without_nvptx:	1}
%define with_nvptx 1
# use (OpenBlas)/FlexiBlas backaend (On=OpenBlas / OFF=FlexiBlas)
%define with_openblas	%{?_without_blas:       0} %{?!_without_blas:   1}
%define with_openblas 0
# use Blis backaend
%define with_blis	%{?_without_blis:	0} %{?!_without_blis:	1}
%define with_blis 0
# use Vulkan backaend
%define with_vlk	%{?_without_vlk:	0} %{?!_without_vlk:	1}
%define with_vlk 0
# use Rocm backaend
%define with_rocm	%{?_without_rocm:	0} %{?!_without_rocm:	1}
%define with_rocm 1
# Build with native/legacy CMake HIP support (ON=native / OFF=legacy)
%define with_hips	%{?_without_hips:	0} %{?!_without_hips:	1}
%define with_hips 1
# use amdgcn offload
%define with_gcn	%{?_without_gcn:	0} %{?!_without_gcn:	1}
%define with_gcn 0
# enable {ADDRESS, THREAD, UNDEFINED} sanitizer (THREAD is broken)
%define with_san	%{?_without_san:	0} %{?!_without_san:	1}
%define with_san 0
# ADDRESS sanitizer
%define with_san_add	%{?_without_san:	0} %{?!_without_san:	1}
%define with_san_add 0
# THREAD sanitizer
%define with_san_thr	%{?_without_san:	0} %{?!_without_san:	1}
%define with_san_thr 0
# UNDEFINED sanitizer
%define with_san_und	%{?_without_san:	0} %{?!_without_san:	1}
%define with_san_und 0
# with package python-guff-py
%define with_guffpy	%{?_without_guffpy:	0} %{?!_without_guffpy:	1}
%define with_guffpy 0
# with package webui
%define with_webui	%{?_without_webui:	0} %{?!_without_webui:	1}
%define with_webui 0
# only build llama-server package 
%define with_lls	%{?_without_lls:	0} %{?!_without_lls:	1}
%define with_lls 0
# only build GGML_RPC package
%define with_rpc	%{?_without_rpc:	0} %{?!_without_rpc:	1}
%define with_rpc 1

%if 0%{?with_openblas} && 0%{?with_omp}
%global summary LLM inference in C/C++. OpenMP parallelization, and OpenBlas backend.
%endif

%if 0%{?with_openblas} && 0%{?with_omp} && 0%{?with_nvptx}
%global summary LLM inference in C/C++. OpenMP parallelization, OpenBlas, and nvptx offload.
%endif

%if 0%{?with_blis} && 0%{?with_omp}
%global summary LLM inference in C/C++. OpenMP parallelization, and Blis backend.
%endif

%if 0%{?with_blis} && 0%{?with_omp} && 0%{?with_nvptx}
%global summary LLM inference in C/C++. OpenMP parallelization, Blis, and nvptx offest.
%endif

# THREAD sanitizer doens not work with OpenMP.
# will use Pthreads:
%if %{with_san_thr}
%define with_omp 0
%endif

# use only 64 bit version of backend
%if 0%{?__isa_bits} == 64
%define with_x64 1
%endif

Summary:	LLM inference in C/C++
Name:		llama-cpp
License:        MIT AND Apache-2.0 AND LicenseRef-Fedora-Public-Domain
Epoch:		1
Version:	b4327
ExclusiveArch:  x86_64 aarch64
Release:        %autorelease
URL:            https://github.com/ggerganov/llama.cpp
Source0:        %{url}/archive/%{version}.tar.gz#/llama.cpp-%{version}.tar.gz
# https://github.com/ggerganov/llama.cpp/pull/10706
# ctest will fail test-eval-callback: curl 
# found in `examples/eval-callback/CMakeLists.txt`
Patch0:		0001-fix-for-building-with-no-internet-connection.patch
Requires:	%{name}-ggml = %{version}-%{release}

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
# ref: .github/workflows/server.yml
# examples/server/tests/requirements.txt
%if %{with_guffpy}
%global pypi_name gguf
%global pypi_version 0.11.0
Recommends:	python3
BuildRequires:	python3-devel
BuildRequires:	python3-huggingface-hub
BuildRequires:	python3-pure-protobuf
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
BuildRequires:  python3dist(protobuf)
# https://pypi.org/project/openai/
# https://pypi.org/project/transformers/
%endif

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
%if %{with_nvptx}
# https://gcc.gnu.org/wiki/OpenACC
# Nvidia PTX and AMD Radeon devices.
Requires:	libgomp-offload-nvptx
BuildRequires:	libgomp-offload-nvptx
%endif
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
%if %{with_lapack}
## lapack
BuildRequires:  lapack
BuildRequires:  lapack-devel
BuildRequires:  lapack-static
%if %{with_x64}
BuildRequires:  lapack64
BuildRequires:  lapack64_
%endif
%endif
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
# these OpenBLAS packages may not be needed:
%if %{with_x64}
BuildRequires:	openblas-serial64
BuildRequires:  openblas-serial64_
%else
BuildRequires:  openblas-serial
%endif
%else
## FlexiBLAS
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
%if %{with_vlk}
Requires:	vulkan-headers
BuildRequires:	vulkan-headers
Requires:	vulkan-loader
BuildRequires:	vulkan-loader
BuildRequires:	vulkan-loader-devel
Requires:	vulkan-tools
BuildRequires:	vulkan-tools
BuildRequires:	vulkan-utility-libraries-devel
Requires:	vulkan-validation-layers
BuildRequires:	vulkan-validation-layers
BuildRequires:	vulkan-volk-devel
Requires:	VulkanMemoryAllocator
BuildRequires:	VulkanMemoryAllocator
BuildRequires:	VulkanMemoryAllocator-devel
Requires:	mesa-vulkan-drivers
BuildRequires:	mesa-vulkan-drivers
%endif

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Rocm
# GGML_HIP_UMA
%if %{with_rocm}
%ifarch x86_64
BuildRequires:	rocsolver
BuildRequires:	rocsolver-devel
BuildRequires:	libchipcard-devel
BuildRequires:	hipblaslt-devel
BuildRequires:	hipcub-devel
BuildRequires:	hipblas
BuildRequires:	hipblaslt
BuildRequires:	hipfft
BuildRequires:	hipfft-devel
BuildRequires:	hiprand
BuildRequires:	hiprand-devel
BuildRequires:	hipsolver
BuildRequires:	hipsolver-devel
BuildRequires:	hipsparse
BuildRequires:  hipsparse-devel
BuildRequires:	hipcc
BuildRequires:	hipcc-libomp-devel
BuildRequires:  rocm-comgr-devel
BuildRequires:  rocm-hip
BuildRequires:  rocm-hip-devel
BuildRequires:  rocblas-devel
BuildRequires:  hipblas-devel
BuildRequires:  hipcc-libomp-devel
BuildRequires:  rocm-runtime-devel
BuildRequires:  rocm-rpm-macros
BuildRequires:  rocm-rpm-macros-modules
%if %{with_gcn}
BuildRequires:	libgomp-offload-amdgcn
%endif

Requires:       rocblas
Requires:       rocsolver
Requires:       hipblas
%endif
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
Requires:       %{name}-ggml%{?_isa} = %{version}-%{release}

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
%{_description}
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
export LLAMA_VERSION=0.0."$(echo %{version} | grep -oP "[0-9][0-9][0-9][0-9]")"
export LLAMA_INSTALL_VERSION=0.0."$(echo %{version} | grep -oP "[0-9][0-9][0-9][0-9]")"
# export LLAMA_BUILD_COMMIT=d9c3ba2b
export SHORT_HASH="$(git rev-parse --short=7 HEAD)"
export LLAMA_BUILD_NUMBER="$(echo %{version} | grep -oP "[0-9][0-9][0-9][0-9]")"
export BRANCH_NAME=%{version}
export GGML_NLOOP=3
export GGML_N_THREADS=1
export LLAMA_LOG_COLORS=1
export LLAMA_LOG_PREFIX=1
export LLAMA_LOG_TIMESTAMPS=1
export LLAMA_LOG_VERBOSITY=10

# Blis
%if %{with_blis}
export GOMP_CPU_AFFINITY="0-19"
export BLIS_NUM_THREADS=14
%endif
# remove phone packages
rm -rf exmples/llma.android
rm -rf examples/llama.swiftui
# remove documentation
%if !%{with_doc}
find . -name '*.md' -exec rm -rf {} \;
%endif
# git cruft
find . -name '.gitignore' -exec rm -rf {} \;

# Rocm
# settings for Rocm release
%if %{with_rocm}
%ifarch x86_64
%global summary LLM inference in C/C++. OpenMP parallelization, amdgcn offload, and Rocm.
%define with_omp 1
%define with_gcn 1
%define with_hips 0
%define with_nvptx 0
%define with_openblas 0
%define with_blis 0
%define with_vlk 0
# global
#%%global build_hip ON
%global toolchain rocm
# hipcc does not support some clang flags
#%%global build_cxxflags %%(echo %%{optflags} | sed -e 's/-fstack-protector-strong/-Xarch_host -fstack-protector-strong/' -e 's/-fcf-protection/-Xarch_host -fcf-protection/')
%else
%define with_rocm 0
%endif
%endif

# python guff-py setup
%if %{with_guffpy}
cd %{_vpath_srcdir}/gguf-py
%generate_buildrequires
%pyproject_buildrequires -r
cd -
%endif

# -----------------------------------------------------------------------------
# build
# -----------------------------------------------------------------------------
%build
# python guff-py build
%if %{with_guffpy}
cd %{_vpath_srcdir}/gguf-py
%pyproject_wheel
cd -
%endif

# https://github.com/ggerganov/llama.cpp/pull/10627
# -DOAI_FULL_COMPAT
# build options:
# ggml/CMakeLists.txt
# .devops/full.Dockerfile
# -DLLAMA_SERVER_SSL=ON
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
	-DLIB_SUFFIX=64 \
	-DCMAKE_INSTALL_DO_STRIP:BOOL=ON \
	-DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
	-DCMAKE_INSTALL_BINDIR:PATH=%{_bindir} \
	-DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir} \
	-DCMAKE_INSTALL_DATADIR:PATH=%{_datadir} \
	-DCMAKE_INSTALL_MANDIR:PATH=%{_mandir} \
	-DCMAKE_INSTALL_INCLUDEDIR:PATH=%{_includedir} \
	-DCMAKE_INSTALL_LOCALSTATEDIR:PATH=%{_localstatedir} \
	-DCMAKE_INSTALL_SHAREDSTATEDIR:PATH=%{_sharedstatedir} \
	-DCMAKE_INSTALL_RUNSTATEDIR:PATH=%{_rundir} \
	-DCMAKE_INSTALL_LIBEXECDIR:PATH=%{_libexecdir} \
	-DCMAKE_INSTALL_INFODIR:PATH=%{_infodir} \
	-DCMAKE_INSTALL_MANDIR:PATH=%{_mandir} \
%if %{with_omp}
	-DGGML_OPENMP:BOOL=ON \
%else
	-DGGML_OPENMP:BOOL=OFF \
%endif
%if %{with_vlk}
	-DGGML_VULKAN:BOOL=ON \
%else
	-DGGML_VULKAN:BOOL=OFF \
%endif
%if %{with_rpc}
	-DGGML_RPC:BOOL=ON \
%else
	-DGGML_RPC:BOOL=OFF \
%endif
%if %{with_san_add}
	-DLLAMA_SANITIZE_ADDRESS:BOOL=ON \
%endif
%if %{with_san_thr}
	-DLLAMA_SANITIZE_THREAD:BOOL=ON \
%endif
%if %{with_san_und}
	-DLLAMA_SANITIZE_UNDEFINED:BOOL=ON \
%endif
%if %{with_exa}
	-DLLAMA_BUILD_EXAMPLES:BOOL=ON \
%else
	-DLLAMA_BUILD_EXAMPLES:BOOL=OFF \
%endif
%if %{with_test}
        -DLLAMA_BUILD_TESTS:BOOL=ON \
%else
        -DLLAMA_BUILD_TESTS:BOOL=OFF \
%endif
%if %{with_hbm}
        -DGGML_CPU_HBM:BOOL=ON \
%else
        -DGGML_CPU_HBM:BOOL=OFF \
%endif
%if %{with_openblas}
        -DGGML_BLAS=ON \
        -DGGML_BLAS_VENDOR=OpenBLAS \
%endif
%if %{with_blis}
        -DGGML_BLAS=ON \
        -DGGML_BLAS_VENDOR=FLAME \
%endif
%if %{with_rocm}
	-DGGML_HIP=ON \
%if %{with_hips}
	-DCMAKE_HIP_COMPILER="$(hipconfig -l)/clang"
%else
	-DCMAKE_C_COMPILER=hipcc \
	-DCMAKE_CXX_COMPILER=hipcc
%endif
%endif

%if %{with_lls}
%cmake_build --config Release --target llama-server
%else
%cmake_build --config Release
%endif
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
#cd examples/server/tests
#SLOW_TESTS=1 ./tests.sh

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

%if %{with_test}
%files test
%{_bindir}/test-*
%endif

#convert_hf_to_gguf.py
#convert_hf_to_gguf_update.py
#convert_llama_ggml_to_gguf.py
#convert_lora_to_gguf.py
%files convert-hf-to-gguf
%{_bindir}/convert_hf_to_gguf.py

# docs

%changelog
%autochangelog
