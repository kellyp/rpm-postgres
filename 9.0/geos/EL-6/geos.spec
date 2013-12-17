Name:		geos
Version:	3.3.8
Release:	1%{?dist}
Summary:	GEOS is a C++ port of the Java Topology Suite

Group:		Applications/Engineering
License:	LGPLv2
URL:		http://trac.osgeo.org/geos/
Source0:	http://download.osgeo.org/geos/%{name}-%{version}.tar.bz2
Patch0:		geos-gcc43.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	doxygen libtool
BuildRequires:	swig ruby
BuildRequires:	python-devel

%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%description
GEOS (Geometry Engine - Open Source) is a C++ port of the Java Topology 
Suite (JTS). As such, it aims to contain the complete functionality of 
JTS in C++. This includes all the OpenGIS "Simple Features for SQL" spatial 
predicate functions and spatial operators, as well as specific JTS topology 
functions such as IsValid()

%package devel
Summary:	Development files for GEOS
Group:		Development/Libraries
Requires: 	%{name} = %{version}-%{release}

%description devel
GEOS (Geometry Engine - Open Source) is a C++ port of the Java Topology 
Suite (JTS). As such, it aims to contain the complete functionality of 
JTS in C++. This includes all the OpenGIS "Simple Features for SQL" spatial 
predicate functions and spatial operators, as well as specific JTS topology 
functions such as IsValid()

This package contains the development files to build applications that 
use GEOS

%package python
Summary:	Python modules for GEOS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description python
Python module to build applications using GEOS and python

%prep
%setup -q
%patch0 -p0 -b .gcc43

%build

# fix python path on 64bit
sed -i -e 's|\/lib\/python|$libdir\/python|g' configure
sed -i -e 's|.get_python_lib(0|.get_python_lib(1|g' configure

# disable internal libtool to avoid hardcoded r-path
for makefile in `find . -type f -name 'Makefile.in'`; do
sed -i 's|@LIBTOOL@|%{_bindir}/libtool|g' $makefile
done

%configure --disable-static --disable-dependency-tracking \
           --enable-python
make %{?_smp_mflags}

# Make doxygen documentation files
cd doc
make doxygen-html

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%check

# test module
make %{?_smp_mflags} check || exit 0

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README TODO
%{_libdir}/libgeos-%{version}.so
%{_libdir}/libgeos_c.so.*
%exclude %{_libdir}/*.a

%files devel
%defattr(-,root,root,-)
%doc doc/doxygen_docs
%{_bindir}/geos-config
%{_includedir}/*
%{_libdir}/libgeos.so
%{_libdir}/libgeos_c.so
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.a

%files python
%defattr(-,root,root,-)
%dir %{python_sitearch}/%{name}
%exclude %{python_sitearch}/%{name}/_%{name}.a
%exclude %{python_sitearch}/%{name}/_%{name}.la
%{python_sitearch}/%{name}.pth
%{python_sitearch}/%{name}/*.py
%{python_sitearch}/%{name}/*.py?
%{python_sitearch}/%{name}/_%{name}.so

%changelog
* Thu Mar 14 2013 Devrim GUNDUZ <devrim@gunduz.org> - 3.3.8-1
- Update to 3.3.8, per changes described at:
  http://trac.osgeo.org/geos/browser/tags/3.3.8/NEWS

* Tue Jul 3 2012 Devrim GUNDUZ <devrim@gunduz.org> - 3.3.5-1
- Update to 3.3.5, per changes described at:
  http://trac.osgeo.org/geos/browser/tags/3.3.5/NEWS

* Fri Jun 1 2012 Devrim GUNDUZ <devrim@gunduz.org> - 3.3.4-1
- Update to 3.3.4

* Wed Apr 4 2012 Devrim GUNDUZ <devrim@gunduz.org> - 3.3.3-1
- Update to 3.3.3

* Mon Jan 9 2012 Devrim GUNDUZ <devrim@gunduz.org> - 3.3.2-1
- Update to 3.3.2

* Tue Oct 4 2011 Devrim GUNDUZ <devrim@gunduz.org> - 3.3.1-1
- Update to 3.3.1

* Tue Aug 9 2011 Devrim GUNDUZ <devrim@gunduz.org> - 3.3.0-1
- Update to 3.3.0

* Thu May 27 2010 Devrim GUNDUZ <devrim@gunduz.org> - 3.2.2-1
- Update to 3.2.2

* Mon Jun 29 2009 Devrim GUNDUZ <devrim@gunduz.org> - 3.1.1-1
- Update to 3.1.1

* Tue Dec 2 2008 Devrim GUNDUZ <devrim@gunduz.org> - 3.0.3-1
- Update to 3.0.3
- Remove patch 1 -- it is now in upstream.

* Mon Jun 2 2008 Devrim GUNDUZ <devrim@gunduz.org> - 3.0.0-4
- Sync with Fedora spec file.

* Wed May 28 2008 Balint Cristian <rezso@rdsor.ro> - 3.0.0-4
- disable bindings for REL4

* Wed Apr 23 2008 Balint Cristian <rezso@rdsor.ro> - 3.0.0-3
- require ruby too

* Wed Apr 23 2008 Balint Cristian <rezso@rdsor.ro> - 3.0.0-2
- remove python-abi request, koji fails

* Sun Apr 20 2008 Balint Cristian <rezso@rdsor.ro> - 3.0.0-1
- New branch upstream
- Fix gcc43 build
- Avoid r-path hardcoding
- Enable and include python module
- Enable and include ruby module
- Enable and run testsuite during build

* Thu Apr 3 2008 Devrim GUNDUZ <devrim@gunduz.org> - 0:2.2.3-2
- Initial build for pgsqlrpms.org, based on Fedora/EPEL spec.

