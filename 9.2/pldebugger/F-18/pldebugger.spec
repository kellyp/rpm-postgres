Summary:	PL/pgSQL debugger for PostgreSQL
Name:		pldebugger
Version:	0.93
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	edb-debugger-%{version}.tgz
Patch0:		pldebugger-pgxs.patch
URL:		http://pgfoundry.org/projects/edb-debugger/
BuildRequires:	postgresql-devel >= 8.3
Requires:	postgresql-server >= 8.3
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The PL/pgSQL debugger lets you step through PL/pgSQL code, set and clear breakpoints, 
view and modify variables, and walk through the call stack. 

%prep
%setup -q -n %{name}
%patch0 -p1

%build
make USE_PGXS=1 %{?_smp_mflags} 

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/pgsql/
install -d %{buildroot}%{_datadir}/%{name}
install -d %{buildroot}%{_docdir}/%{name}-%{version}
install -m 755 *.so %{buildroot}%{_libdir}/pgsql
install -p -m 755 pldbgapi.sql %{buildroot}%{_datadir}/%{name}
install -p -m 755 README.%{name} %{buildroot}%{_docdir}/%{name}-%{version}/README

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{_docdir}/%{name}-%{version}/README
%{_datadir}/%{name}
%{_datadir}/%{name}/pldbgapi.sql
%{_libdir}/pgsql/*.so

%changelog
* Fri Mar 12 2010 - Devrim GUNDUZ <devrim@gunduz.org> 0.93-1
- Initial RPM packaging for Fedora
