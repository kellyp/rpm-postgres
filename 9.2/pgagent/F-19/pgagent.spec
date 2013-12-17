%global pgmajorversion 92
%global pginstdir /usr/pgsql-9.2
%global sname	pgagent

Summary:	Job scheduler for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	3.3.0
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source:		http://ftp.postgresql.org/pub/pgadmin3/release/pgagent/pgAgent-%{version}-Source.tar.gz
Source2:	pgagent.init
URL:		http://www.pgadmin.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	wxGTK-devel postgresql%{pgmajorversion}-devel cmake

%description
pgAgent is a job scheduler for PostgreSQL which may be managed
using pgAdmin. Prior to pgAdmin v1.9, pgAgent shipped as part 
of pgAdmin. From pgAdmin v1.9 onwards, pgAgent is shipped as 
a separate application.

%pre
groupadd -o -r pgagent >/dev/null 2>&1 || :
useradd -o -g pgagent -r -s /bin/false \
	-c "pgAgent Job Schedule" pgagent >/dev/null 2>&1 || :
touch /var/log/pgagent_92.log
chown pgagent:pgagent /var/log/pgagent_92.log
chmod 0700 /var/log/pgagent_92.log

%prep
%setup -q -n pgAgent-%{version}-Source

%build
cmake -D CMAKE_INSTALL_PREFIX:PATH=/usr -D PG_CONFIG_PATH:FILEPATH=/%{pginstdir}/bin/pg_config -D STATIC_BUILD:BOOL=OFF .

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

# Remove some cruft, and also install doc related files to appropriate directory:
%{__mkdir} -p %{buildroot}%{_datadir}/%{name}-%{version}
%{__rm} -f %{buildroot}/usr/LICENSE
%{__rm} -f %{buildroot}/usr/README
%{__mv} -f %{buildroot}%{_datadir}/pgagent*.sql %{buildroot}%{_datadir}/%{name}-%{version}/

# install init script
install -d %{buildroot}/etc/rc.d/init.d
install -m 755 %{SOURCE2} %{buildroot}/etc/rc.d/init.d/%{name}

%post
chkconfig --add %{name}

%preun
chkconfig --add %{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc README LICENSE
%{_bindir}/pgagent
%{_datadir}/%{name}-%{version}/%{sname}*.sql
%{_initrddir}/%{name}

%changelog
* Mon Sep 17 2012 Devrim GUNDUZ <devrim@gunduz.org> 3.3.0-1
- Update to 3.3.0

* Wed Sep 12 2012 Devrim GUNDUZ <devrim@gunduz.org> 3.2.1-1
- Various updates from David Wheeler
- Update to 3.2.1
- Improve init script

* Tue Dec 6 2011 Devrim GUNDUZ <devrim@gunduz.org> 3.0.1-1
- Initial packaging

