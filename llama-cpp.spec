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
Version:	b4265
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

# python requirements from:
# .devops/full.Dockerfile
# ./requirements/requirements-*

# hardware acceleration / optimization packages:
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
# BuildRequires:	libgomp-offload-amdgcn
BuildRequires:	libgomp-offload-nvptx
## memkind
Requires:       memkind
BuildRequires:  memkind
BuildRequires:  memkind-devel
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
### Blas + pthread
Requires:	openblas-threads
BuildRequires:	openblas-threads
BuildRequires:	openblas-threads64
BuildRequires:	openblas-threads64_

# optional
Recommends:     numactl

%description %_description
# -----------------------------------------------------------------------------
# sub packages
# -----------------------------------------------------------------------------

%package -n llama-cpp-devel
Summary:        %{summary} with optimizations for amx, openmp, pthread, memkind backend

%description -n llama-cpp-devel
%{_description}

# TODO

# -----------------------------------------------------------------------------
# prep
# -----------------------------------------------------------------------------
%prep
%autosetup -p1 -n llama.cpp-%{version}
%define _vpath_builddir %{_target_platform}

# fix shebang lines in Python scripts
find . -name \*.py -exec sed -i 's|/usr/bin/env python3|/usr/bin/python3|' {} \;
# verson the *.so
find . -iname "CMakeLists.*" -exec sed -i 's|POSITION_INDEPENDENT_CODE ON|POSITION_INDEPENDENT_CODE ON SOVERSION %{version}|' '{}' \;

# no android needed
#rm -rf exmples/llma.android
# remove documentation
#find . -name '*.md' -exec rm -rf {} \;
# git cruft
#find . -name '.gitignore' -exec rm -rf {} \;
# get rid of .gitignore files in examples
#find . -name \.gitignore -delete

# -----------------------------------------------------------------------------
# build
# -----------------------------------------------------------------------------
%build
# https://github.com/ggerganov/llama.cpp/pull/10627
# -DOAI_FULL_COMPAT
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
# will fail `test-eval-callback`:

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
%{_bindir}/llama-batched
%{_bindir}/llama-batched-bench
%{_bindir}/llama-bench
%{_bindir}/llama-cli
%{_bindir}/llama-convert-llama2c-to-ggml
%{_bindir}/llama-cvector-generator
%{_bindir}/llama-embedding
%{_bindir}/llama-eval-callback
%{_bindir}/llama-export-lora
%{_bindir}/llama-gbnf-validator
%{_bindir}/llama-gguf
%{_bindir}/llama-gguf-hash
%{_bindir}/llama-gguf-split
%{_bindir}/llama-gritlm
%{_bindir}/llama-imatrix
%{_bindir}/llama-infill
%{_bindir}/llama-llava-cli
%{_bindir}/llama-lookahead
%{_bindir}/llama-lookup
%{_bindir}/llama-lookup-create
%{_bindir}/llama-lookup-merge
%{_bindir}/llama-lookup-stats
%{_bindir}/llama-minicpmv-cli
%{_bindir}/llama-parallel
%{_bindir}/llama-passkey
%{_bindir}/llama-perplexity
%{_bindir}/llama-quantize
%{_bindir}/llama-quantize-stats
%{_bindir}/llama-retrieval
%{_bindir}/llama-run
%{_bindir}/llama-save-load-state
%{_bindir}/llama-server
%{_bindir}/llama-simple
%{_bindir}/llama-simple-chat
%{_bindir}/llama-speculative
%{_bindir}/llama-speculative-simple
%{_bindir}/llama-tokenize
%{_bindir}/test-arg-parser
%{_bindir}/test-autorelease
%{_bindir}/test-backend-ops
%{_bindir}/test-barrier
%{_bindir}/test-chat-template
%{_bindir}/test-grammar-integration
%{_bindir}/test-grammar-parser
%{_bindir}/test-json-schema-to-grammar
%{_bindir}/test-llama-grammar
%{_bindir}/test-log
%{_bindir}/test-model-load-cancel
%{_bindir}/test-quantize-fns
%{_bindir}/test-quantize-perf
%{_bindir}/test-rope
%{_bindir}/test-sampling
%{_bindir}/test-tokenizer-0
%{_bindir}/test-tokenizer-1-bpe
%{_bindir}/test-tokenizer-1-spm
%{_includedir}/ggml-alloc.h
%{_includedir}/ggml-backend.h
%{_includedir}/ggml-blas.h
%{_includedir}/ggml-cann.h
%{_includedir}/ggml-cpu.h
%{_includedir}/ggml-cuda.h
%{_includedir}/ggml-kompute.h
%{_includedir}/ggml-metal.h
%{_includedir}/ggml-opt.h
%{_includedir}/ggml-rpc.h
%{_includedir}/ggml-sycl.h
%{_includedir}/ggml-vulkan.h
%{_includedir}/ggml.h
%{_includedir}/llama-cpp.h
%{_includedir}/llama.h
%{_libdir}/cmake/llama/llama-config.cmake
%{_libdir}/cmake/llama/llama-version.cmake
%{_libdir}/libggml-amx.so
%{_libdir}/libggml-base.so
%{_libdir}/libggml-base.so.%{version}
%{_libdir}/libggml-cpu.so
%{_libdir}/libggml.so
%{_libdir}/libggml.so.%{version}
%{_libdir}/libllama.so
%{_libdir}/libllama.so.%{version}
%{_libdir}/libllava_shared.so
%{_prefix}/lib/pkgconfig/llama.pc

%changelog
%autochangelog
