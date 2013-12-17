Summary:	Web-based PostgreSQL administration
Name:		phpPgAdmin
Version:	5.1
Release:	2%{?dist}
License:	GPLv2+ and (LGPLv2+ or BSD) and ASL 2.0 and MIT
Group:		Applications/Databases
URL:		http://phppgadmin.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	http://downloads.sourceforge.net/phppgadmin/%{name}-%{version}.tar.bz2
Source1:	%{name}.conf

Requires:	php >= 4.2, gawk
Requires:	php-pgsql >= 4.2, httpd
Requires(post): systemd
Requires(postun): systemd
Buildarch:	noarch

%define		_phppgadmindir	%{_datadir}/%{name}

Patch1:		%{name}-langcheck.patch

%description
phpPgAdmin is a fully functional web-based administration utility for
a PostgreSQL database server. It handles all the basic functionality
as well as some advanced features such as triggers, views and
functions (stored procedures). It also has Slony-I support.

%prep
%setup -q -n %{name}-%{version}
%patch1 -p0

%build

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_phppgadmindir}
install -d %{buildroot}%{_phppgadmindir}/conf
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}%{_sysconfdir}/httpd/conf.d/
install -m 644 -p *.php %{buildroot}%{_phppgadmindir}
cp -ap *.js robots.txt classes help images js lang libraries plugins themes xloadtree %{buildroot}%{_phppgadmindir}
install -m 755 -p %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf
install -m 755 conf/* %{buildroot}%{_sysconfdir}/%{name}
ln -s %{_sysconfdir}/%{name}/config.inc.php %{buildroot}/%{_phppgadmindir}/conf/config.inc.php
ln -s %{_sysconfdir}/%{name}/config.inc.php-dist %{buildroot}/%{_phppgadmindir}/conf/config.inc.php-dist

%post
/usr/bin/systemctl reload httpd.service

%postun
/usr/bin/systemctl reload httpd.service

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc CREDITS DEVELOPERS FAQ HISTORY INSTALL LICENSE TODO TRANSLATORS
%dir %{_phppgadmindir}
%dir %{_sysconfdir}/%{name}
%dir %{_phppgadmindir}/conf
%config(noreplace) %{_sysconfdir}/%{name}/*
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%attr(644,root,root) %{_phppgadmindir}/*.php
%{_phppgadmindir}/*.js
%{_phppgadmindir}/robots.txt
%{_phppgadmindir}/classes
%{_phppgadmindir}/help
%{_phppgadmindir}/images
%{_phppgadmindir}/js/*.js
%{_phppgadmindir}/libraries
%{_phppgadmindir}/plugins/Report/*
%{_phppgadmindir}/plugins/GuiControl/*
%{_phppgadmindir}/themes
%{_phppgadmindir}/xloadtree
%{_phppgadmindir}/conf/*
%dir %{_phppgadmindir}/lang
%attr(644,root,root) %{_phppgadmindir}/lang/*.php
%attr(644,root,root) %{_phppgadmindir}/lang/README
%attr(755,root,root) %{_phppgadmindir}/lang/langcheck
%attr(755,root,root) %{_phppgadmindir}/lang/synch

%changelog
* Wed Oct 23 2013 Devrim Gündüz <devrim@gunduz.org> 5.1-2
- Apply fixes from Fedora, per Josef Mlich:
 * post, preun, postun phases modified accoding to Fedora Packaging Guidelines
 * Update apache configuration file for httpd 2.4
 * incorrect disabling of httpd during uninstallation

* Wed Apr 17 2013 Devrim Gunduz <devrim@gunduz.org> 5.1-1
- Update to 5.1, per changes described at
  http://sourceforge.net/mailarchive/message.php?msg_id=30730170

"* Sun Mar 25 2012 Devrim Gunduz <devrim@gunduz.org> 5.0.4-1
- Update to 5.0.4, per changes described at
  http://archives.postgresql.org/pgsql-announce/2012-03/msg00016.php

* Mon Oct 3 2011 Devrim Gunduz <devrim@gunduz.org> 5.0.3-1
- Update to 5.0.3, per changes described at:
   http://sourceforge.net/mailarchive/forum.php?thread_name=4E897F6C.90905%40free.fr&forum_name=phppgadmin-news
- Update license

* Sun Jan 9 2011 Devrim Gunduz <devrim@gunduz.org> 5.0.2-1
- Update to 5.0.2

* Tue Dec 14 2010 Devrim Gunduz <devrim@gunduz.org> 5.0.1-1
- Update to 5.0.1

* Tue Nov 30 2010 Devrim Gunduz <devrim@gunduz.org> 5.0-1
- Update to 5.0
* Thu Oct 7 2010 Devrim Gunduz <devrim@gunduz.org> 5.0-beta2-1
- Update to 5.0-beta2
- Trim changelog

