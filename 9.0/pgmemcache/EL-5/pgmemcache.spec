%global pginstdir /usr/pgsql-9.0
%global pgmajorversion pg-9.0

Summary:	A PostgreSQL API to interface with memcached
Name:		pgmemcache
Version:	2.0.4
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://pgfoundry.org/frs/download.php/2672/%{name}_%{version}.tar.bz2
URL:		http://pgfoundry.org/projects/pgmemcache
BuildRequires:	postgresql-devel >= 8.4
Requires:	postgresql-server >= 8.4
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
pgmemcache is a set of PostgreSQL user-defined functions that provide
an interface to memcached.

%prep
%setup -q -n %{name}

%build
make USE_PGXS=1 %{?_smp_mflags} 

%install
rm -rf %{buildroot}

install -d %{buildroot}%{pginstdir}/lib/
install -d %{buildroot}%{_datadir}/%{name}-%{version}-%{pgmajorversion}
install -d %{buildroot}%{_docdir}/%{name}-%{version}-%{pgmajorversion}

install -m 755 %{name}.so %{buildroot}%{pginstdir}/lib/%{name}.so
install -m 755 test.sql %{name}.sql %{buildroot}%{_datadir}/%{name}-%{version}-%{pgmajorversion}/
install -m 755 README.%{name} LICENSE COPYING NEWS %{buildroot}%{_docdir}/%{name}-%{version}-%{pgmajorversion}/


%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig 
%postun -p /sbin/ldconfig 

%files
%defattr(644,root,root,755)
%doc %{_docdir}/%{name}-%{version}-%{pgmajorversion}/README.%{name}
%doc %{_docdir}/%{name}-%{version}-%{pgmajorversion}/LICENSE
%doc %{_docdir}/%{name}-%{version}-%{pgmajorversion}/COPYING
%doc %{_docdir}/%{name}-%{version}-%{pgmajorversion}/NEWS
%{_datadir}/%{name}-%{version}-%{pgmajorversion}/*.sql
%{pginstdir}/lib/%{name}.so

%changelog
* Sat Jul 3 2010 - Devrim GÜNDÜZ <devrim@gunduz.org> 2.0.4-1
- Initial packaging for PostgreSQL RPM Repository
