%define debug 0

Name:		pgbouncer
Version:	1.5.4
Release:	2%{?dist}
Summary:	Lightweight connection pooler for PostgreSQL
Group:		Applications/Databases
License:	MIT and BSD
URL:		http://pgfoundry.org/projects/pgbouncer/
Source0:	http://ftp.postgresql.org/pub/projects/pgFoundry/%{name}/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-ini.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	libevent-devel >= 2.0
Requires:	initscripts

Requires(post):	chkconfig
Requires(preun):	chkconfig, initscripts
Requires(postun):	initscripts
Requires:	/usr/sbin/useradd

%description
pgbouncer is a lightweight connection pooler for PostgreSQL.
pgbouncer uses libevent for low-level socket handling.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p0

%build
sed -i.fedora \
 -e 's|-fomit-frame-pointer||' \
 -e '/BININSTALL/s|-s||' \
 configure

%configure \
%if %debug
	--enable-debug \
	--enable-cassert \
%endif
--datadir=%{_datadir} 

make %{?_smp_mflags} V=1

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
install -p -d %{buildroot}%{_sysconfdir}/%{name}/
install -p -d %{buildroot}%{_sysconfdir}/sysconfig
install -p -m 644 etc/pgbouncer.ini %{buildroot}%{_sysconfdir}/%{name}
install -p -m 700 etc/mkauth.py %{buildroot}%{_sysconfdir}/%{name}/
install -p -d %{buildroot}%{_initrddir}
install -p -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
install -p -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

# Remove duplicated files
%{__rm} -f %{buildroot}%{_docdir}/%{name}/pgbouncer.ini
%{__rm} -f %{buildroot}%{_docdir}/%{name}/NEWS
%{__rm} -f %{buildroot}%{_docdir}/%{name}/README
%{__rm} -f %{buildroot}%{_docdir}/%{name}/userlist.txt

%post
chkconfig --add pgbouncer

%pre
groupadd -r pgbouncer >/dev/null 2>&1 || :
useradd -m -g pgbouncer -r -s /bin/bash \
        -c "PgBouncer Server" pgbouncer >/dev/null 2>&1 || :
touch /var/log/pgbouncer.log
chown pgbouncer:pgbouncer /var/log/pgbouncer.log
chmod 0700 /var/log/pgbouncer.log

%preun
if [ $1 = 0 ] ; then
	/sbin/service pgbouncer condstop >/dev/null 2>&1
	chkconfig --del pgbouncer
fi

%postun
if [ "$1" -ge "1" ] ; then
	/sbin/service pgbouncer condrestart >/dev/null 2>&1 || :
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README NEWS AUTHORS
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.ini
%{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_mandir}/man1/%{name}.*
%{_mandir}/man5/%{name}.*
%{_sysconfdir}/%{name}/mkauth.py*

%changelog
* Mon Sep 16 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.5.4-2
- Update init script, per #138, which fixes the following.
  Contributed by Peter:
 - various legacy code of unknown purpose
 - no LSB header
 - used the script name as NAME, making it impossible to copy
   the script and run two pgbouncers
 - didn't use provided functions like daemon and killproc
 - incorrect exit codes when starting already started service and
   stopping already stopped service (nonstandard condstop action
   was a partial workaround?)
 - restart didn't make use of pgbouncer -R option

* Mon Dec 10 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.5.4-1
- Update to 1.5.4

* Wed Sep 12 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.5.3-1
- Update to 1.5.3, per changes described at:
  http://pgfoundry.org/forum/forum.php?forum_id=1981

* Tue Jul 31 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.5.2-3
- Add mkauth.py among installed files.

* Thu Jun 21 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.5.2-2
- Fix useradd line.

* Tue Jun 5 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.5.2-1
- Update to 1.5.2, per changes described at:
  http://pgfoundry.org/forum/forum.php?forum_id=1885

* Tue May 15 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.5.1-1
- Update to 1.5.1

* Sun Apr 08 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.5-2
-  Fix shell of pgbouncer user, to avoid startup errors.

* Fri Apr 6 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.5-1
- Update to 1.5, for the changes described here:
  http://pgfoundry.org/frs/shownotes.php?release_id=1920
- Trim changelog

* Fri Aug 12 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.4.2-1
- Update to 1.4.2, for the changes described here:
  http://pgfoundry.org/frs/shownotes.php?release_id=1863

* Mon Sep 13 2010 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.3.4-1
- Update to 1.3.4, for the changes described here:
  http://pgfoundry.org/frs/shownotes.php?prelease_id=1698
* Fri Aug 06 2010 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.3.3-2
- Sleep 2 seconds before getting pid during start(), like we do in PostgreSQL
  init script, to avoid false positive startup errors.

* Tue May 11 2010 Devrim GUNDUZ <devrim@gunduz.org> - 1.3.3-1
- Update to 1.3.3, per pgrpms.org #25, for the fixes described at:
  http://pgfoundry.org/frs/shownotes.php?release_id=1645

* Tue Mar 16 2010 Devrim GUNDUZ <devrim@gunduz.org> - 1.3.2-1
- Fix some issues in init script. Fixes pgrpms.org #9.

