%global pgmajorversion 93
%global pginstdir /usr/pgsql-9.3
%global sname pgfincore

Summary:	PgFincore is a set of functions to manage blocks in memory
Name:		%{sname}%{pgmajorversion}
Version:	1.1.1
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://pgfoundry.org/frs/download.php/3186/%{sname}-v%{version}.tar.gz
Patch0:		Makefile-pgxs.patch
URL:		http://pgfoundry.org/projects/pgfincore
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
PgFincore is a set of functions to manage blocks in memory.

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
install -m 755 README.rst %{buildroot}%{pginstdir}/share/extension/
rm -f %{buildroot}%{_docdir}/pgsql/extension/README.rst

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig 
%postun -p /sbin/ldconfig 

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYRIGHT TODO ChangeLog README.rst
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/README.rst

%changelog
* Mon Dec 19 2011 - Devrim GUNDUZ <devrim@gunduz.org> 1.1.1-1
- Update to 1.1.1, per changes described in
  http://pgfoundry.org/forum/forum.php?forum_id=1859

* Fri Aug 12 2011 - Devrim GUNDUZ <devrim@gunduz.org> 1.0-1
- Update to 1.0, (#68), per changes described in
  http://pgfoundry.org/frs/shownotes.php?release_id=1872

* Wed Nov 10 2010 - Devrim GUNDUZ <devrim@gunduz.org> 0.4.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
