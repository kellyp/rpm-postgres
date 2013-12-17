%global	pgmajorversion 91
%global pginstdir	/usr/pgsql-9.1
%global sname	pg_reorg

Summary:	Reorganize tables in PostgreSQL databases without any locks
Name:		%{sname}%{pgmajorversion}
Version:	1.1.7
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	ftp://ftp.postgresql.org/pub/projects/pgFoundry/reorg/%{sname}-%{version}.tar.gz
Patch0:		pg_reorg-makefile-pgxs.patch
URL:		http://pgfoundry.org/projects/%{sname}/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)

BuildRequires:	postgresql%{pgmajorversion}-devel, postgresql%{pgmajorversion}
Requires:	postgresql%{pgmajorversion}

%description 	
pg_reorg can re-organize tables on a postgres database without any locks so that 
you can retrieve or update rows in tables being reorganized. 
The module is developed to be a better alternative of CLUSTER and VACUUM FULL.

%prep
%setup -q -n %{sname}
%patch0 -p0

%build
USE_PGXS=1 make %{?_smp_mflags}

%install
rm -rf %{buildroot}
USE_PGXS=1 make DESTDIR=%{buildroot} install

%files
%defattr(644,root,root)
%doc COPYRIGHT doc/*
%attr (755,root,root) %{pginstdir}/bin/pg_reorg
%attr (755,root,root) %{pginstdir}/lib/pg_reorg.so
%{pginstdir}/share/contrib/pg_reorg.sql
%{pginstdir}/share/contrib/uninstall_pg_reorg.sql

%clean
rm -rf %{buildroot}

%changelog
* Fri Mar 23 2012 - Devrim Gunduz <devrim@gunduz.org> 1.1.7-1
- Initial packaging for PostgreSQL RPM Repository, based on the
  NTT spec, simplified and modified for PostgreSQL RPM compatibility.
- Cleaned up various rpmlint errors and warnings.
