%global real_name cuda_sanitizer_api

%global debug_package %{nil}
%global __strip /bin/true
%global _missing_build_ids_terminate_build 0
%global _build_id_links none
%global major_package_version 12-0

Name:           cuda-sanitizer
Epoch:          1
Version:        12.0.140
Release:        1%{?dist}
Summary:        CUDA Compute Sanitizer API
License:        CUDA Toolkit
URL:            https://developer.nvidia.com/cuda-toolkit
ExclusiveArch:  x86_64 ppc64le aarch64 %{ix86}

Source0:        https://developer.download.nvidia.com/compute/cuda/redist/%{real_name}/linux-x86_64/%{real_name}-linux-x86_64-%{version}-archive.tar.xz
Source1:        https://developer.download.nvidia.com/compute/cuda/redist/%{real_name}/linux-ppc64le/%{real_name}-linux-ppc64le-%{version}-archive.tar.xz
Source2:        https://developer.download.nvidia.com/compute/cuda/redist/%{real_name}/linux-aarch64/%{real_name}-linux-aarch64-%{version}-archive.tar.xz

Requires(post): ldconfig
Conflicts:      %{name}-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}

%description
Compute Sanitizer is a functional correctness checking suite included in the
CUDA toolkit. It provides a set of API's to enable third party tools to write
GPU sanitizing tools, such as memory and race checkers.

%package devel
Summary:        Development files for CUDA Compute Sanitizer API
Requires:       %{name}%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-devel-%{major_package_version} < %{?epoch:%{epoch}:}%{version}

%description devel
This package provides development files for the CUDA Compute Sanitizer API.

%prep
%ifarch x86_64 %{ix86}
%setup -q -n %{real_name}-linux-x86_64-%{version}-archive
%endif

%ifarch ppc64le
%setup -q -T -b 1 -n %{real_name}-linux-ppc64le-%{version}-archive
%endif

%ifarch aarch64
%setup -q -T -b 2 -n %{real_name}-linux-aarch64-%{version}-archive
%endif

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_libdir}

cp -fr compute-sanitizer/include/* %{buildroot}%{_includedir}/

%ifarch %{ix86}
cp -fr compute-sanitizer/x86/lib* %{buildroot}%{_libdir}/
cp -fr compute-sanitizer/x86/Tree* %{buildroot}%{_bindir}/
%else
cp -fr compute-sanitizer/lib* %{buildroot}%{_libdir}/
cp -fr compute-sanitizer/Tree* compute-sanitizer/compute-sanitizer %{buildroot}%{_bindir}/
%endif

%{?ldconfig_scriptlets}

%files
%license LICENSE
%{_bindir}/TreeLauncherSubreaper
%{_bindir}/TreeLauncherTargetLdPreloadHelper
%ifnarch %{ix86}
%{_bindir}/compute-sanitizer
%{_libdir}/libsanitizer-collection.so
%{_libdir}/libsanitizer-public.so
%endif
%{_libdir}/libInterceptorInjectionTarget.so
%{_libdir}/libTreeLauncherPlaceholder.so
%{_libdir}/libTreeLauncherTargetInjection.so
%{_libdir}/libTreeLauncherTargetUpdatePreloadInjection.so

%files devel
%doc compute-sanitizer/docs
%{_includedir}/*

%changelog
* Sat Feb 25 2023 Simone Caronni <negativo17@gmail.com> - 1:12.0.140-1
- Update to 12.0.140.

* Tue Dec 13 2022 Simone Caronni <negativo17@gmail.com> - 1:12.0.90-1
- Update to 12.0.90.

* Fri Nov 11 2022 Simone Caronni <negativo17@gmail.com> - 1:11.8.86-1
- Update to 11.8.86.
- Use aarch64 archive in place of sbsa.

* Sun Sep 04 2022 Simone Caronni <negativo17@gmail.com> - 1:11.7.91-1
- Update to 11.7.91.

* Thu Jun 23 2022 Simone Caronni <negativo17@gmail.com> - 1:11.7.50-1
- Update to 11.7.50.

* Thu Mar 31 2022 Simone Caronni <negativo17@gmail.com> - 1:11.6.124-1
- Update to 11.6.124 (CUDA 11.6.2).

* Tue Mar 08 2022 Simone Caronni <negativo17@gmail.com> - 1:11.6.112-1
- Update to 11.6.112 (CUDA 11.6.1).

* Thu Jan 27 2022 Simone Caronni <negativo17@gmail.com> - 1:11.6.55-1
- First build with the new tarball components.
