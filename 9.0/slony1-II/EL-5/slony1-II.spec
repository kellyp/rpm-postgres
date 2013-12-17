%global pginstdir /usr/pgsql-9.0
%global pgmajorversion 90
%global sname	slony1
%{!?docs:%global docs 1}

Summary:	A "master to multiple slaves" replication system with cascading and failover
Name:		%{sname}-%{pgmajorversion}-II
Version:	2.1.4
Release:	3%{?dist}
License:	BSD
Group:		Applications/Databases
URL:		http://main.slony.info/
Source0:	http://main.slony.info/downloads/2.1/source/%{sname}-%{version}.tar.bz2
Source2:	filter-requires-perl-Pg.sh
Source3:	http://www.slony.info/adminguide/2.1/doc/adminguide/slony.pdf
BuildRoot:	%{_tmppath}/%{sname}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	postgresql%{pgmajorversion}-devel, postgresql%{pgmajorversion}-server, initscripts, byacc, flex
Requires:	postgresql%{pgmajorversion}-server, perl-DBD-Pg
Conflicts:	slony1

%description
Slony-I is a "master to multiple slaves" replication 
system for PostgreSQL with cascading and failover.

The big picture for the development of Slony-I is to build
a master-slave system that includes all features and
capabilities needed to replicate large databases to a
reasonably limited number of slave systems.

Slony-I is a system for data centers and backup
sites, where the normal mode of operation is that all nodes
are available

%if %docs
%package docs
Summary:	Documentation for Slony-I
Group:		Applications/Databases
Requires:	%{sname}-%{pgmajorversion}
Obsoletes:	slony1-docs

%description docs
The slony1-docs package includes PDF documentation for Slony-I.

%endif

%global __perl_requires %{SOURCE2}

%prep
%setup -q -n %{sname}-%{version}

cp -p %{SOURCE3} .

%build

CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS
CPPFLAGS="${CPPFLAGS} -I%{_includedir}/et -I%{_includedir}" ; export CPPFLAGS
CFLAGS="${CFLAGS} -I%{_includedir}/et -I%{_includedir}" ; export CFLAGS

export LIBNAME=%{_lib}
%configure --prefix=%{pginstdir} --includedir %{pginstdir}/include --with-pgconfigdir=%{pginstdir}/bin --libdir=%{pginstdir}/lib \
	--with-perltools=%{pginstdir}/bin --sysconfdir=%{_sysconfdir}/%{sname}-%{pgmajorversion} \
	--datadir=%{pginstdir}/share --with-pglibdir=%{pginstdir}/lib --sysconfdir=%{_sysconfdir}/%{name}

make %{?_smp_mflags}
make %{?_smp_mflags} -C tools

%install
rm -rf %{buildroot}
make %{?_smp_mflags} DESTDIR=%{buildroot} install

# Install sample slon.conf file
install -m 0644 share/slon.conf-sample %{buildroot}%{_sysconfdir}/%{name}/slon.conf
install -m 0644 tools/altperl/slon_tools.conf-sample %{buildroot}%{_sysconfdir}/%{name}/slon_tools.conf

# Fix the log path
sed "s:\([$]LOGDIR = '/var/log/slony1\):\1-%{pgmajorversion}:" -i %{buildroot}%{_sysconfdir}/%{name}/slon_tools.conf

# Install init script
install -d %{buildroot}%{_initrddir}
install -m 755 redhat/slony1.init %{buildroot}%{_initrddir}/%{name}

cd tools
make %{?_smp_mflags} DESTDIR=%{buildroot} install
/bin/rm -f %{buildroot}%{_sysconfdir}/%{sname}-%{pgmajorversion}/slon_tools.conf-sample
# Perform some cleanup
/bin/rm -f %{buildroot}%{_datadir}/pgsql/*.sql
/bin/rm -f %{buildroot}%{_libdir}/slony1_funcs.so

%clean
rm -rf %{buildroot}

%post
chkconfig --add slony1-II-90
if [ ! -e "/var/log/slony1-II-90" -a ! -h "/var/log/slony1-II-90" ]
then
        mkdir /var/log/slony1-II-90
        chown postgres:postgres /var/log/slony1-II-90
fi

%preun
if [ $1 = 0 ] ; then
	/sbin/service %{sname}-%{pgmajorversion} condstop >/dev/null 2>&1
	chkconfig --del %{sname}-%{pgmajorversion}
fi

%postun
if [ $1 -ge 1 ]; then
	/sbin/service %{sname}-%{pgmajorversion} condrestart >/dev/null 2>&1
fi

%files
%defattr(-,root,root,-)
%attr(644,root,root) %doc COPYRIGHT UPGRADING HISTORY-1.1 INSTALL SAMPLE RELEASE-2.0 RELEASE
%{pginstdir}/bin/slon*
%{pginstdir}/lib/slon*
%{pginstdir}/share/slon*
%config(noreplace) %{_sysconfdir}/%{name}/slon.conf
%config(noreplace) %{_sysconfdir}/%{name}/slon_tools.conf
%config(noreplace) %{_sysconfdir}/%{name}/slon_tools.conf-sample
%attr(755,root,root) %{_initrddir}/%{name}

%if %docs
%files docs
%attr(644,root,root) %doc *.pdf
%endif

%changelog
* Mon Aug 26 2013 Jeff Frost <jeff@pgexperts.com> 2.1.4-3
- Fix slon_tools.conf location for sed command

* Tue Aug 23 2013 Xavier Bergade <XavierB@benon.com> 2.1.4-2
- Set --sysconfdir during configure to fix the require list & the CONFIG_FILE
  path in the Perl scripts
- Set the correct path for LOGDIR in the slon_tools.conf file

* Tue Aug 20 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 2.1.4-1
- Update to 2.1.4

* Thu Mar 14 2013 Devrim Gunduz <devrim@gunduz.org> 2.1.3-1
- Update to 2.1.3
- Fix init script names in %%postun and %%preun.

* Sat Sep 1 2012 Devrim Gunduz <devrim@gunduz.org> 2.1.2-1
- Update to 2.1.2

* Mon Feb 13 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 2.1.1-1
- Update to 2.1.1

* Wed Oct 05 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 2.1.0-1
- Initial 2.1.0 packaging.
- Trim changelog.
- Install only PDF docs, don't build HTML anymore.
