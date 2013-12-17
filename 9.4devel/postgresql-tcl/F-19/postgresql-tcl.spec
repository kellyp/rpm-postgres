%global pgmajorversion 93
%global pginstdir /usr/pgsql-9.3

Name:           postgresql%{pgmajorversion}-tcl
Version:	2.0.0
Release:	1%{?dist}
Summary:	A Tcl client library for PostgreSQL

Group:		Applications/Databases
URL:		http://sourceforge.net/projects/pgtclng/
License:	PostgreSQL

Source0:        http://downloads.sourceforge.net/pgtclng/pgtcl%{version}.tar.gz
Source1:        http://downloads.sourceforge.net/pgtclng/Manual/20110918/pgtcldocs-20110918.zip

Patch1:		pgtcl-no-rpath.patch

Provides:	pgtcl = %{version}-%{release}
# pgtcl was originally shipped as a sub-RPM of the PostgreSQL package;
# these Provides/Obsoletes give a migration path.  The cutoff EVR was
# chosen to be later than anything we are likely to ship in Fedora 12.
Provides:	postgresql%{pgmajorversion}-tcl = 8.5.0-1
Obsoletes:	postgresql-tcl < 8.5

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:	postgresql%{pgmajorversion}-devel tcl-devel
BuildRequires:	autoconf

Requires:	tcl(abi) = 8.5

%{!?tcl_version: %global tcl_version %(echo 'puts $tcl_version' | tclsh)}
%{!?tcl_sitearch: %global tcl_sitearch %{_libdir}/tcl%{tcl_version}}

%description
PostgreSQL is an advanced Object-Relational database management system.
The tcl-pgtcl package contains Pgtcl, a Tcl client library for connecting
to a PostgreSQL server.

%prep
%setup -q -n pgtcl%{version}

unzip %{SOURCE1}
PGTCLDOCDIR=`basename %{SOURCE1} .zip`
mv $PGTCLDOCDIR Pgtcl-docs

%patch1 -p1

autoconf

%build

./configure --libdir=%{tcl_sitearch} --with-tcl=%{_libdir} --with-postgres-include=%{pginstdir}/include --with-postgres-lib=%{pginstdir}/lib

# note: as of pgtcl 1.5.2, its makefile is not parallel-safe
make all

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}
# we don't really need to ship the .h file
rm -f %{buildroot}%{_includedir}/libpgtcl.h

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_libdir}/tcl%{tcl_version}/pgtcl%{version}/
%doc Pgtcl-docs/*

%changelog
* Thu Nov 10 2011 Devrim Gunduz <devrim@gunduz.org> 2.0.0-1
- Update to 2.0.0
- Use better download URLs.

* Tue Aug 09 2011 Devrim Gunduz <devrim@gunduz.org> 1.9.0-1
- Update to 1.9.0, per #65.

* Fri Mar 12 2010 Devrim Gunduz <devrim@gunduz.org> 1.8.0-1
- Update to 1.8.0, per:
  http://pgfoundry.org/forum/forum.php?forum_id=1766

* Fri Mar 12 2010 Devrim Gunduz <devrim@gunduz.org> 1.7.1-1
- Use Fedora's spec for consistency, and update to 1.7.1
- Update spec for 9.0 multiple postmaster support.
