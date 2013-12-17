%global pgmajorversion 84
%global pginstdir /usr/pgsql-8.4
%global pgpoolinstdir /usr/pgpool-8.4
%global sname pgpool-II

Summary:	Pgpool is a connection pooling/replication server for PostgreSQL
Name:		%{sname}-%{pgmajorversion}
Version:	3.0.4
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
URL:		http://pgpool.projects.PostgreSQL.org
Source0:	http://pgfoundry.org/frs/download.php/3076/%{sname}-%{version}.tar.gz
Source1:        pgpool.init
Source2:        pgpool.sysconfig
Patch1:		pgpool.conf.sample.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	postgresql%{pgmajorversion}-devel pam-devel
Requires(post):	%{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives

Obsoletes:	postgresql-pgpool

%description
pgpool-II is a inherited project of pgpool (to classify from 
pgpool-II, it is sometimes called as pgpool-I). For those of 
you not familiar with pgpool-I, it is a multi-functional 
middle ware for PostgreSQL that features connection pooling, 
replication and load balancing functions. pgpool-I allows a 
user to connect at most two PostgreSQL servers for higher 
availability or for higher search performance compared to a 
single PostgreSQL server.

pgpool-II, on the other hand, allows multiple PostgreSQL 
servers (DB nodes) to be connected, which enables queries 
to be executed simultaneously on all servers. In other words, 
it enables "parallel query" processing. Also, pgpool-II can 
be started as pgpool-I by changing configuration parameters. 
pgpool-II that is executed in pgpool-I mode enables multiple 
DB nodes to be connected, which was not possible in pgpool-I. 

%package devel
Summary:	The  development files for pgpool-II
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Development headers and libraries for pgpool-II.

%prep
%setup -q -n %{sname}-%{version}
%patch1 -p0

%build
./configure --exec-prefix=%{pgpoolinstdir} --with-pgsql=%{pginstdir} --disable-static --with-pam --disable-rpath --sysconfdir=%{_sysconfdir}/%{name}/ --includedir=%{pgpoolinstdir}/include --datadir=%{pgpoolinstdir}/share --mandir=%{pgpoolinstdir}/man

make %{?_smp_flags}

%install
rm -rf %{buildroot}
make %{?_smp_flags} DESTDIR=%{buildroot} install
install -d %{buildroot}%{_initrddir}
sed 's/^PGVERSION=.*$/PGVERSION=%{pgmajorversion}/' <%{SOURCE1} > pgpool-II-%{pgmajorversion}.init
install -m 755 pgpool-II-%{pgmajorversion}.init %{buildroot}%{_initrddir}/pgpool-II-%{pgmajorversion}
install -d %{buildroot}%{_sysconfdir}/sysconfig/
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/pgpool-II-%{pgmajorversion}

# nuke libtool archive and static lib
rm -f %{buildroot}%{pgpoolinstdir}/lib/libpcp.{a,la}

%clean
rm -rf %{buildroot}

%post 
/sbin/ldconfig
chkconfig --add %{sname}-%{pgmajorversion}
# Create alternatives entries for common binaries and man files
%{_sbindir}/update-alternatives --install /usr/bin/pgpool pgpool-pgpool %{pgpoolinstdir}/bin/pgpool 840
%{_sbindir}/update-alternatives --install /usr/bin/pcp_attach_node pgpool-pcp_attach_node %{pgpoolinstdir}/bin/pcp_attach_node 840
%{_sbindir}/update-alternatives --install /usr/bin/pcp_detach_node pgpool-pcp_detach_node %{pgpoolinstdir}/bin/pcp_detach_node 840
%{_sbindir}/update-alternatives --install /usr/bin/pcp_node_count pgpool-pcp_node_count %{pgpoolinstdir}/bin/pcp_node_count 840
%{_sbindir}/update-alternatives --install /usr/bin/pcp_node_info pgpool-pcp_node_info %{pgpoolinstdir}/bin/pcp_node_info 840
%{_sbindir}/update-alternatives --install /usr/bin/pcp_proc_count pgpool-pcp_proc_count %{pgpoolinstdir}/bin/pcp_proc_count 840
%{_sbindir}/update-alternatives --install /usr/bin/pcp_proc_info pgpool-pcp_proc_info %{pgpoolinstdir}/bin/pcp_proc_info 840
%{_sbindir}/update-alternatives --install /usr/bin/pcp_stop_pgpool pgpool-pcp_stop_pgpool %{pgpoolinstdir}/bin/pcp_stop_pgpool 840
%{_sbindir}/update-alternatives --install /usr/bin/pcp_recovery_node pgpool-pcp_recovery_node %{pgpoolinstdir}/bin/pcp_recovery_node 840
%{_sbindir}/update-alternatives --install /usr/bin/pcp_systemdb_info pgpool-pcp_systemdb_info %{pgpoolinstdir}/bin/cp_systemdb_info 840
%{_sbindir}/update-alternatives --install /usr/bin/pg_md5 pgpool-pg_md5 %{pgpoolinstdir}/bin/pg_md5 840

# Drop alternatives entries for common binaries and man files
%preun
if [ $1 = 0 ] ; then
	/sbin/service %{sname}-%{pgmajorversion} condstop >/dev/null 2>&1
	chkconfig --del %{sname}-%{pgmajorversion}
fi
%{_sbindir}/update-alternatives --remove pgpool-pgpool %{pgpoolinstdir}/bin/pgpool
%{_sbindir}/update-alternatives --remove pgpool-pcp_attach_node %{pgpoolinstdir}/bin/pcp_attach_node
%{_sbindir}/update-alternatives --remove pgpool-pcp_detach_node %{pgpoolinstdir}/bin/pcp_detach_node
%{_sbindir}/update-alternatives --remove pgpool-pcp_node_count %{pgpoolinstdir}/bin/pcp_node_count
%{_sbindir}/update-alternatives --remove pgpool-pcp_node_info %{pgpoolinstdir}/bin/pcp_node_info
%{_sbindir}/update-alternatives --remove pgpool-pcp_proc_count %{pgpoolinstdir}/bin/pcp_proc_count
%{_sbindir}/update-alternatives --remove pgpool-pcp_proc_info %{pgpoolinstdir}/bin/pcp_proc_info
%{_sbindir}/update-alternatives --remove pgpool-pcp_stop_pgpool %{pgpoolinstdir}/bin/pcp_stop_pgpool
%{_sbindir}/update-alternatives --remove pgpool-pcp_recovery_node %{pgpoolinstdir}/bin/pcp_recovery_node
%{_sbindir}/update-alternatives --remove pgpool-pcp_systemdb_info %{pgpoolinstdir}/bin/cp_systemdb_info
%{_sbindir}/update-alternatives --remove pgpool-pg_md5 %{pgpoolinstdir}/bin/pg_md5

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
#%dir %{_datadir}/%{name}
%{pgpoolinstdir}/bin/pgpool
%{pgpoolinstdir}/bin/pcp_attach_node
%{pgpoolinstdir}/bin/pcp_detach_node
%{pgpoolinstdir}/bin/pcp_node_count
%{pgpoolinstdir}/bin/pcp_node_info
%{pgpoolinstdir}/bin/pcp_proc_count
%{pgpoolinstdir}/bin/pcp_proc_info
%{pgpoolinstdir}/bin/pcp_stop_pgpool
%{pgpoolinstdir}/bin/pcp_recovery_node
%{pgpoolinstdir}/bin/pcp_systemdb_info
%{pgpoolinstdir}/bin/pg_md5
%{_sysconfdir}/pgpool-II-%{pgmajorversion}/pcp.conf.sample
%{_sysconfdir}/pgpool-II-%{pgmajorversion}/pgpool.conf.sample
%{_sysconfdir}/pgpool-II-%{pgmajorversion}/pgpool.conf.sample-master-slave
%{_sysconfdir}/pgpool-II-%{pgmajorversion}/pgpool.conf.sample-replication
%{_sysconfdir}/pgpool-II-%{pgmajorversion}/pgpool.conf.sample-stream
%{_sysconfdir}/pgpool-II-%{pgmajorversion}/pool_hba.conf.sample
%{pgpoolinstdir}/lib/libpcp.so*
%{pgpoolinstdir}/man/man8/pgpool.8
%{pgpoolinstdir}/share/pgpool-II/pgpool.pam
%{pgpoolinstdir}/share/pgpool-II/system_db.sql
%{_initrddir}/%{sname}-%{pgmajorversion}
%{_sysconfdir}/sysconfig/%{sname}-%{pgmajorversion}

%files devel
%defattr(-,root,root,-)
%{pgpoolinstdir}/include/pcp.h
%{pgpoolinstdir}/include/pool_type.h

%changelog
* Fri Aug 12 2011 Devrim GUNDUZ <devrim@gunduz.org> - 3.0.4
- Update to 3.0.4

* Tue Nov 9 2010 Devrim GUNDUZ <devrim@gunduz.org> - 3.0.1
- Update to 3.0.1
- Apply many 9.0+ specific changes, and use alternatives method.
- Apply some changes to init script.

* Sun Sep 26 2010 Devrim GUNDUZ <devrim@gunduz.org> - 3.0.0
- Update to 3.0

* Thu Jul 1 2010 Devrim GUNDUZ <devrim@gunduz.org> - 2.3.3-1
- Update to 2.3.3
- Enable compilation with PostgreSQL 9.0.

* Thu Dec 10 2009 Devrim GUNDUZ <devrim@gunduz.org> - 2.3-1
- Update to 2.3

* Tue Dec 1 2009 Devrim GUNDUZ <devrim@gunduz.org> - 2.2.6-1
- Update to 2.2.6

* Sun Nov 01 2009 Devrim GUNDUZ <devrim@gunduz.org> - 2.2.5-2
- Remove init script from all runlevels before uninstall. Per #RH Bugzilla
  532177

* Sun Oct 4 2009 Devrim Gunduz <devrim@gunduz.org> 2.2.5-1
- Update to 2.2.5, for various fixes described at
  http://lists.pgfoundry.org/pipermail/pgpool-general/2009-October/002188.html
- Re-apply a fix for Red Hat Bugzilla #442372

* Wed Sep 9 2009 Devrim Gunduz <devrim@gunduz.org> 2.2.4-1
- Update to 2.2.4

* Wed May 6 2009 Devrim Gunduz <devrim@gunduz.org> 2.2.2-1
- Update to 2.2.2

* Sun Mar 1 2009 Devrim Gunduz <devrim@gunduz.org> 2.2-1
- Update to 2.2
- Fix URL
- Own /usr/share/pgpool-II directory.
- Fix pid file path in init script, per	pgcore #81.
- Fix spec file -- we don't use short_name macro in pgcore spec file.
- Create pgpool pid file directory, per pgcore #81.
- Fix stop/start routines, also improve init script a bit.
- Install conf files to a new directory (/etc/pgpool-II), and get rid 
  of sample conf files.

* Fri Aug 8 2008 Devrim Gunduz <devrim@gunduz.org> 2.1-1
- Update to 2.1
- Removed temp patch #4.

* Sun Jan 13 2008 Devrim Gunduz <devrim@gunduz.org> 2.0.1-1
- Update to 2.0.1
- Add a temp patch that will disappear in 2.0.2

* Fri Oct 5 2007 Devrim Gunduz <devrim@gunduz.org> 1.2.1-1
- Update to 1.2.1

* Wed Aug 29 2007 Devrim Gunduz <devrim@gunduz.org> 1.2-5
- Chmod sysconfig/pgpool to 644, not 755. Per BZ review.
- Run chkconfig --add pgpool during %%post.

* Thu Aug 16 2007 Devrim Gunduz <devrim@gunduz.org> 1.2-4
- Fixed the directory name where sample conf files and sql files 
  are installed.

* Sun Aug 5 2007 Devrim Gunduz <devrim@gunduz.org> 1.2-3
- Added a patch for sample conf file to use Fedora defaults

* Sun Aug 5 2007 Devrim Gunduz <devrim@gunduz.org> 1.2-2
- Added an init script for pgpool
- Added /etc/sysconfig/pgpool

* Wed Aug 1 2007 Devrim Gunduz <devrim@gunduz.org> 1.2-1
- Update to 1.2

* Fri Jun 15 2007 Devrim Gunduz <devrim@gunduz.org> 1.1.1-1
- Update to 1.1.1

* Sat Jun 2 2007 Devrim Gunduz <devrim@gunduz.org> 1.1-1
- Update to 1.1
- added --disable-rpath configure parameter.
- Chowned sample conf files, so that they can work with pgpoolAdmin.

* Thu Apr 22 2007 Devrim Gunduz <devrim@gunduz.org> 1.0.2-4
- Added postgresql-devel as BR, per bugzilla review.
- Added --disable-static flan, per bugzilla review.
- Removed superfluous manual file installs, per bugzilla review.

* Thu Apr 22 2007 Devrim Gunduz <devrim@gunduz.org> 1.0.2-3
- Rebuilt for the correct tarball
- Fixed man8 file ownership, per bugzilla review #229321 

* Tue Feb 20 2007 Jarod Wilson <jwilson@redhat.com> 1.0.2-2
- Create proper devel package, drop -libs package
- Nuke rpath
- Don't install libtool archive and static lib
- Clean up %%configure line
- Use proper %%_smp_mflags
- Install config files properly, without .sample on the end
- Preserve timestamps on header files

* Tue Feb 20 2007 Devrim Gunduz <devrim@gunduz.org> 1.0.2-1
- Update to 1.0.2-1

* Mon Oct 02 2006 Devrim Gunduz <devrim@gunduz.org> 1.0.1-5
- Rebuilt

* Mon Oct 02 2006 Devrim Gunduz <devrim@gunduz.org> 1.0.1-4
- Added -libs and RPM
- Fix .so link problem
- Cosmetic changes to spec file

* Thu Sep 27 2006 - Devrim GUNDUZ <devrim@gunduz.org> 1.0.1-3
- Fix spec, per Yoshiyuki Asaba

* Thu Sep 26 2006 - Devrim GUNDUZ <devrim@gunduz.org> 1.0.1-2
- Fixed rpmlint errors
- Fixed download url
- Added ldconfig for .so files

* Thu Sep 21 2006 - David Fetter <david@fetter.org> 1.0.1-1
- Initial build pgpool-II 1.0.1 for PgPool Global Development Group

