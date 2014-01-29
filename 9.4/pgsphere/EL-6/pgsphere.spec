%global pgmajorversion 93
%global pginstdir /usr/pgsql-9.4devel
%global sname pgsphere

Summary:	R-Tree implementation using GiST for spherical objects
Name:           %{sname}%{pgmajorversion}
Version:	1.1.1
Release:	2%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://ftp.postgresql.org/pub/projects/pgFoundry/%{sname}/%{sname}/%{version}/%{sname}-%{version}.tar.gz
Patch0:		pgsphere-pg92-languages.patch
URL:		http://pgfoundry.org/projects/pgsphere
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
pgSphere is a server side module for PostgreSQL. It contains methods for 
working with spherical coordinates and objects. It also supports indexing of 
spherical objects.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
make PG_CONFIG=%{pginstdir}/bin/pg_config USE_PGXS=1 %{?_smp_mflags} 

%install
rm -rf %{buildroot}
DESTDIR=%{buildroot} PG_CONFIG=%{pginstdir}/bin/pg_config USE_PGXS=1 make install %{?_smp_mflags}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig 
%postun -p /sbin/ldconfig 

%files
%defattr(-,root,root,-)
%doc %{_docdir}/pgsql/contrib/README.pg_sphere 
%doc %{_docdir}/pgsql/contrib/COPYRIGHT.pg_sphere
%{pginstdir}/lib/pg_sphere.so
%{pginstdir}/share/contrib/pg_sphere.sql

%changelog
* Mon Apr 15 2013 - Devrim GUNDUZ <devrim@gunduz.org> 1.1.1-2
- Fix packaging issues, per report from Yukio Yamamoto:
  * Install pg_sphere.so under correct location. Actually
     trust make install there, do not manually install files.
  * Fix pg_sphere.sql, so that it can be loaded w/o errors to 
    PostgreSQL 9.2.
- Update download URL.

* Wed Jan 5 2011 - Devrim GUNDUZ <devrim@gunduz.org> 1.1.1-1
- Update to 1.1.1, per: 
  http://pgfoundry.org/forum/forum.php?forum_id=1665

* Tue Jul 28 2009 - Devrim GUNDUZ <devrim@gunduz.org> 1.1.0-1
- Update to 1.1.0

* Wed Aug 20 2008 - Devrim GUNDUZ <devrim@gunduz.org> 1.0.1-1
- Update to 1.0.1

* Wed Apr 9 2008 - Devrim GUNDUZ <devrim@gunduz.org> 1.0.0-1
- Initial RPM packaging for Fedora
