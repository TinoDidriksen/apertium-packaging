Name: libdivvun
Version: 0.2.0
Release: 1%{?dist}
Summary: Grammar checker tools for Divvun languages
Group: Development/Tools
License: GPL-3.0+
URL: https://github.com/divvun/libdivvun
Source0: %{name}_%{version}.orig.tar.bz2

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gawk
BuildRequires: gcc-c++
BuildRequires: hfst-ospell-devel
BuildRequires: libarchive-devel
BuildRequires: libcg3-devel
BuildRequires: libhfst-devel
BuildRequires: libtool
BuildRequires: libxml2
BuildRequires: swig
BuildRequires: pkgconfig
BuildRequires: pugixml-devel
%if ! ( 0%{?el7} )
BuildRequires: python3
BuildRequires: python3-devel
%endif
BuildRequires: zip
Requires: libdivvun0 = %{version}-%{release}
Provides: divvun-gramcheck = %{version}-%{release}

%description
Helper tools for grammar checking for Divvun languages

%package -n libdivvun0
Summary: Runtime for Divvun grammar checker

%description -n libdivvun0
Runtime library for applications using the Divvun grammar checker API

%package -n libdivvun-devel
Summary: Headers and shared files to develop using the Divvun grammar checker library
Group: Development/Libraries
Requires: divvun-gramcheck = %{version}-%{release}

%description -n libdivvun-devel
Development files to use the Divvun grammar checker API

%if ! ( 0%{?el7} )
%package -n python3-libdivvun
Summary: Runtime for Divvun grammar checker (Python 3 module)
Requires: libdivvun0 = %{version}-%{release}

%description -n python3-libdivvun
Python 3 module for applications using the Divvun grammar checker API
%endif

%prep
%setup -q -n %{name}-%{version}

%build
autoreconf -fvi
%if ! ( 0%{?el7} )
%configure --enable-checker --enable-cgspell --enable-python-bindings
%else
%configure --enable-checker --enable-cgspell --disable-python-bindings
%endif
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot}/%{_libdir}/ -type f -name '*.pyc' -exec rm -f '{}' \;
find %{buildroot}/%{_libdir}/ -type f -name '*.pyo' -exec rm -f '{}' \;
find %{buildroot}/%{_libdir}/ -type f -name '*.la' -exec rm -f '{}' \;
find %{buildroot}/%{_libdir}/ -type f -name '*.a' -exec rm -f '{}' \;

%check
export LC_ALL=%(locale -a | grep -i utf | head -n1)
make check

%files
%defattr(-,root,root)
%doc AUTHORS NEWS README README.org
%{_bindir}/*
%{_datadir}/man/man1/*
%{_datadir}/divvun-gramcheck

%files -n libdivvun0
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n libdivvun-devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so

%if ! ( 0%{?el7} )
%files -n python3-libdivvun
%defattr(-,root,root)
%{python3_sitearch}/*
%endif

%post -n libdivvun0 -p /sbin/ldconfig

%postun -n libdivvun0 -p /sbin/ldconfig

%changelog
* Fri Dec 19 2014 Tino Didriksen <tino@didriksen.cc> 0.2.0
- Initial release
