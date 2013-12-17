Summary:	PgFouine PostgreSQL log analyzer
Name:		pgfouine
Version:	1.2
Release:	1%{?dist}
BuildArch:	noarch
License:	GPLv2+
Group:		Development/Tools
Source0:	http://pgfoundry.org/frs/download.php/2575/%{name}-%{version}.tar.gz
Source2:	pgfouine-tutorial.txt
URL: 		http://pgfouine.projects.postgresql.org
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch1:		pgfouine-0.7-include_path.patch

%description
pgFouine is a PostgreSQL log analyzer. It generates text 
or HTML reports from PostgreSQL log files. These reports 
contain the list of the slowest queries, the queries that 
take the most time and so on.

pgFouine can also:
- analyze VACUUM VERBOSE output to help you improve your 
VACUUM strategy,
- generate Tsung sessions file to benchmark your 
PostgreSQL server.

%prep
%setup -q 
%patch1 -p0
sed -i 's!@INCLUDEPATH@!%{_datadir}/%{name}!' pgfouine_vacuum.php
sed -i 's!@INCLUDEPATH@!%{_datadir}/%{name}!' pgfouine.php

cp %{SOURCE2} .

%build

%install
# cleaning build environment
rm -rf %{buildroot}

# creating required directories
install -m 755 -d %{buildroot}/%{_datadir}/%{name}
install -m 755 -d %{buildroot}/%{_bindir}

# installing pgFouine
for i in include version.php; do
	cp -rp $i %{buildroot}/%{_datadir}/%{name}/
done

install -m 755 pgfouine.php %{buildroot}/%{_bindir}/
install -m 755 pgfouine_vacuum.php %{buildroot}/%{_bindir}/

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc AUTHORS ChangeLog COPYING THANKS README pgfouine-tutorial.txt
%attr(0755, root, root) %{_bindir}/pgfouine.php
%attr(0755, root, root) %{_bindir}/pgfouine_vacuum.php
%{_datadir}/%{name}

%changelog 
* Wed Mar 3 2010 Devrim Gunduz <devrim@gunduz.org> - 1.2-1
- Update to 1.2
- Update license
- Trim changelog
