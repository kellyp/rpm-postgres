%global pgmajorversion 92
%global pginstdir /usr/pgsql-9.2
%global sname pg_bulkload

Summary:	High speed data loading utility for PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	3.1.1
Release:	1%{?dist}
URL:		http://pgfoundry.org/projects/pgbulkload/
Source0:	http://ftp.postgresql.org/pub/projects/pgFoundry/pgbulkload/%{sname}-%{version}.tar.gz
Patch0:		pg_bulkload-makefile.patch
License:	BSD
Group:		Applications/Databases
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
pg_bulkload provides high-speed data loading capability to PostgreSQL users.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build

make USE_PGXS=1 %{?_smp_mflags}

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/%{name}
install -m 755 lib/pg_bulkload.so %{buildroot}%{_libdir}
install -m 755 util/pg_timestamp.so %{buildroot}%{_libdir}
install -m 755 bin/pg_bulkload %{buildroot}%{_bindir}
install -m 755 bin/postgresql %{buildroot}%{_bindir}/pg_bulkload_ctl
install -m 644 lib/pg_bulkload.sql %{buildroot}%{_datadir}/%{name}/
install -m 644 bin/sql/*.sql %{buildroot}%{_datadir}/%{name}/
install -m 644 lib/uninstall_pg_bulkload.sql %{buildroot}%{_datadir}/%{name}/
install -m 644 util/pg_timestamp.sql %{buildroot}%{_datadir}/%{name}/
install -m 644 util/uninstall_pg_timestamp.sql %{buildroot}%{_datadir}/%{name}/
install -m 644 sample* %{buildroot}%{_datadir}/%{name}/

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/pg_bulkload.so
%{_libdir}/pg_timestamp.so
%{_bindir}/pg_bulkload
%{_bindir}/pg_bulkload_ctl
%{_datadir}/%{name}/pg_bulkload.sql
%{_datadir}/%{name}/*.sql
%{_datadir}/%{name}/sample*
%doc README.pg_bulkload

%changelog
* Fri Jan 22 2010 Devrim GUNDUZ <devrim@gunduz.org> 3.0a2-1
- Update to 3.0a2

* Fri Apr 18 2008 Devrim GUNDUZ <devrim@gunduz.org> 2.3.0-1
- Initial packaging for PGDG Repository
