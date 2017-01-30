%bcond_without	tests
#
Summary:	C library for decrypting and parsing Yubikey One-time passwords
Name:		libyubikey
Version:	1.13
Release:	1
License:	BSD
Group:		Development/Libraries
Group:		Libraries
URL:		http://opensource.yubico.com/yubico-c
Source0:	http://opensource.yubico.com/yubico-c/releases/%{name}-%{version}.tar.gz
# Source0-md5:	6e84fc1914ab5b609319945c18d45835
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package holds a low-level C software development kit for the
Yubico authentication device, the Yubikey.

%package devel
Summary:	Development files for libyubikey
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header file needed to develop applications
that use libyubikey.

%prep
%setup -q

%build
%configure \
	--disable-static \
	--disable-silent-rules \

%{__make}

%if %{with tests}
export LD_LIBRARY_PATH=$RPM_BUILD_DIR/%{name}-%{version}/.libs
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL="%{__install} -p"

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS ChangeLog README
%attr(755,root,root) %{_bindir}/modhex
%attr(755,root,root) %{_bindir}/ykparse
%attr(755,root,root) %{_bindir}/ykgenerate
%attr(755,root,root) %ghost %{_libdir}/libyubikey.so.0
%attr(755,root,root) %{_libdir}/libyubikey.so.*.*
%{_mandir}/man1/ykgenerate.1*
%{_mandir}/man1/ykparse.1*
%{_mandir}/man1/modhex.1*

%files devel
%defattr(644,root,root,755)
%{_includedir}/yubikey.h
%attr(755,root,root) %{_libdir}/libyubikey.so
%{_libdir}/libyubikey.la
