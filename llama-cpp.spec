# For the extra python package gguf that comes with llama-cpp
%global pypi_name gguf
%global pypi_version 0.10.0

# Some optional subpackages
%bcond_without examples
%if %{with examples}
%global build_examples ON
%else
%global build_examples OFF
%endif

%bcond_with test
%if %{with test}
%global build_test ON
%else
%global build_test OFF
%endif

# remove documentation files
%bcond_without doc

# don't add ssl support to llama-server
%bcond_without openssl

# OpenSSL ENGINE support
# This is deprecated by OpenSSL since OpenSSL 3.0 and by Fedora since Fedora 41
# https://fedoraproject.org/wiki/Changes/OpensslDeprecateEngine
# Change the bcond to 0 to turn off ENGINE support by default
%bcond openssl_engine_support %[%{defined fedora} || 0%{?rhel} < 10]

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
Release:        %autorelease

URL:            https://github.com/ggerganov/llama.cpp
Source0:        %{url}/archive/%{version}.tar.gz#/llama.cpp-%{version}.tar.gz

%ifarch x86_64
%bcond_without rocm
%else
%bcond_with rocm
%endif

%if %{with rocm}
%global build_hip ON
%global toolchain rocm
# hipcc does not support some clang flags
%global build_cxxflags %(echo %{optflags} | sed -e 's/-fstack-protector-strong/-Xarch_host -fstack-protector-strong/' -e 's/-fcf-protection/-Xarch_host -fcf-protection/')
%else
%global build_hip OFF
%global toolchain gcc
%endif

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
%if %{with openssl}
# https://github.com/ggerganov/llama.cpp/blob/master/examples/server/README.md#build-with-ssl
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig(libcrypto)
BuildRequires:	pkgconfig(libssl)
BuildRequires:	pkgconfig(openssl)
%if %{with openssl_engine_support} && 0%{?fedora} >= 41
BuildRequires:	openssl-devel-engine
%endif
%endif
%if 0%{?fedora} >= 40
BuildRequires:  pthreadpool-devel
BuildRequires:  pkgconfig(pthread-stubs)
%endif
%if %{with examples}
BuildRequires:  python3-devel
BuildRequires:  python3dist(pip)
BuildRequires:  python3dist(poetry)
%endif

%if 0%{with rocm} && 0%{?fedora} >= 40
BuildRequires:  hipblas-devel
BuildRequires:  rocm-comgr-devel
BuildRequires:  rocm-hip-devel
BuildRequires:  rocblas-devel
BuildRequires:  hipblas-devel
BuildRequires:  rocm-runtime-devel
BuildRequires:  rocm-rpm-macros
BuildRequires:  rocm-rpm-macros-modules

Requires:	rocblas
Requires:	hipblas
%endif

Requires:       curl
Requires:       pkgconfig(libcurl)
Requires:       pkgconfig(pthread-stubs)
Recommends:     numactl


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

Provides:       bundled(llama-batched)
Provides:       bundled(llama-batched-bench)
Provides:       bundled(llama-bench)
Provides:       bundled(llama-cli)
Provides:       bundled(llama-convert-llama2c-to-ggml)
Provides:       bundled(llama-embedding)
Provides:       bundled(llama-eval-callback)
Provides:       bundled(llama-export-lora)
Provides:       bundled(llama-gbnf-validator)
Provides:       bundled(llama-gguf)
Provides:       bundled(llama-gguf-hash)
Provides:       bundled(llama-gguf-split)
Provides:       bundled(llama-gritlm)
Provides:       bundled(llama-imatrix)
Provides:       bundled(llama-infill)
Provides:       bundled(llama-llava-cli)
Provides:       bundled(llama-minicpmv-cli)
Provides:       bundled(llama-lookahead)
Provides:       bundled(llama-lookup)
Provides:       bundled(llama-lookup-create)
Provides:       bundled(llama-lookup-merge)
Provides:       bundled(llama-lookup-stats)
Provides:       bundled(llama-parallel)
Provides:       bundled(llama-passkey)
Provides:       bundled(llama-perplexity)
Provides:       bundled(llama-q8dot)
Provides:       bundled(llama-quantize)
Provides:       bundled(llama-quantize-stats)
Provides:       bundled(llama-retrieval)
Provides:       bundled(llama-save-load-state)
Provides:       bundled(llama-server)
Provides:       bundled(llama-simple)
Provides:       bundled(llama-simple-chat)
Provides:       bundled(llama-run)
Provides:       bundled(llama-speculative)
Provides:       bundled(llama-tokenize)
Provides:       bundled(llama-vdot)
Provides:       bundled(llama-cvector-generator)
Provides:       bundled(llama-gen-docs)

%package	llama-cpp
Summary:        Meta-package to pull in all %{name} tools
BuildArch:	x86_64 aarch64
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description    -n all %{common_description}
#%%if %{with openssl}

