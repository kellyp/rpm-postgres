%global pgmajorversion 93
%global pginstdir /usr/pgsql-9.3

Name:           repmgr
Version:        1.2.0
Release:        1%{?dist}
Summary:        Replication Manager for	PostgreSQL Clusters
Group:		Applications/Databases
License:        GPLv3
URL:            http://www.repmgr.org
Source0:        http://repmgr.org/download/%{name}-%{version}.tar.gz
Patch0:		repmgr-makefile-pgxs.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  postgresql%{pgmajorversion}
Requires:       postgresql%{pgmajorversion}-server

%description
repmgr is a set of open source tools that helps DBAs and System 
administrators manage a cluster of PostgreSQL databases..

By taking advantage of the Hot Standby capability introduced in 
PostgreSQL 9, repmgr greatly simplifies the process of setting up and 
managing database with high availability and scalability requirements.

repmgr simplifies administration and daily management, enhances 
productivity and reduces the overall costs of a PostgreSQL cluster by:
  * monitoring the replication process;
  * allowing DBAs to issue high availability operations such as
switch-overs and fail-overs.

%prep
%setup -q
%patch0 -p0

%build
USE_PGXS=1 make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%{__mkdir} -p %{buildroot}/%{pginstdir}/bin/
USE_PGXS=1 make install DESTDIR=%{buildroot}
#mv repmgr %{buildroot}/%{pginstdir}/bin/

%clean
make USE_PGXS=1 clean

%files
%doc COPYRIGHT CREDITS HISTORY LICENSE README.rst TODO 
%dir %{pginstdir}/bin
%{pginstdir}/bin/repmgr
%{pginstdir}/bin/repmgrd
%{pginstdir}/share/contrib/repmgr.sql
%{pginstdir}/share/contrib/uninstall_repmgr.sql

%changelog
* Fri Jul 27 2012 - Devrim GUNDUZ <devrim@gunduz.org> 1.2.0-1
- Update to 1.2.0

* Tue Apr 3 2012 - Devrim GUNDUZ <devrim@gunduz.org> 1.1.0-2
- Spec file fixes by Satoshi Nagayasu
- Updated patch0 and renamed it for better convenience.
- Replaced postgresql-devel dependency with postgresql, since
  pg_config is now in main package.

* Wed Oct 19 2011 - Devrim GUNDUZ <devrim@gunduz.org> 1.1.0-1
- Initial packaging.
