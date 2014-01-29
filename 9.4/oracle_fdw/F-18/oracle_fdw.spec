%global pgmajorversion 93
%global pginstdir /usr/pgsql-9.4devel
%define sname	oracle_fdw

Summary:	A PostgreSQL Foreign Data Wrapper for Oracle.
Name:		%{sname}%{pgmajorversion}
Version:	0.9.7
Release:	1%{?dist}
Group:		Applications/Databases
License:	PostgreSQL
URL:		http://oracle-fdw.projects.postgresql.org/
Source0:	http://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	postgresql%{pgmajorversion}-server
BuildRequires:	oracle-instantclient11.2-basic
BuildRequires:	oracle-instantclient11.2-devel
Requires:	postgresql%{pgmajorversion}-server
Requires:	oracle-instantclient11.2-basic

# Override RPM dependency generation to filter out libclntsh.so.
# http://fedoraproject.org/wiki/PackagingDrafts/FilteringAutomaticDependencies
%global		_use_internal_dependency_generator 0

%description
Provides a Foreign Data Wrapper for easy and efficient read access from
PostgreSQL to Oracle databases, including pushdown of WHERE conditions and
required columns as well as comprehensive EXPLAIN support.

%prep
%setup -q -n %{sname}-%{version}

%build
make PG_CONFIG=%{pginstdir}/bin/pg_config %{?_smp_mflags}

%install
%{__rm} -rf  %{buildroot}
make install DESTDIR=%{buildroot} PG_CONFIG=%{pginstdir}/bin/pg_config %{?_smp_mflags}
mv %{buildroot}/usr/share/doc/pgsql/extension/README.oracle_fdw %{buildroot}%{pginstdir}/share/extension

%check
make installcheck PG_CONFIG=%{pginstdir}/bin/pg_config %{?_smp_mflags} PGUSER=postgres

%clean
%{__rm} -rf  %{buildroot}

%files
%defattr(-,root,root,-)
%{pginstdir}/lib/*.so
%{pginstdir}/share/extension/*.sql
%{pginstdir}/share/extension/*.control
%{pginstdir}/share/extension/README.*

%changelog
* Mon Oct 8 2012 David E. Wheeler <david.wheeler@iovation.com> 0.9.7-1
- Initial RPM
 
