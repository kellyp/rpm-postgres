%global pginstdir /usr/pgsql-9.3
%global pgmajorversion 93
%global sname   skytools

# Python major version.
%{expand: %%define pyver %(python -c 'import sys;print(sys.version[0:3])')}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary:	PostgreSQL database management tools from Skype
Name:		%{sname}-%{pgmajorversion}
Version:	3.1.5
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://ftp.postgresql.org/pub/projects/pgFoundry/%{sname}/%{sname}/%{version}/%{sname}-%{version}.tar.gz
URL:		http://pgfoundry.org/projects/skytools
BuildRequires:	postgresql%{pgmajorversion}-devel, python-devel
Requires:	python-psycopg2, postgresql%{pgmajorversion}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Database management tools from Skype:WAL shipping, queueing, replication. 
The tools are named walmgr, PgQ and Londiste, respectively.

%package modules
Summary:	PostgreSQL modules of Skytools
Group:		Applications/Databases
Requires:	%{sname}-%{pgmajorversion} = %{version}-%{release}

%description modules
This package has PostgreSQL modules of skytools.

%prep
%setup -q -n %{sname}-%{version}

%build
%configure --with-pgconfig=%{pginstdir}/bin/pg_config

make %{?_smp_mflags} 

%install
rm -rf %{buildroot}

