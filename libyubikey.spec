#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_without	tests		# build without tests

Summary:	C library for decrypting and parsing Yubikey One-time passwords
Summary(pl.UTF-8):	Biblioteka C do odszyfrowywania i analizy jednorazowych haseł Yubikey
Name:		libyubikey
Version:	1.13
Release:	2
License:	BSD
Group:		Libraries
Source0:	https://developers.yubico.com/yubico-c/Releases/%{name}-%{version}.tar.gz
# Source0-md5:	6e84fc1914ab5b609319945c18d45835
URL:		https://developers.yubico.com/yubico-c/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package holds a low-level C software development kit for the
Yubico authentication device, the Yubikey.

%description -l pl.UTF-8
Ten pakiet zawiera niskopoziomową bibliotekę C do urządzenia
uwierzytelniającego Yubico - Yubikey.

%package devel
Summary:	Development files for libyubikey
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libyubikey
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header file needed to develop applications
that use libyubikey.

%description devel -l pl.UTF-8
Ten pakiet zawiera plik nagłówkowy niezbędny do tworzenia aplikacji
wykorzystujących libyubikey.

%package static
Summary:	Static libyubikey library
Summary(pl.UTF-8):	Statyczna biblioteka libyubikey
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libyubikey library.

%description static -l pl.UTF-8
Statyczna biblioteka libyubikey.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}

%{__make}

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL="%{__install} -p" \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README THANKS
%attr(755,root,root) %{_bindir}/modhex
%attr(755,root,root) %{_bindir}/ykparse
%attr(755,root,root) %{_bindir}/ykgenerate
%attr(755,root,root) %{_libdir}/libyubikey.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libyubikey.so.0
%{_mandir}/man1/ykgenerate.1*
%{_mandir}/man1/ykparse.1*
%{_mandir}/man1/modhex.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libyubikey.so
%{_libdir}/libyubikey.la
%{_includedir}/yubikey.h

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libyubikey.a
%endif
