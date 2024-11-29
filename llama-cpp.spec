# For the extra python package gguf that comes with llama-cpp
%global pypi_name gguf
%global pypi_version 0.10.0

%global summary %{expand:
LLM inference in C/C++}

%global common_description %{expand:
The main goal of llama.cpp is to enable LLM inference with minimal setup and state-of-the-art performance on a wide variety of hardware - locally and in the cloud.

* Plain C/C++ implementation without any dependencies
* Apple silicon is a first-class citizen - optimized via ARM NEON, Accelerate and Metal frameworks
* AVX, AVX2, AVX512 and AMX support for x86 architectures
* 1.5-bit, 2-bit, 3-bit, 4-bit, 5-bit, 6-bit, and 8-bit integer quantization for faster inference and reduced memory use
* Custom CUDA kernels for running LLMs on NVIDIA GPUs (support for AMD GPUs via HIP and Moore Threads MTT GPUs via MUSA)
* Vulkan and SYCL backend support
* CPU+GPU hybrid inference to partially accelerate models larger than the total VRAM capacity}

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

Summary:	LLM inference in C/C++
Name:		llama-cpp
Epoch:		1
License:        MIT AND Apache-2.0 AND LicenseRef-Fedora-Public-Domain
Version:        b4206
ExclusiveArch:  x86_64 aarch64
Release:        %autorelease
URL:            https://github.com/ggerganov/llama.cpp
Source0:        %{url}/archive/%{version}.tar.gz#/llama.cpp-%{version}.tar.gz
Provides:       llama-cpp-full = %{version}-%{release}

# Build Required packages
BuildRequires:  xxd
BuildRequires:  git
BuildRequires:  cmake
BuildRequires:  wget
BuildRequires:  langpacks-en
# glibc-all-langpacks and glibc-langpack-is are needed for GETTEXT_LOCALE and
# GETTEXT_ISO_LOCALE test prereq's, glibc-langpack-en ensures en_US.UTF-8.
BuildRequires:  glibc-all-langpacks
BuildRequires:  glibc-langpack-en
BuildRequires:  glibc-langpack-is
BuildRequires:  curl
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  libcurl-devel
# above are packages in .github/workflows/server.yml
BuildRequires:  gcc-c++
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

%description
LLM inference in C/C++

%prep
%autosetup -S git
%autosetup -p1 -n llama.cpp-%{version}

# no android needed
rm -rf exmples/llma.android
# remove documentation
find . -name '*.md' -exec rm -rf {} \;
# git cruft
find . -name '.gitignore' -exec rm -rf {} \;

%build
# Improve build reproducibility
export TZ=UTC
export SOURCE_DATE_EPOCH=$(date -r version +%%s 2>/dev/null)

%cmake \
    -DCMAKE_INSTALL_LIBDIR=%{_lib} \
    -DCMAKE_INSTALL_BIBDIR=%{_bindir} \
    -DCMAKE_INSTALL_BIBDIR=%{_includedir} \
    -DCMAKE_SKIP_RPATH=ON
 
%cmake_build --config Release

%install
%cmake_install

## rm -rf %{buildroot}%{_libdir}/libggml_shared.*

%if %{with check}
%check
%ctest
%endif

%files
%license LICENSE
%{_libdir}/libllama.so.%{version}
%{_libdir}/libggml.so.%{version}

%changelog
%autochangelog
