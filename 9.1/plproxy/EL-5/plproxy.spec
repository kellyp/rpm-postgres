%global pgmajorversion 91
%global pginstdir /usr/pgsql-9.1
%global sname plproxy

Summary:	PL/Proxy is database partitioning system implemented as PL language.
Name:           %{sname}%{pgmajorversion}
Version:	2.4
Release:	1%{?dist}
Group:		Applications/Databases
License:	BSD
URL:		http://pgfoundry.org/projects/plproxy/
Source0:	http://ftp.postgresql.org/pub/projects/pgFoundry/%{sname}/%{sname}-%{version}.tar.gz
Patch0:		Makefile-pgxs.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	postgresql%{pgmajorversion}-devel flex >= 2.5.4
Requires:	postgresql%{pgmajorversion}

%description
PL/Proxy is database partitioning system implemented as PL language.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p1

%build
USE_PGXS=1 make %{?_smp_mflags}

%install
rm -rf %{buildroot}
USE_PGXS=1 make %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README NEWS AUTHORS COPYRIGHT 
%{pginstdir}/lib/plproxy.so
%{pginstdir}/share/extension/plproxy--2.4.0.sql
%{pginstdir}/share/extension/plproxy--unpackaged--2.3.0.sql
%{pginstdir}/share/extension/plproxy.control

%changelog
* Fri Jul 27 2012 - Devrim GUNDUZ <devrim@gunduz.org> 2.4-1
- Update to 2.4
- Update download URL.
- Trim changelog

