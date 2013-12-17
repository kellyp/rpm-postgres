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

Name:		postgresql-odbc
Summary:	PostgreSQL ODBC driver
Version:	08.04.0200
Release:	1PGDG%{?dist}
License:	LGPLv2
Group:		Applications/Databases
Url:		http://psqlodbc.projects.postgresql.org/

Source0:	ftp://ftp.postgresql.org/pub/odbc/versions/src/psqlodbc-%{version}.tar.gz
Source1:	acinclude.m4

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	unixODBC-devel
BuildRequires:	libtool automake autoconf postgresql-devel
BuildRequires:	openssl-devel krb5-devel pam-devel zlib-devel readline-devel

Requires:	postgresql-libs >= 8.0

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

./configure --with-unixodbc -disable-dependency-tracking --libdir=%{_libdir}

make

%install
rm -rf %{buildroot}
%makeinstall

# Provide the old library name "psqlodbc.so" as a symlink,
# and remove the rather useless .la file

install -d -m 755 %{buildroot}%{_libdir}/
pushd %{buildroot}%{_libdir}
	ln -s psqlodbcw.so psqlodbc.so
	rm %{buildroot}%{_libdir}/psqlodbcw.la
popd
strip %{buildroot}%{_libdir}/*.so

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%attr(755,root,root) %{_libdir}/psqlodbcw.so
%{_libdir}/psqlodbc.so
%doc license.txt readme.txt 

%changelog
* Tue Mar 9 2010 Devrim GUNDUZ <devrim@gunduz.org> 08.04.0200-1PGDG
- Update to 08.04.0200
- Remove --with-odbcinst parameter.
- Update URL.
- Update license
- Add new BRs, per Fedora spec.
- Use build system's libtool.m4, not the one in the package.
- Since it looks like upstream has decided to stick with psqlodbcw.so
  permanently, allow the library to have that name.  But continue to
  provide psqlodbc.so as a symlink.
- Add -disable-dependency-tracking, per Fedora spec.
- Trim changelog (see svn repo for history)
