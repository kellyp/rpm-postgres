Summary:	Web-based PostgreSQL administration
Name:		phpPgAdmin
Version:	5.0.3
Release:	1%{?dist}
License:	GPLv3+
Group:		Applications/Databases
URL:		http://phppgadmin.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	http://downloads.sourceforge.net/phppgadmin/%{name}-%{version}.tar.bz2

Source1:	%{name}.conf

Requires:	php >= 4.2, gawk
Requires:	php-pgsql >= 4.2, httpd
Requires(post):	/sbin/service
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
# Cleanup encoding problem
sed -i 's/\r//' lang/php2po
sed -i 's/\r//' lang/po2php

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_phppgadmindir}
install -d %{buildroot}%{_phppgadmindir}/conf
install -d %{buildroot}%{_sysconfdir}/%{name}
install -m 644 -p *.php %{buildroot}%{_phppgadmindir}
cp -ap *.js robots.txt classes images lang libraries sql themes xloadtree help %{buildroot}%{_phppgadmindir}
install -d  %{buildroot}%{_sysconfdir}/httpd/conf.d/
install -d %{buildroot}%{_sysconfdir}/httpd/conf.d/
install -m 755 -p %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf
install -m 755 conf/* %{buildroot}%{_sysconfdir}/%{name}
ln -s %{_sysconfdir}/%{name}/config.inc.php %{buildroot}/%{_phppgadmindir}/conf/config.inc.php
ln -s %{_sysconfdir}/%{name}/config.inc.php-dist %{buildroot}/%{_phppgadmindir}/conf/config.inc.php-dist

%post
	/sbin/service httpd reload > /dev/null 2>&1

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
%{_phppgadmindir}/images
%dir %{_phppgadmindir}/lang
%dir %attr(755,root,root) %{_phppgadmindir}/lang/recoded
%attr(644,root,root) %{_phppgadmindir}/lang/*.php
%attr(644,root,root) %{_phppgadmindir}/lang/recoded/*
%attr(644,root,root) %{_phppgadmindir}/lang/Makefile
%attr(755,root,root) %{_phppgadmindir}/lang/convert.awk
%attr(755,root,root) %{_phppgadmindir}/lang/langcheck
%attr(755,root,root) %{_phppgadmindir}/lang/php2po
%attr(755,root,root) %{_phppgadmindir}/lang/po2php
%attr(755,root,root) %{_phppgadmindir}/lang/synch
%{_phppgadmindir}/libraries
%{_phppgadmindir}/sql
%{_phppgadmindir}/themes
%{_phppgadmindir}/xloadtree
%{_phppgadmindir}/help
%{_phppgadmindir}/conf/config.inc.php*

%changelog
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
