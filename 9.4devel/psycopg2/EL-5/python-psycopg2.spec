# Python major version.
%{expand: %%define pyver %(python -c 'import sys;print(sys.version[0:3])')}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define ZPsycopgDAdir %{_localstatedir}/lib/zope/Products/ZPsycopgDA

%global pgmajorversion 93
%global pginstdir /usr/pgsql-9.4devel
%global sname psycopg2

Summary:	A PostgreSQL database adapter for Python
Name:		python-%{sname}
Version:	2.5.1
Release:	1%{?dist}
Source0:	http://initd.org/psycopg/tarballs/PSYCOPG-2-5/%{sname}-%{version}.tar.gz
Patch0:		setup.cfg.patch
License:	GPL (with Exceptions)
Group:		Applications/Databases
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Url:		http://www.psycopg.org/psycopg/
BuildRequires:	python-devel postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-libs

%description
psycopg is a PostgreSQL database adapter for the Python programming
language (just like pygresql and popy.) It was written from scratch 
with the aim of being very small and fast, and stable as a rock. The 
main advantages of psycopg are that it supports the full Python
DBAPI-2.0 and being thread safe at level 2.

%package doc
Summary:	Documentation for psycopg python PostgreSQL database adapter
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description doc
Documentation and example files for the psycopg python PostgreSQL
database adapter.

%package test
Summary:	Tests for psycopg2
Group:		Development Libraries
Requires:	%{name} = %{version}-%{release}

%description test
Tests for psycopg2.

%package zope
Summary:	Zope Database Adapter ZPsycopgDA
Group:		Applications/Databases
Requires:	%{name} = %{version}-%{release} zope

%description zope
Zope Database Adapter for PostgreSQL, called ZPsycopgDA

%prep
%setup -q -n psycopg2-%{version}
%patch0 -p0

%build
python setup.py build
# Fix for wrong-file-end-of-line-encoding problem; upstream also must fix this.
for i in `find doc -iname "*.html"`; do sed -i 's/\r//' $i; done
for i in `find doc -iname "*.css"`; do sed -i 's/\r//' $i; done

%install
rm -Rf %{buildroot}
mkdir -p %{buildroot}%{python_sitearch}/psycopg2
python setup.py install --no-compile --root %{buildroot}

