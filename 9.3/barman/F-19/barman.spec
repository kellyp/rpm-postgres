#Python major version.
%{expand: %%define pybasever %(python -c 'import sys;print(sys.version[0:3])')}
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary:	Backup and Recovery Manager for PostgreSQL
Name:		barman
Version:	1.2.3
Release:	1%{?dist}
License:	GPLv3
Group:		Applications/Databases
Url:		http://www.pgbarman.org/
Source0:	http://garr.dl.sourceforge.net/project/pgbarman/%{version}/%{name}-%{version}.tar.gz
Source1:	%{name}.cron
Source2:	%{name}.logrotate
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
BuildArch:	noarch
Requires:	python-abi = %{pybasever}, python-argh  => 0.21.2, python-psycopg2, 
Requires:	python-argcomplete, python-dateutil
Requires:	/usr/sbin/useradd

%description
Barman (backup and recovery manager) is an administration
tool for disaster recovery of PostgreSQL servers written in Python.
It allows to perform remote backups of multiple servers
in business critical environments and help DBAs during the recovery phase.
Barman's most wanted features include backup catalogs, retention policies,
remote recovery, archiving and compression of WAL files and backups.
Barman is written and maintained by PostgreSQL professionals 2ndQuadrant.

%prep
%setup -n barman-%{version} -q

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
mkdir -p %{buildroot}%{_sysconfdir}/cron.d/
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d/
mkdir -p %{buildroot}/var/lib/barman
mkdir -p %{buildroot}/var/log/barman
install -pm 644 doc/barman.conf %{buildroot}%{_sysconfdir}/barman.conf
install -pm 644 scripts/barman.bash_completion %{buildroot}%{_sysconfdir}/bash_completion.d/barman
install -pm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/cron.d/barman
install -pm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/barman
touch %{buildroot}/var/log/barman/barman.log

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc INSTALL NEWS README
%{python_sitelib}/%{name}-%{version}-py%{pybasever}.egg-info
%{python_sitelib}/%{name}/
%{_bindir}/%{name}
%doc %{_mandir}/man1/%{name}.1.gz
%doc %{_mandir}/man5/%{name}.5.gz
%config(noreplace) %{_sysconfdir}/bash_completion.d/
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/cron.d/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(700,barman,barman) %dir /var/lib/%{name}
%attr(755,barman,barman) %dir /var/log/%{name}
%attr(600,barman,barman) %ghost /var/log/%{name}/%{name}.log

%pre
groupadd -f -r barman >/dev/null 2>&1 || :
useradd -M -n -g barman -r -d /var/lib/barman -s /bin/bash \
	-c "Backup and Recovery Manager for PostgreSQL" barman >/dev/null 2>&1 || :

%changelog
* Tue Sep 10 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.2.3-1
- Update to 1.2.3, per changes described in this page:
   http://sourceforge.net/projects/pgbarman/files/1.2.3/

* Thu Jun 27 2013 Jeff Frost <jeff@pgexperts.com> - 1.2.2-1
- Update to 1.2.2, per changes described in this page:
   http://sourceforge.net/projects/pgbarman/files/1.2.2/

* Thu Jun 20 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.2.1-1
- Update to 1.2.1, per changes described in this page:
   http://sourceforge.net/projects/pgbarman/files/1.2.1/

* Tue Feb 26 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.2.0-2
- Add dependency for argcomplete, also add dependency for 
  specific version of python-argh.

* Fri Feb 1 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.2.0-1
- Update to 1.2.0, per changes described in this page:
   http://sourceforge.net/projects/pgbarman/files/1.2.0/

* Tue Dec 11 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.1.2-1
- Update to 1.1.2, per changes described in this page:
   http://sourceforge.net/projects/pgbarman/files/1.1.2/

* Sun Oct 28 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.1.1-1
- Update to 1.1.1, per changes described in this page:
   http://sourceforge.net/projects/pgbarman/files/1.1.1/

* Tue Aug 28 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.0.0-2
- Add missing Requires, per Ger Timmens.

* Fri Jul  27 2012 - Devrim Gunduz <devrim@gunduz.org> - 1.0.0-1
- Initial packaging, based on the spec by Marco Neciarini
