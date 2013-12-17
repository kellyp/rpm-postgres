%global pgmajorversion 92
%global pginstdir /usr/pgsql-9.2
%global sname pg_filedump

Summary:	PostgreSQL File Dump Utility
Name:		%{sname}%{pgmajorversion}
Version:	9.2.0
Release:	1%{?dist}
URL:		http://pgfoundry.org/projects/pgfiledump
License:	GPLv2+
Group:		Applications/Databases
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	postgresql%{pgmajorversion}-devel

Source0:	http://pgfoundry.org/frs/download.php/3391/pg_filedump-%{version}.tar.gz
Patch1:		pg_filedump-make.patch

Obsoletes:	rhdb-utils => 8.2.0

%description
Display formatted contents of a PostgreSQL heap/index/control file.

%prep
%setup -q -n %{sname}-%{version}

%patch1 -p0

%build
export CFLAGS="$RPM_OPT_FLAGS"

USE_PGXS=1 make %{?_smp_mflags}

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
install -m 755 pg_filedump %{buildroot}%{_bindir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/pg_filedump
%doc  README.pg_filedump

%changelog
* Wed Nov 14 2012 Devrim GUNDUZ <devrim@gunduz.org> 9.2.0-1
- Update to 9.2.0

* Mon Jan 3 2011 Devrim GUNDUZ <devrim@gunduz.org> 9.0-1
- Update to 9.0

* Tue Mar 11 2008 Devrim GUNDUZ <devrim@gunduz.org> 8.3-1
- Initial packaging for PGDG Repository, using the Fedora
  spec of Tom, with minor stylistic cleanup. Also, conflict
  with rhdb-utils.

