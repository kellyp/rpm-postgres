%global pgmajorversion 93
%global pginstdir /usr/pgsql-9.4devel
%global sname plsh

Summary:	Sh shell procedural language handler for PostgreSQL
Name:           %{sname}%{pgmajorversion}
Version:	1.20121018
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/downloads/petere/%{sname}/%{sname}-%{version}.tar.gz
Patch1:		%{sname}-makefile.patch
URL:		https://github.com/petere/plsh
BuildRequires:	postgresql%{pgmajorversion}-devel 
Requires:	postgresql%{pgmajorversion}-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
PL/sh is a procedural language handler for PostgreSQL that 
allows you to write stored procedures in a shell of your choice.

%prep
%setup -q -n %{sname}-%{version}
%patch1 -p0

%build
make %{?_smp_mflags} DESTDIR=%{buildroot}

%install
rm -rf %{buildroot}

make %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig 
%postun -p /sbin/ldconfig 

%files
%defattr(644,root,root,755)

%{pginstdir}/lib/%{sname}.so
%doc NEWS COPYING README.md 
%{pginstdir}/share/extension/%{sname}--1.sql
%{pginstdir}/share/extension/%{sname}--unpackaged--1.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Tue Nov 27 2012 - Devrim GUNDUZ <devrim@gunduz.org> 1.20121018-1
- Rewrite the spec file based on the new version, and update
  to 1.20121018

* Sun Jan 20 2008 - Devrim GUNDUZ <devrim@gunduz.org> 1.3-2
- Move .so file to the correct directory

* Tue Jan 15 2008 - Devrim GUNDUZ <devrim@gunduz.org> 1.3-1
- Initial RPM packaging for Fedora
