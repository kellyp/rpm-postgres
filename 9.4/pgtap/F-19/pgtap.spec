%global pgmajorversion 93
%global pginstdir /usr/pgsql-9.4devel
%global sname	pgtap

Summary:	Unit testing suite for PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	0.25.0
Release:	1%{?dist}
Group:		Applications/Databases
License:	BSD
URL:		http://pgtap.projects.postgresql.org
Source0:	ftp://ftp.postgresql.org/pub/projects/pgFoundry/pgtap/pgtap-%{version}.tar.bz2
Patch0:		Makefile-pgxs.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server, perl-Test-Harness >= 3.0

Requires(post):	%{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives

BuildArch:	noarch
 
%description
pgTAP is a unit testing framework for PostgreSQL written in PL/pgSQL and
PL/SQL. It includes a comprehensive collection of TAP-emitting assertion
functions, as well as the ability to integrate with other TAP-emitting
test frameworks. It can also be used in the xUnit testing style.
 
%prep
%setup -q -n %{sname}-%{version}
%patch0 -p1

%build
make USE_PGXS=1 TAPSCHEMA=pgtap %{?_smp_mflags}

%install
%{__rm} -rf  %{buildroot}
make install USE_PGXS=1 DESTDIR=%{buildroot} %{?_smp_mflags}
mv %{buildroot}/usr/share/doc/pgsql/contrib/README.pgtap %{buildroot}%{pginstdir}/share/contrib

%clean
%{__rm} -rf  %{buildroot}

%post
# Create alternatives entries for binaries
%{_sbindir}/update-alternatives --install /usr/bin/pg_prove pgtap-prove %{pginstdir}/bin/pg_prove 910
%{_sbindir}/update-alternatives --install /usr/bin/pg_tapgen pgtap-tapgen %{pginstdir}/bin/pg_tapgen 910

%preun
# Drop alternatives entries for common binaries and man files
%{_sbindir}/update-alternatives --remove pgtap-prove %{pginstdir}/bin/pg_prove
%{_sbindir}/update-alternatives --remove pgtap-tapgen %{pginstdir}/bin/pg_tapgen

%files
%defattr(-,root,root,-)
%{pginstdir}/bin/pg_prove
%{pginstdir}/bin/pg_tapgen
%{pginstdir}/share/contrib/*.sql
%{pginstdir}/share/contrib/README.pgtap

%changelog
* Fri Apr 1 2011 Devrim GÜNDÜZ <devrim@gunduz.org> 0.25.0-1
- Update to 0.25.0
 
* Fri Oct 8 2010 Devrim GÜNDÜZ <devrim@gunduz.org> 0.24-3
- Use alternatives method for binaries.
- Use %%{?_smp_mflags} macro for make.

* Thu Oct 7 2010 Devrim GÜNDÜZ <devrim@gunduz.org> 0.24-2
- Update spec for 9.0 layout.
- TODO: Use alternatives.
 
* Tue Jun 15 2010 Devrim GÜNDÜZ <devrim@gunduz.org> 0.24-1
- Update to 0.24
 
* Mon Dec 28 2009 Devrim GÜNDÜZ <devrim@gunduz.org> 0.23-1
- Update to 0.23
 
* Wed Aug 19 2009 Darrell Fuhriman <darrell@projectdx.com> 0.22-1
- initial RPM
 
