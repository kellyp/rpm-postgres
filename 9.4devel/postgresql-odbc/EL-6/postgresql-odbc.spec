# Conventions for PostgreSQL Global Development Group RPM releases:

# Official PostgreSQL Development Group RPMS have a PGDG after the release number.
# Integer releases are stable -- 0.1.x releases are Pre-releases, and x.y are
# test releases.

# Pre-releases are those that are built from CVS snapshots or pre-release
# tarballs from postgresql.org.  Official beta releases are not
# considered pre-releases, nor are release candidates, as their beta or
# release candidate status is reflected in the version of the tarball. Pre-
# releases' versions do not change -- the pre-release tarball of 7.0.3, for
# example, has the same tarball version as the final official release of 7.0.3:

# Major Contributors:
# ---------------
# Tom Lane
# Devrim Gunduz

# This spec file and ancilliary files are licensed in accordance with
# The PostgreSQL license.
# In this file you can find the default build package list macros.  These can be overridden by defining
# on 

%global pgmajorversion 93
%global	pginstdir /usr/pgsql-9.3

Name:		postgresql%{pgmajorversion}-odbc
Summary:	PostgreSQL ODBC driver
Version:	09.02.0100
Release:	1PGDG%{?dist}
License:	LGPLv2
Group:		Applications/Databases
Url:		http://psqlodbc.projects.postgresql.org/

Source0:	ftp://ftp.postgresql.org/pub/odbc/versions/src/psqlodbc-%{version}.tar.gz
Source1:	acinclude.m4

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	unixODBC-devel
BuildRequires:	libtool automake autoconf postgresql%{pgmajorversion}-devel
BuildRequires:	openssl-devel krb5-devel pam-devel zlib-devel readline-devel

Requires:	postgresql%{pgmajorversion}-libs

# This spec file and ancillary files are licensed in accordance with 
# the psqlodbc license.

%description
This package includes the driver needed for applications to access a
PostgreSQL system via ODBC (Open Database Connectivity).

%prep
%setup -q -n psqlodbc-%{version}

# Some missing macros.  Courtesy Owen Taylor <otaylor@redhat.com>.
cp -p %{SOURCE1} .
# Use build system's libtool.m4, not the one in the package.
rm -f libtool.m4

libtoolize --force  --copy
aclocal -I .
automake --add-missing --copy
autoconf
autoheader

%build

./configure --with-unixodbc --with-libpq=%{pginstdir} -disable-dependency-tracking --libdir=%{_libdir}

make

%install
rm -rf %{buildroot}
%makeinstall

# Provide the old library name "psqlodbc.so" as a symlink,
# and remove the rather useless .la file

install -d -m 755 %{buildroot}%{pginstdir}/lib
pushd %{buildroot}%{pginstdir}/lib
	ln -s psqlodbcw.so psqlodbc.so
	mv %{buildroot}%{_libdir}/psqlodbc*.so %{buildroot}%{pginstdir}/lib
	rm %{buildroot}%{_libdir}/psqlodbcw.la
popd
strip %{buildroot}%{pginstdir}/lib/*.so

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%attr(755,root,root) %{pginstdir}/lib/psqlodbcw.so
%{pginstdir}/lib/psqlodbc.so
%doc license.txt readme.txt 

%changelog
* Sat Nov 9 2013 - Devrim GUNDUZ <devrim@gunduz.org> - 09.02.0100-1
- Update to 09.02.0100

* Mon Sep 10 2012 - Devrim GUNDUZ <devrim@gunduz.org> - 09.01.0200
- Update to 09.01.0200 

* Tue Nov 8 2011 - Devrim GUNDUZ <devrim@gunduz.org> - 09.00.0310
- Update to 09.00.0310.

* Tue Nov 9 2010 - Devrim GUNDUZ <devrim@gunduz.org> - 09.00.0200
- Update to 09.00.0200, and also apply changes for new RPM layout.

* Tue Mar 9 2010 Devrim GUNDUZ <devrim@gunduz.org> 08.04.0200-1PGDG
- Update to 08.04.0200
- Use new parameter --with-libpq in order to support multiple version
  installation of PostgreSQL.
- Remove --with-odbcinst parameter.
- Add new global variable to support multiple version installation 
  of PostgreSQL.
- Update URL.
- Update license
- Add new BRs, per Fedora spec.
- Use build system's libtool.m4, not the one in the package.
- Since it looks like upstream has decided to stick with psqlodbcw.so
  permanently, allow the library to have that name.  But continue to
  provide psqlodbc.so as a symlink.
- Add -disable-dependency-tracking, per Fedora spec.
- Trim changelog (see svn repo for history)
