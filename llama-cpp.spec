# For the extra python package gguf that comes with llama-cpp
%global pypi_name gguf
%global pypi_version 0.10.0

# Some optional subpackages
%bcond_with examples
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

%bcond_with check

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
Version:        b3837
Release:        %autorelease

URL:            https://github.com/ggerganov/llama.cpp
Source0:        %{url}/archive/%{version}.tar.gz#/llama.cpp-%{version}.tar.gz

ExclusiveArch:  x86_64 aarch64

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
BuildRequires:  curl
BuildRequires:  wget
BuildRequires:  langpacks-en
# above are packages in .github/workflows/server.yml
BuildRequires:  libcurl-devel
BuildRequires:  gcc-c++
BuildRequires:  openmpi
%if 0%{?fedora} >= 40
BuildRequires:  pthreadpool-devel
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
Recommends:     numactl

%global _description %{expand:
The main goal of llama.cpp is to enable LLM inference with minimal setup and state-of-the-art performance on a wide variety of hardware - locally and in the cloud.

* Plain C/C++ implementation without any dependencies
* Apple silicon is a first-class citizen - optimized via ARM NEON, Accelerate and Metal frameworks
* AVX, AVX2, AVX512 and AMX support for x86 architectures
* 1.5-bit, 2-bit, 3-bit, 4-bit, 5-bit, 6-bit, and 8-bit integer quantization for faster inference and reduced memory use
* Custom CUDA kernels for running LLMs on NVIDIA GPUs (support for AMD GPUs via HIP and Moore Threads MTT GPUs via MUSA)
* Vulkan and SYCL backend support
* CPU+GPU hybrid inference to partially accelerate models larger than the total VRAM capacity}

%package devel
Summary:        %{summary}.
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel

%if %{with test}
%package test
Summary:        Tests for %{name} - %{summary}.
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description test
%{summary}
%endif

%if %{with examples}
%package examples
Summary:        Examples for %{name} - %{summary}.
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       python3dist(numpy)
Requires:       python3dist(torch)
Requires:       python3dist(sentencepiece)

%description examples
%{summary}
%endif

%prep
%autosetup -S git
%autosetup -p1 -n llama.cpp-%{version}

# verson the *.so
sed -i -e 's/POSITION_INDEPENDENT_CODE ON/POSITION_INDEPENDENT_CODE ON SOVERSION %{version}/' src/CMakeLists.txt
sed -i -e 's/POSITION_INDEPENDENT_CODE ON/POSITION_INDEPENDENT_CODE ON SOVERSION %{version}/' ggml/src/CMakeLists.txt

# no android needed
rm -rf exmples/llma.android
# git cruft
find . -name '.gitignore' -exec rm -rf {} \;

%build
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
    -DCMAKE_INSTALL_BIBDIR=%{_bin} \
    -DCMAKE_INSTALL_BIBDIR=%{_includedir} \
    -DCMAKE_SKIP_RPATH=ON \
    -DLLAMA_AVX=OFF \
    -DLLAMA_AVX2=OFF \
    -DLLAMA_AVX512=OFF \
    -DLLAMA_AVX512_VBMI=OFF \
    -DLLAMA_AVX512_VNNI=OFF \
    -DLLAMA_FMA=OFF \
    -DLLAMA_F16C=OFF \
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

rm -rf %{buildroot}%{_libdir}/libggml_shared.*

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
