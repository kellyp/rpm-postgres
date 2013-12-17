%global pgmajorversion 91
%global pginstdir /usr/pgsql-9.1
%global sname table_log

Summary:	Log data changes in a PostgreSQL table
Name:		%{sname}%{pgmajorversion}
Version:	0.4.4
Release:	3%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://pgfoundry.org/frs/download.php/1387/%{sname}-%{version}.tar.gz
Patch0:		Makefile-pgxs.patch
URL:		http://pgfoundry.org/projects/tablelog
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
table_log is a set of functions to log changes on a table in PostgreSQL
and to restore the state of the table or a specific row on any time
in the past.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p1

%build
make USE_PGXS=1 %{?_smp_mflags}

%install
rm -rf %{buildroot}

make USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README file under PostgreSQL installation directory:
install -d %{buildroot}%{pginstdir}/share/contrib/
install -m 755 README.%{sname} %{buildroot}%{pginstdir}/share/contrib/
rm -f %{buildroot}%{_docdir}/pgsql/contrib/README.%{sname}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig 
%postun -p /sbin/ldconfig 

%files
%defattr(644,root,root,755)
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/contrib/%{sname}.sql
%{pginstdir}/share/contrib/README.%{sname}

%changelog
* Fri Sep 10 2010 - Devrim GUNDUZ <devrim@gunduz.org> 0.4.4-3
- Add a patch for new RPM layout, so that the correct pg_config is 
  picked up.
- Really use PGXS build, and don't install files manually (except
  README)

* Sat Jun 17 2007 - Devrim GUNDUZ <devrim@gunduz.org> 0.4.4-2
- Added Requires, per bugzilla review #244536 (Thanks Ruben)
- Renamed README file, per bugzilla review #244536

* Sat Jun 16 2007 - Devrim GUNDUZ <devrim@gunduz.org> 0.4.4-1
- Initial RPM packaging for Fedora