install -d %{buildroot}%{ZPsycopgDAdir}
cp -pr ZPsycopgDA/* %{buildroot}%{ZPsycopgDAdir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS INSTALL LICENSE README NEWS
%dir %{python_sitearch}/psycopg2
%{python_sitearch}/psycopg2/*.py
%{python_sitearch}/psycopg2/*.pyc
%{python_sitearch}/psycopg2/*.so
%{python_sitearch}/psycopg2/*.pyo

%files doc
%defattr(-,root,root)
%doc doc examples/

%files test
%defattr(-,root,root)
%{python_sitearch}/%{sname}/tests/*

%files zope
%defattr(-,root,root)
%dir %{ZPsycopgDAdir}
%{ZPsycopgDAdir}/*.py
%{ZPsycopgDAdir}/*.pyo
%{ZPsycopgDAdir}/*.pyc
%{ZPsycopgDAdir}/dtml/*
%{ZPsycopgDAdir}/icons/*

%changelog
* Sun Jun 30 2013 Devrim GUNDUZ <devrim@gunduz.org> 2.5.1-1
- Update to 2.5.1, per changes described at:
  http://www.psycopg.org/psycopg/articles/2013/06/23/psycopg-251-released/

* Thu Apr 11 2013 Devrim GUNDUZ <devrim@gunduz.org> 2.5-1
- Update to 2.5, per changes described at:
  http://www.psycopg.org/psycopg/articles/2013/04/07/psycopg-25-released/

* Wed Dec 12 2012 Devrim GUNDUZ <devrim@gunduz.org> 2.4.6-1
- Update to 2.4.6, per changes described at:
  http://www.psycopg.org/psycopg/articles/2012/12/12/psycopg-246-released/

* Thu Jul 5 2012 Devrim GUNDUZ <devrim@gunduz.org> 2.4.5-1
- Update to 2.4.5

* Mon Dec 19 2011 Devrim GUNDUZ <devrim@gunduz.org> 2.4.4-1
- Update to 2.4.4

* Mon Aug 22 2011 Devrim GUNDUZ <devrim@gunduz.org> 2.4.2-1
- Update to 2.4.2
- Add a patch for pg_config path.
- Add new subpackage: test

* Tue Mar 16 2010 Devrim GUNDUZ <devrim@gunduz.org> 2.0.14-1
- Update to 2.0.14

* Mon Oct 19 2009 Devrim GUNDUZ <devrim@gunduz.org> 2.0.13-1
- Update to 2.0.13

* Mon Sep 7 2009 Devrim GUNDUZ <devrim@gunduz.org> 2.0.12-1
- Update to 2.0.12

* Tue May 26 2009 Devrim GUNDUZ <devrim@gunduz.org> 2.0.11-1
- Update to 2.0.11

* Fri Apr 24 2009 Devrim GUNDUZ <devrim@gunduz.org> 2.0.10-1
- Update to 2.0.10

* Thu Mar 2 2009 Devrim GUNDUZ <devrim@gunduz.org> 2.0.9-1
- Update to 2.0.9

* Wed Apr 30 2008 - Devrim GUNDUZ <devrim@gunduz.org> 2.0.7-1
- Update to 2.0.7

* Fri Jun 15 2007 - Devrim GUNDUZ <devrim@gunduz.org> 2.0.6-1
- Update to 2.0.6

* Sun May 06 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info>
- rebuilt for RHEL5 final

* Wed Dec 6 2006 - Devrim GUNDUZ <devrim@gunduz.org> 2.0.5.1-4
- Rebuilt for PostgreSQL 8.2.0

* Mon Sep 11 2006 - Devrim GUNDUZ <devrim@gunduz.org> 2.0.5.1-3
- Rebuilt

* Wed Sep 6 2006 - Devrim GUNDUZ <devrim@gunduz.org> 2.0.5.1-2
- Remove ghost'ing, per Python Packaging Guidelines

* Mon Sep 4 2006 - Devrim GUNDUZ <devrim@gunduz.org> 2.0.5.1-1
- Update to 2.0.5.1

* Sun Aug 6 2006 - Devrim GUNDUZ <devrim@gunduz.org> 2.0.3-3
- Fixed zope package dependencies and macro definition, per bugzilla review (#199784)
- Fixed zope package directory ownership, per bugzilla review (#199784)
- Fixed cp usage for zope subpackage, per bugzilla review (#199784)

* Mon Jul 31 2006 - Devrim GUNDUZ <devrim@gunduz.org> 2.0.3-2
- Fixed 64 bit builds
- Fixed license
- Added Zope subpackage
- Fixed typo in doc description
- Added macro for zope subpackage dir

* Mon Jul 31 2006 - Devrim GUNDUZ <devrim@gunduz.org> 2.0.3-1
- Update to 2.0.3
- Fixed spec file, per bugzilla review (#199784)

* Sat Jul 22 2006 - Devrim GUNDUZ <devrim@gunduz.org> 2.0.2-3
- Removed python dependency, per bugzilla review. (#199784)
- Changed doc package group, per bugzilla review. (#199784)
- Replaced dos2unix with sed, per guidelines and bugzilla review (#199784)
- Fix changelog dates

* Sat Jul 21 2006 - Devrim GUNDUZ <devrim@gunduz.org> 2.0.2-2
- Added dos2unix to buildrequires
- removed python related part from package name

* Fri Jul 20 2006 - Devrim GUNDUZ <devrim@gunduz.org> 2.0.2-1
- Fix rpmlint errors, including dos2unix solution
- Re-engineered spec file

* Fri Jan 23 2006 - Devrim GUNDUZ <devrim@gunduz.org>
- First 2.0.X build

* Fri Jan 23 2006 - Devrim GUNDUZ <devrim@gunduz.org>
- Update to 1.2.21

* Tue Dec 06 2005 - Devrim GUNDUZ <devrim@gunduz.org>
- Initial release for 1.1.20
