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
Version:        b4206
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
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  libcurl-devel
# packages that either are or possibly needed
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  clang
BuildRequires:  gcc
BuildRequires:  glib
BuildRequires:  glib-devel
BuildRequires:  glibc
BuildRequires:  glibc-devel

# hardware acceleration / optimization packages
BuildRequires:  openmpi
BuildRequires:  pthreadpool-devel
BuildRequires:  pkgconfig(pthread-stubs)

# user required package
Requires:       curl
Requires:       pkgconfig(libcurl)
Requires:       pkgconfig(pthread-stubs)

# optional
Recommends:     numactl

# Provided packges
#Provides:       bundled(llama-batched)
#Provides:       bundled(llama-batched-bench)
#Provides:       bundled(llama-bench)
#Provides:       bundled(llama-cli)
#Provides:       bundled(llama-convert-llama2c-to-ggml)
#Provides:       bundled(llama-embedding)
#Provides:       bundled(llama-eval-callback)
#Provides:       bundled(llama-export-lora)
#Provides:       bundled(llama-gbnf-validator)
#Provides:       bundled(llama-gguf)
#Provides:       bundled(llama-gguf-hash)
#Provides:       bundled(llama-gguf-split)
#Provides:       bundled(llama-gritlm)
#Provides:       bundled(llama-imatrix)
#Provides:       bundled(llama-infill)
#Provides:       bundled(llama-llava-cli)
#Provides:       bundled(llama-minicpmv-cli)
#Provides:       bundled(llama-lookahead)
#Provides:       bundled(llama-lookup)
#Provides:       bundled(llama-lookup-create)
#Provides:       bundled(llama-lookup-merge)
#Provides:       bundled(llama-lookup-stats)
#Provides:       bundled(llama-parallel)
#Provides:       bundled(llama-passkey)
#Provides:       bundled(llama-perplexity)
#Provides:       bundled(llama-q8dot)
#Provides:       bundled(llama-quantize)
#Provides:       bundled(llama-quantize-stats)
#Provides:       bundled(llama-retrieval)
#Provides:       bundled(llama-save-load-state)
#Provides:       bundled(llama-server)
#Provides:       bundled(llama-simple)
#Provides:       bundled(llama-simple-chat)
#Provides:       bundled(llama-run)
#Provides:       bundled(llama-speculative)
#Provides:       bundled(llama-tokenize)
#Provides:       bundled(llama-vdot)
#Provides:       bundled(llama-cvector-generator)
#Provides:       bundled(llama-gen-docs)

%description %_description

# ---------------------------------------------------------------------------
%package -n llama-cpp-all
Summary:	%{summary} with openmp and curl without ssl

%description -n llama-cpp-all %_description
# ----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# prep
# -----------------------------------------------------------------------------
%prep
%autosetup -p1 -n llama.cpp-%{version}

# verson the *.so
find . -iname "CMakeLists.*" -exec sed -i 's|POSITION_INDEPENDENT_CODE ON|POSITION_INDEPENDENT_CODE ON SOVERSION %{version}|' '{}' \;

# no android needed
rm -rf exmples/llma.android
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
%cmake \
	-DCMAKE_INSTALL_BINDIR=%{_bindir} \
	-DCMAKE_INSTALL_LIBDIR=%{_libdir} \
	-DINCLUDE_INSTALL_DIR=%{_includedir} \
	-DLIB_INSTALL_DIR=%{_libdir} \
	-DSHARE_INSTALL_PREFIX=%{_datadir} \
	-DSYSCONF_INSTALL_DIR=%{_sysconfdir} \
	-DBUILD_SHARED_LIBS=ON \
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
%if %{with check}
%check
%ctest
%endif

# -----------------------------------------------------------------------------
# Files
# -----------------------------------------------------------------------------
%files
%license LICENSE

%changelog
%autochangelog
