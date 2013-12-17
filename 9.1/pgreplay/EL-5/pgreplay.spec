%global pgmajorversion 91
%global pginstdir /usr/pgsql-9.1
%global sname pgreplay

Summary:	PostgreSQL log file re-player
Name:		%{sname}
Version:	1.2.0
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://pgfoundry.org/frs/download.php/3345/%{sname}-%{version}.tar.gz
URL:		http://pgfoundry.org/projects/pgreplay
Requires:	postgresql%{pgmajorversion}
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
pgreplay reads a PostgreSQL log file (not a WAL file), extracts the SQL 
statements and executes them in the same order and relative time against 
a PostgreSQL database cluster.

If the execution of statements gets behind schedule, warning messages 
are issued that indicate that the server cannot handle the load in a 
timely fashion. The idea is to replay a real-world database workload as 
exactly as possible.

pgreplay is useful for performance tests, particularly in the following 
situations:

* You want to compare the performance of your PostgreSQL application 
on different hardware or different operating systems.
* You want to upgrade your database and want to make sure that the new 
database version does not suffer from performance regressions that 
affect you.

%prep
%setup -q -n %{sname}-%{version}
%configure --with-postgres=%{pginstdir}/bin

%build
make %{?_smp_mflags} 

%install
rm -rf %{buildroot}

make %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc pgreplay.html README CHANGELOG
%{_bindir}/%{sname}
%{_mandir}/man1/%{sname}*

%changelog
* Mon Sep 10 2012 - Devrim GUNDUZ <devrim@gunduz.org> 1.2.0-1
- Initial RPM packaging for Fedora