make %{?_smp_mflags} DESTDIR=%{buildroot} python-install modules-install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig 
%postun -p /sbin/ldconfig 

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/data_maintainer3
%attr(755,root,root) %{_bindir}/londiste3
%attr(755,root,root) %{_bindir}/pgqd
%attr(755,root,root) %{_bindir}/qadmin
%attr(755,root,root) %{_bindir}/queue_mover3
%attr(755,root,root) %{_bindir}/queue_splitter3
%attr(755,root,root) %{_bindir}/scriptmgr3
%attr(755,root,root) %{_bindir}/simple_consumer3
%attr(755,root,root) %{_bindir}/simple_local_consumer3
%attr(755,root,root) %{_bindir}/skytools_upgrade3
%attr(755,root,root) %{_bindir}/walmgr3
%dir %{_libdir}/python%{pyver}/site-packages/londiste
/usr/lib//python%{pyver}/site-packages/pkgloader.py*
%{_libdir}/python%{pyver}/site-packages/londiste/*.py*
%{_libdir}/python%{pyver}/site-packages/londiste/handlers/*.py*
%{_libdir}/python%{pyver}/site-packages/pgq/*.py*
%{_libdir}/python%{pyver}/site-packages/skytools/*.py*
%{_libdir}/python%{pyver}/site-packages/skytools/*.so
%{_libdir}/python%{pyver}/site-packages/pgq/cascade/*.py*
/usr/lib/python%{pyver}/site-packages/pkgloader-1.0-py%{pyver}.egg-info
%{_libdir}/python%{pyver}/site-packages/skytools-%{version}-py%{pyver}.egg-info
%{pginstdir}/share/contrib/londiste.sql
%{pginstdir}/share/contrib/londiste.upgrade.sql
%{pginstdir}/share/contrib/newgrants_londiste.sql
%{pginstdir}/share/contrib/newgrants_pgq.sql
%{pginstdir}/share/contrib/newgrants_pgq_coop.sql
%{pginstdir}/share/contrib/newgrants_pgq_ext.sql
%{pginstdir}/share/contrib/newgrants_pgq_node.sql
%{pginstdir}/share/contrib/oldgrants_londiste.sql
%{pginstdir}/share/contrib/oldgrants_pgq.sql
%{pginstdir}/share/contrib/oldgrants_pgq_coop.sql
%{pginstdir}/share/contrib/oldgrants_pgq_ext.sql
%{pginstdir}/share/contrib/oldgrants_pgq_node.sql
%{pginstdir}/share/contrib/pgq.sql
%{pginstdir}/share/contrib/pgq.upgrade.sql
%{pginstdir}/share/contrib/pgq_coop.sql
%{pginstdir}/share/contrib/pgq_coop.upgrade.sql
%{pginstdir}/share/contrib/pgq_ext.sql
%{pginstdir}/share/contrib/pgq_ext.upgrade.sql
%{pginstdir}/share/contrib/pgq_node.sql
%{pginstdir}/share/contrib/pgq_node.upgrade.sql
%{pginstdir}/share/contrib/txid.sql
%{pginstdir}/share/contrib/uninstall_pgq.sql
%{pginstdir}/share/extension/londiste--3.1--3.1.4.sql
%{pginstdir}/share/extension/londiste--3.1.1--3.1.4.sql
%{pginstdir}/share/extension/londiste--3.1.3--3.1.4.sql
%{pginstdir}/share/extension/londiste--3.1.4.sql
%{pginstdir}/share/extension/londiste--unpackaged--3.1.4.sql
%{pginstdir}/share/extension/londiste.control
%{pginstdir}/share/extension/pgq--3.1--3.1.3.sql
%{pginstdir}/share/extension/pgq--3.1.1--3.1.3.sql
%{pginstdir}/share/extension/pgq--3.1.2--3.1.3.sql
%{pginstdir}/share/extension/pgq--3.1.3.sql
%{pginstdir}/share/extension/pgq--unpackaged--3.1.3.sql
%{pginstdir}/share/extension/pgq.control
%{pginstdir}/share/extension/pgq_coop--3.1--3.1.1.sql
%{pginstdir}/share/extension/pgq_coop--3.1.1.sql
%{pginstdir}/share/extension/pgq_coop--unpackaged--3.1.1.sql
%{pginstdir}/share/extension/pgq_coop.control
%{pginstdir}/share/extension/pgq_ext--3.1.sql
%{pginstdir}/share/extension/pgq_ext--unpackaged--3.1.sql
%{pginstdir}/share/extension/pgq_ext.control
%{pginstdir}/share/extension/pgq_node--3.1--3.1.3.sql
%{pginstdir}/share/extension/pgq_node--3.1.3.sql
%{pginstdir}/share/extension/pgq_node--unpackaged--3.1.3.sql
%{pginstdir}/share/extension/pgq_node.control
%{_docdir}/skytools3/conf/pgqd.ini.templ
%{_docdir}/skytools3/conf/wal-master.ini
%{_docdir}/skytools3/conf/wal-slave.ini
%{_docdir}/pgsql/extension/README.pgq
%{_docdir}/pgsql/extension/README.pgq_ext
%{_mandir}/man1/londiste3.1.gz
%{_mandir}/man1/pgqd.1.gz
%{_mandir}/man1/qadmin.1.gz
%{_mandir}/man1/queue_mover3.1.gz
%{_mandir}/man1/queue_splitter3.1.gz
%{_mandir}/man1/scriptmgr3.1.gz
%{_mandir}/man1/simple_consumer3.1.gz
%{_mandir}/man1/simple_local_consumer3.1.gz
%{_mandir}/man1/skytools_upgrade3.1.gz
%{_mandir}/man1/walmgr3.1.gz
%{_datadir}/skytools3/londiste.upgrade_2.1_to_3.1.sql
%{_datadir}/skytools3/pgq.upgrade_2.1_to_3.0.sql

%{_datadir}/skytools3/londiste.sql
%{_datadir}/skytools3/londiste.upgrade.sql
%{_datadir}/skytools3/pgq.sql
%{_datadir}/skytools3/pgq.upgrade.sql
%{_datadir}/skytools3/pgq_coop.sql
%{_datadir}/skytools3/pgq_coop.upgrade.sql
%{_datadir}/skytools3/pgq_ext.sql
%{_datadir}/skytools3/pgq_ext.upgrade.sql
%{_datadir}/skytools3/pgq_node.sql
%{_datadir}/skytools3/pgq_node.upgrade.sql

%files modules
%{pginstdir}/lib/pgq_lowlevel.so
%{pginstdir}/share/contrib/pgq_lowlevel.sql
%{pginstdir}/lib/pgq_triggers.so
%{pginstdir}/share/contrib/pgq_triggers.sql

%changelog
* Tue Aug 20 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 3.1.5-1
- Update to 3.1.5, per changes described at
  http://pgfoundry.org/frs/shownotes.php?release_id=2045

* Tue Jan 15 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 3.1.3-1
- Update to 3.1.3

* Fri Jul 27 2012 - Devrim Gunduz <devrim@gunduz.org> - 3.1-1
- Update to 3.1
- Re-add mistakenly removed modules subpackage

* Fri Jun 8 2012 - Devrim Gunduz <devrim@gunduz.org> - 3.0.3-1
- Update to 3.0.3

* Tue Mar 8 2011 Devrim GUNDUZ <devrim@gunduz.org> - 2.1.12-1
- Update to 2.1.12

* Thu Mar 11 2010 Devrim GUNDUZ <devrim@gunduz.org> - 2.1.11-1
- Update to 2.1.11
- Apply fixes for multiple PostgreSQL installation.
- Trim changelog
