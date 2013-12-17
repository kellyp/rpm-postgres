%global pgmajorversion 93
%global pginstdir /usr/pgsql-9.3
%global sname pgmemcache

Summary:	A PostgreSQL API to interface with memcached
Name:		%{sname}-%{pgmajorversion}
Version:	2.1.2
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/ohmu/%{sname}/archive/%{version}.tar.gz
Patch0:		%{sname}-makefile.patch
URL:		http://pgfoundry.org/projects/pgmemcache
BuildRequires:	postgresql%{pgmajorversion}-devel, libmemcached-devel, cyrus-sasl-devel
Requires:	postgresql%{pgmajorversion}-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
pgmemcache is a set of PostgreSQL user-defined functions that provide
an interface to memcached.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
make USE_PGXS=1 %{?_smp_mflags} 

%install
rm -rf %{buildroot}
make USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig 
%postun -p /sbin/ldconfig 

%files
%defattr(644,root,root,755)
%doc README LICENSE NEWS TODO
%{pginstdir}/lib/pgmemcache.so
%{pginstdir}/share/extension/pgmemcache--*.sql
%{pginstdir}/share/extension/pgmemcache.control

%changelog
* Wed Nov 20 2013 - Devrim GÜNDÜZ <devrim@gunduz.org> 2.1.2-1
- Update to 2.1.2
- Fix various issues in init script

* Sat Jul 3 2010 - Devrim GÜNDÜZ <devrim@gunduz.org> 2.0.4-1
- Initial packaging for PostgreSQL RPM Repository
