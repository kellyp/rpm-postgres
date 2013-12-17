%global pgmajorversion 93
%global pginstdir /usr/pgsql-9.3
%global sname prefix

Summary:	Prefix Opclass for PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	1.2.0
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/dimitri/%{sname}/archive/v%{version}.zip
Patch0:		prefix-makefile-pgconfig.patch
URL:		http://pgfoundry.org/projects/prefix
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The prefix project implements text prefix matches operator (prefix @> 
text) and provide a GiST opclass for indexing support of prefix 
searches.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make %{?_smp_mflags} DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{_docdir}/pgsql/extension/README.md 
%doc %{_docdir}/pgsql/extension/TESTS.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*

%changelog
* Mon Jan 7 2013 - Devrim GUNDUZ <devrim@gunduz.org> 1.2.0-1
- Update to 1.2.0
- Fix for PostgreSQL 9.0+ RPM layout.

* Fri Dec 11 2009 - Devrim GUNDUZ <devrim@gunduz.org> 1.1.0-1
- Update to 1.1.0

* Fri May 30 2008 - Devrim GUNDUZ <devrim@gunduz.org> 0.2-1
- Initial RPM packaging for yum.pgsqlrpms.org 
