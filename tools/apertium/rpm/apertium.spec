Name: apertium
Version: 3.6.0
Release: 1%{?dist}
Summary: Shallow-transfer machine translation engine
Group: Development/Tools
License: GPL-2.0+
URL: https://apertium.org/
Source0: %{name}_%{version}.orig.tar.bz2

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: flex
BuildRequires: gcc-c++
BuildRequires: libtool
BuildRequires: libxml2
BuildRequires: libxml2-devel
BuildRequires: libxslt
BuildRequires: lttoolbox-devel
BuildRequires: pcre-devel
BuildRequires: pkgconfig
BuildRequires: python3
BuildRequires: python3-devel
BuildRequires: swig
BuildRequires: libzip-tools
BuildRequires: unzip
BuildRequires: zip

Requires: libapertium3-3_6-1 = %{version}-%{release}
Requires: lttoolbox >= 3.5.0
# Require xmllint from:
Requires: libxml2
# Require xsltproc from:
Requires: libxslt

%description
An open-source shallow-transfer machine translation
engine, Apertium is initially aimed at related-language pairs.

It uses finite-state transducers for lexical processing,
hidden Markov models for part-of-speech tagging, and
finite-state based chunking for structural transfer.

The system is largely based upon systems already developed by
the Transducens  group at the Universitat d'Alacant, such as
interNOSTRUM (Spanish-Catalan, http://www.internostrum.com/welcome.php)
and Traductor Universia (Spanish-Portuguese,
http://traductor.universia.net).

It will be possible to use Apertium to build machine translation
systems for a variety of related-language pairs simply providing
the linguistic data needed in the right format.

%package -n libapertium3-3_6-1
Summary: Shared library for apertium
Group: Development/Libraries
Provides: libapertium = %{version}-%{release}
Obsoletes: libapertium < %{version}-%{release}
Obsoletes: libapertium3 < %{version}-%{release}

%description -n libapertium3-3_6-1
Contains shared library for the Apertium shallow-transfer
machine translation engine.

%package -n apertium-devel
Summary: Development tools and library for apertium
Group: Development/Tools
Requires: apertium = %{version}-%{release}
Requires: lttoolbox-devel >= 3.5.0
Obsoletes: libapertium3-devel < %{version}-%{release}

%description -n apertium-devel
Contains development files for the Apertium shallow-transfer
machine translation engine.

%package -n python3-apertium-core
Summary: Python 3 module for the Apertium shallow-transfer machine translation engine
Requires: libapertium3-3_6-1 = %{version}-%{release}

%description -n python3-apertium-core
Python 3 module for the Apertium shallow-transfer machine translation engine

%prep
%setup -q -n %{name}-%{version}

%build
export LC_ALL=%(locale -a | grep -i utf | head -n1)
autoreconf -fi
%configure --disable-static --enable-python-bindings
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/%{_libdir}/*.la
rm -f %{buildroot}/%{_datadir}/man/man1/*lextor*
ln -s libapertium3-3.6.so.1.0.0 %{buildroot}/%{_libdir}/libapertium3-3.6.so

%check
export LC_ALL=%(locale -a | grep -i utf | head -n1)
make check

%files
%defattr(-,root,root)
%doc AUTHORS NEWS README README-MODES
%{_bindir}/apertium
%{_bindir}/apertium-cleanstream
%{_bindir}/apertium-des*
%{_bindir}/apertium-interchunk
%{_bindir}/apertium-multiple-translations
%{_bindir}/apertium-postchunk
%{_bindir}/apertium-postlatex
%{_bindir}/apertium-postlatex-raw
%{_bindir}/apertium-prelatex
%{_bindir}/apertium-preprocess-transfer
%{_bindir}/apertium-pretransfer
%{_bindir}/apertium-re*
%{_bindir}/apertium-tagger
%{_bindir}/apertium-tmxbuild
%{_bindir}/apertium-transfer
%{_bindir}/apertium-unformat
%{_bindir}/apertium-utils-fixlatex
%{_datadir}/%{name}
%{_datadir}/man/man1/apertium.*
%{_datadir}/man/man1/apertium-des*
%{_datadir}/man/man1/apertium-interchunk.*
%{_datadir}/man/man1/apertium-multiple-translations.*
%{_datadir}/man/man1/apertium-postchunk.*
%{_datadir}/man/man1/apertium-postlatex.*
%{_datadir}/man/man1/apertium-postlatex-raw.*
%{_datadir}/man/man1/apertium-prelatex.*
%{_datadir}/man/man1/apertium-preprocess-transfer.*
%{_datadir}/man/man1/apertium-pretransfer.*
%{_datadir}/man/man1/apertium-re*
%{_datadir}/man/man1/apertium-tagger.*
%{_datadir}/man/man1/apertium-transfer.*
%{_datadir}/man/man1/apertium-unformat.*
%{_datadir}/man/man1/apertium-utils-fixlatex.*

%files -n libapertium3-3_6-1
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n apertium-devel
%defattr(-,root,root)
%{_bindir}/apertium-filter-ambiguity
%{_bindir}/apertium-filter-dix
%{_bindir}/apertium-filter-rules
%{_bindir}/apertium-gen-deformat
%{_bindir}/apertium-gen-modes
%{_bindir}/apertium-gen-reformat
%{_bindir}/apertium-genvdix
%{_bindir}/apertium-genvldix
%{_bindir}/apertium-genvrdix
%{_bindir}/apertium-get
%{_bindir}/apertium-metalrx
%{_bindir}/apertium-metalrx-to-lrx
%{_bindir}/apertium-perceptron-trace
%{_bindir}/apertium-tagger-apply-new-rules
%{_bindir}/apertium-tagger-readwords
%{_bindir}/apertium-translate-to-default-equivalent
%{_bindir}/apertium-validate-acx
%{_bindir}/apertium-validate-dictionary
%{_bindir}/apertium-validate-interchunk
%{_bindir}/apertium-validate-modes
%{_bindir}/apertium-validate-postchunk
%{_bindir}/apertium-validate-tagger
%{_bindir}/apertium-validate-transfer
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%{_datadir}/aclocal/*
%{_datadir}/man/man1/apertium-filter-ambiguity.*
%{_datadir}/man/man1/apertium-gen-*
%{_datadir}/man/man1/apertium-tagger-apply-new-rules.*
%{_datadir}/man/man1/apertium-validate-*

%files -n python3-apertium-core
%defattr(-,root,root)
%{python3_sitearch}/*

%post -n libapertium3-3_6-1 -p /sbin/ldconfig

%postun -n libapertium3-3_6-1 -p /sbin/ldconfig

%changelog
* Fri Sep 05 2014 Tino Didriksen <tino@didriksen.cc> 3.3.0
- Initial version of the package