# get all docs files with
# find . -name '*.md'
%package	doc
Summary:        Documentation files for %{name}
BuildArch:      noarch
%description	-n doc
Documentation files for %{name} package

%package	devel
Summary:        devel for %{summary}
BuildArch:	x86_64 aarch64
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description	-n devel %{common_description}

%package        rocm
Summary:        %{summary} with rocm
BuildArch:	x86_64
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description    -n rocm %{common_description}

%if %{with test}
%package test
Summary:        Tests for %{summary}
BuildArch:	x86_64 aarch64
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description	-n tests %{common_description}
%endif

%if %{with examples}
%package examples
Summary:        Examples for %{name} - %{summary}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       python3dist(numpy)
Requires:       python3dist(torch)
Requires:       python3dist(sentencepiece)
%description	-n examples %{common_description}
%endif

%prep
%autosetup -S git
%autosetup -p1 -n llama.cpp-%{version}

# verson the *.so
sed -i -e 's/POSITION_INDEPENDENT_CODE ON/POSITION_INDEPENDENT_CODE ON SOVERSION %{version}/' src/CMakeLists.txt
sed -i -e 's/POSITION_INDEPENDENT_CODE ON/POSITION_INDEPENDENT_CODE ON SOVERSION %{version}/' ggml/src/CMakeLists.txt
sed -i -e 's/POSITION_INDEPENDENT_CODE ON/POSITION_INDEPENDENT_CODE ON SOVERSION %{version}/' cmake/llama-config.cmake.in
sed -i -e 's/POSITION_INDEPENDENT_CODE ON/POSITION_INDEPENDENT_CODE ON SOVERSION %{version}/' common/CMakeLists.txt
sed -i -e 's/POSITION_INDEPENDENT_CODE ON/POSITION_INDEPENDENT_CODE ON SOVERSION %{version}/' examples/llava/CMakeLists.txt

# no android needed
rm -rf exmples/llma.android
# remove documentation
%if %{without doc}
find . -name '*.md' -exec rm -rf {} \;
%endif
# git cruft
find . -name '.gitignore' -exec rm -rf {} \;

%build
# Improve build reproducibility
export TZ=UTC
export SOURCE_DATE_EPOCH=$(date -r version +%%s 2>/dev/null)

%if %{with examples}
cd %{_vpath_srcdir}/gguf-py
%pyproject_wheel
cd -
%endif

%if %{with rocm}
module load rocm/default
%endif

%cmake \
    -DCMAKE_INSTALL_LIBDIR=%{_lib} \
    -DCMAKE_INSTALL_BIBDIR=%{_bindir} \
    -DCMAKE_INSTALL_BIBDIR=%{_includedir} \
    -DCMAKE_SKIP_RPATH=ON \
%if %{with rocm}
    -DLLAMA_HIPBLAS=%{build_hip} \
    -DAMDGPU_TARGETS=${ROCM_GPUS} \
%endif
    -DLLAMA_BUILD_EXAMPLES=%{build_examples} \
    -DLLAMA_BUILD_TESTS=%{build_test}
    
%cmake_build

%if %{with rocm}
module purge
%endif


%install
%if %{with examples}
cd %{_vpath_srcdir}/gguf-py
%pyproject_install
cd -
%endif

%cmake_install

## rm -rf %{buildroot}%{_libdir}/libggml_shared.*

%if %{with examples}
mkdir -p %{buildroot}%{_datarootdir}/%{name}
cp -r %{_vpath_srcdir}/examples %{buildroot}%{_datarootdir}/%{name}/
cp -r %{_vpath_srcdir}/models %{buildroot}%{_datarootdir}/%{name}/
cp -r %{_vpath_srcdir}/README.md %{buildroot}%{_datarootdir}/%{name}/
rm -rf %{buildroot}%{_datarootdir}/%{name}/examples/llama.android
%else
rm %{buildroot}%{_bindir}/convert*.py
%endif

%if %{with test}
%if %{with check}
%check
%ctest
%endif
%endif

%files
%license LICENSE
%{_libdir}/libllama.so.%{version}
%{_libdir}/libggml.so.%{version}

%files devel
%dir %{_libdir}/cmake/llama
%doc README.md
%{_includedir}/ggml.h
%{_includedir}/ggml-*.h
%{_includedir}/llama.h
%{_libdir}/libllama.so
%{_libdir}/libggml.so
%{_libdir}/cmake/llama/*.cmake
%{_exec_prefix}/lib/pkgconfig/llama.pc

%if %{with test}
%files test
%{_bindir}/test-*
%endif

%if %{with examples}
%files examples
%{_bindir}/convert_hf_to_gguf.py
%{_bindir}/gguf-*
%{_bindir}/llama-*
%{_datarootdir}/%{name}/
%{_libdir}/libllava_shared.so
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}*.dist-info
%{python3_sitelib}/scripts
%endif

%changelog
%autochangelog
