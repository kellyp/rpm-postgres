%global pgmajorversion 93
%global pginstdir /usr/pgsql-9.4devel
%global sname pagila

Summary:	A sample database for PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	0.10.1
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
URL:		http://pgfoundry.org/projects/dbsamples
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	http://pgfoundry.org/frs/download.php/1719/%{sname}-%{version}.zip

Requires:	postgresql%{pgmajorversion}
Buildarch:	noarch

%define		_pagiladir  %{_datadir}/%{name}

%description
Pagila is a port of the Sakila example database available for MySQL, which was
originally developed by Mike Hillyer of the MySQL AB documentation team. It
is intended to provide a standard schema that can be used for examples in
books, tutorials, articles, samples, etc.

%prep
%setup -q -n %{sname}-%{version}

%build

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_pagiladir}
install -m 644 -p *.sql %{buildroot}%{_pagiladir}

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc README
%dir %{_pagiladir}
%attr(644,root,root) %{_pagiladir}/*.sql

%changelog
* Mon Sep 27 2010 Devrim Gunduz <devrim@gunduz.org> 0.10.1-2
- Apply some minor fixes for new PostgreSQL RPM layout.

* Sat Jun 14 2008 Devrim Gunduz <devrim@gunduz.org> 0.10.1-1
- Update to 0.10.1

* Fri Feb 1 2008 Devrim Gunduz <devrim@gunduz.org> 0.10.0-1
- Initial packaging for Fedora/EPEL
