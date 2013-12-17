%global pgmajorversion 90
%global pginstdir /usr/pgsql-9.0
%global sname	pgagent

Summary:	Job scheduler for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	3.0.1
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

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc README LICENSE
%{_bindir}/pgagent
%{_datadir}/%{name}-%{version}/%{sname}*.sql
%{_initrddir}/%{name}

%changelog
* Tue Dec 6 2011 Devrim GUNDUZ <devrim@gunduz.org> 3.0.1-1
- Initial packaging

