Summary:	PgFincore is a set of functions to manage blocks in memory
Name:		pgfincore
Version:	0.4.1
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://pgfoundry.org/frs/download.php/2670/%{name}-v%{version}.tar.gz
URL:		http://pgfoundry.org/projects/pgfincore
BuildRequires:	postgresql-devel >= 8.3
Requires:	postgresql-server >= 8.3
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
PgFincore is a set of functions to manage blocks in memory.

%prep
%setup -q -n %{name}

%build
make USE_PGXS=1 %{?_smp_mflags}

%install
rm -rf %{buildroot}

make USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig 
%postun -p /sbin/ldconfig 

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYRIGHT TODO ChangeLog
%doc %{_docdir}/pgsql/contrib/README.%{name}
%{_datadir}/pgsql/contrib/*%{name}*.sql
%{_libdir}/pgsql/%{name}.so

%changelog
* Wed Nov 10 2010 - Devrim GUNDUZ <devrim@gunduz.org> 0.4.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
