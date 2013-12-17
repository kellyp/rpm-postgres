%global pgmajorversion 93
%global pginstdir /usr/pgsql-9.3
%global sname pg_comparator

Summary:	Efficient table content comparison and synchronization for PostgreSQL and MySQL
Name:           %{sname}%{pgmajorversion}
Version:	2.2.1
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://ftp.postgresql.org/pub/projects/pgFoundry/pg-comparator/%{sname}/%{version}/%{sname}-%{version}.tgz
Patch0:		Makefile-pgxs.patch
URL:		http://pgfoundry.org/projects/pg-comparator
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	perl(Getopt::Long), perl(Time::HiRes), perl-Pod-Usage

%description
pg_comparator is a tool to compare possibly very big tables in 
different locations and report differences, with a network and 
time-efficient approach.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p1

%build
make USE_PGXS=1 %{?_smp_mflags} 

%install
rm -rf %{buildroot}
make USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}
install -d %{buildroot}%{pginstdir}/share/contrib/
mv %{buildroot}%{_docdir}/pgsql/contrib/README* %{buildroot}%{pginstdir}/share/contrib/
strip %{buildroot}/%{pginstdir}/lib/*.so

%post
# Create alternatives entries for binaries
%{_sbindir}/update-alternatives --install /usr/bin/pg_comparator pgcomparator %{pginstdir}/bin/pg_comparator 920

%preun
# Drop alternatives entries for common binaries and man files
%{_sbindir}/update-alternatives --remove pgcomparator %{pginstdir}/bin/pg_comparator

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{pginstdir}/bin/pg_comparator
%{pginstdir}/lib/*.so
%{pginstdir}/share/contrib/*.sql
%doc %{pginstdir}/share/contrib/README.*

%changelog
* Sun Jun 30 2013 - Devrim GUNDUZ <devrim@gunduz.org> 2.2.1-1
- Update to 2.2.1

* Wed Nov 14 2012 - Devrim GUNDUZ <devrim@gunduz.org> 2.1.2-1
- Update to 2.1.2

* Fri Sep 14 2012 - Devrim GUNDUZ <devrim@gunduz.org> 2.1.1-1
- Update to 2.1.1
- Use a better URL for tarball

* Fri Oct 8 2010 - Devrim GUNDUZ <devrim@gunduz.org> 1.6.2-1
- Refactor spec for 9.0 compatibility. 

* Tue Apr 20 2010 - Devrim GUNDUZ <devrim@gunduz.org> 1.6.1-1
- Initial RPM packaging for PostgreSQL RPM Repository

