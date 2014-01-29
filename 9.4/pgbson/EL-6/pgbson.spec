%global pgmajorversion 93
%global pginstdir /usr/pgsql-9.4devel
%global sname pgbson

Summary:	BSON support for PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	1.0.1
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
Patch0:		%{sname}-pgconfig.patch
URL:		http://pgxn.org/dist/pgbson
BuildRequires:	postgresql%{pgmajorversion}-devel, cmake28, boost-devel
Requires:	postgresql%{pgmajorversion}-server, python-psycopg2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
pgbson is a PostgreSQL extension to manage partitioned tables by time or ID.
This PostgreSQL extension brings BSON data type, together with functions to 
create, inspect and manipulate BSON objects.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
# Create build directory:
%{__rm} -rf ../%{sname}-%{version}-build
mkdir ../%{sname}-%{version}-build
cd ../%{sname}-%{version}-build
# Start building
cmake28 ../%{sname}-%{version}
%{__make}

%install
rm -rf %{buildroot}
cd ../%{sname}-%{version}-build
%{__make} install DESTDIR=%{buildroot}

# Install README file under PostgreSQL installation directory:
install -d %{buildroot}%{pginstdir}/share/extension
install -m 755 ../%{sname}-%{version}/README.md  %{buildroot}%{pginstdir}/share/extension/README-%{sname}.md
rm -f %{buildroot}%{_docdir}/pgsql/extension/pgbson.md

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/share/extension/README-%{sname}.md
%{pginstdir}/lib/libpgbson.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Tue Dec 17 2013 - Devrim GUNDUZ <devrim@gunduz.org> 1.0.1-1
- Update to 1.0.1
- Depend on cmake28 on RHEL 6, which comes from EPEL repo.

* Thu Oct 31 2013 - Devrim GUNDUZ <devrim@gunduz.org> 1.0.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
