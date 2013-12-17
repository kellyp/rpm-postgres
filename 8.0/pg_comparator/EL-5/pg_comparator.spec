Summary:	Efficient table content comparison and synchronization for PostgreSQL and MySQL
Name:		pg_comparator
Version:	1.6.1
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://pgfoundry.org/frs/download.php/2655/%{name}-%{version}.tgz
URL:		http://pgfoundry.org/projects/pg-comparator
BuildRequires:	postgresql-devel >= 8.0
Requires:	postgresql-server >= 8.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	perl(Getopt::Long) perl(Time::HiRes)
%description
pg_comparator is a tool to compare possibly very big tables in 
different locations and report differences, with a network and 
time-efficient approach.

%prep
%setup -q -n %{name}-%{version}

%build
make USE_PGXS=1 %{?_smp_mflags} 

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}/
install -d %{buildroot}%{_libdir}/
install -d %{buildroot}%{_docdir}/%{name}-%{version}
install -d %{buildroot}%{_datadir}/%{name}
install -m 755 pg_comparator %{buildroot}%{_bindir}
install -m 644 casts.so checksum.so %{buildroot}%{_libdir}
install -m 644 README.* INSTALL LICENSE %{buildroot}%{_docdir}/%{name}-%{version}
install -m 644 *.sql %{buildroot}%{_datadir}/%{name}

strip %{buildroot}/%{_libdir}/*.so

%clean
rm -rf %{buildroot}

#%post -p /sbin/ldconfig 
#%postun -p /sbin/ldconfig 

%files
%defattr(-,root,root,-)
%doc INSTALL LICENSE README.*
%{_bindir}/pg_comparator
%{_libdir}/casts.so
%{_libdir}/checksum.so
%{_datadir}/%{name}/*.sql

%changelog
* Tue Apr 20 2010 - Devrim GUNDUZ <devrim@gunduz.org> 1.6.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
