#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static libraries
#
Summary:	Low-level NVM Express Mastery Galore
Summary(pl.UTF-8):	Niskopoziomowa biblioteka do operowania urządzeniami NVM Express
Name:		libvfn
Version:	5.1.0
Release:	1
License:	LGPL v2.1+ or MIT
Group:		Libraries
#Source0Download: https://github.com/SamsungDS/libvfn/releases
Source0:	https://github.com/SamsungDS/libvfn/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	f46a3dd69a477b5a6c8f35a59dd33a7a
URL:		https://github.com/SamsungDS/libvfn
BuildRequires:	gcc >= 6:4.7
# for examples
BuildRequires:	libnvme-devel >= 1.0
BuildRequires:	meson >= 0.59.0
BuildRequires:	ninja >= 1.5
BuildRequires:	perl-base
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
%{?with_apidocs:BuildRequires:	sphinx-build}
ExclusiveArch:	%{x8664} aarch64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libvfn is zero-dependency library for interacting with PCIe-based NVMe
devices from user-space using the Linux kernel vfio-pci driver.

The core of the library is excessively low-level and aims to allow
controller verification and testing teams to interact with the NVMe
device at the register and queue level. However, it does also provide
a range of utility functions to issue commands and polling for their
completions along with helpers for mapping memory in the commands as
well as managing allocation of I/O Virtual Address through VFIO.

%description -l pl.UTF-8
libvfn to biblioteka bez zewnętrznych zależności do pracy z
urządzeniami NVMe opartymi na PCIe z przestrzeni użytkownika przy
użyciu sterownika jądra Linuksa vfio-pci.

Podstawowa część biblioteki jest skrajnie poziomowa, a jej celem jest
umożliwienie zespołom weryfikującym i testującym pracować z
urządzeniami NMVe na poziomie rejestrów i kolejek. Jednak dostępne są
też funkcje narzędziowe do wysyłania poleceń i oczekiwania na
zakończenie oraz pomocnicze do odwzorowywania pamięci w poleceniach, a
także zarządzania przydzielaniem adresów wirtualnych we/wy poprzez
VFIO.

%package devel
Summary:	Header files for libvfn library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libvfn
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libvfn library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libvfn.

%package static
Summary:	Static libvfn library
Summary(pl.UTF-8):	Statyczna biblioteka libvfn
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libvfn library.

%description static -l pl.UTF-8
Statyczna biblioteka libvfn.

%package apidocs
Summary:	API documentation for libvfn library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libvfn
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libvfn library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libvfn.

%prep
%setup -q

%build
%meson build \
	%{!?with_static_libs:--default-library=shared} \
	%{!?with_apidocs:-Ddocs=false}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG.md CONTRIBUTORS LICENSE README.rst
%attr(755,root,root) %{_bindir}/vfntool
%attr(755,root,root) %{_libdir}/libvfn.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libvfn.so.5

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvfn.so
%{_includedir}/vfn
%{_pkgconfigdir}/libvfn.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libvfn.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/docs/manual/{_static,api,*.html,*.js}
%endif
