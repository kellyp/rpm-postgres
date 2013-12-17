%global pgmajorversion 93
%global pginstdir /usr/pgsql-9.3
%global sname pg_jobmon

Summary:	Job logging and monitoring extension for PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	1.1.3
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
Patch0:		Makefile-pgxs.patch
URL:		http://pgfoundry.org/projects/pgfincore
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

%description
pg_jobmon is a job logging and monitoring extension for PostgreSQL.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
make USE_PGXS=1 %{?_smp_mflags}

%install
rm -rf %{buildroot}

make USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README file under PostgreSQL installation directory:
install -d %{buildroot}%{pginstdir}/share/extension
install -m 755 README.md  %{buildroot}%{pginstdir}/share/extension/README-%{sname}.md
install -m 755 doc/pg_jobmon.md  %{buildroot}%{pginstdir}/share/extension/
rm -f %{buildroot}%{_docdir}/pgsql/extension/pg_jobmon.md

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/share/extension/README-%{sname}.md 
%doc %{pginstdir}/share/extension/%{sname}.md
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Thu Oct 31 2013 - Devrim GUNDUZ <devrim@gunduz.org> 1.1.3-1
- Initial RPM packaging for PostgreSQL RPM Repository
