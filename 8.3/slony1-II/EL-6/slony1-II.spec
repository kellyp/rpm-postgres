%global sname	slony1
%{!?docs:%global docs 0}
%{!?kerbdir:%global kerbdir "/usr"}

Summary:	A "master to multiple slaves" replication system with cascading and failover
Name:		%{sname}-II
Version:	2.0.3
Release:	2%{?dist}
License:	BSD
Group:		Applications/Databases
URL:		http://main.slony.info/
Source0:	http://main.slony.info/downloads/2.0/source/%{sname}-%{version}.tar.bz2
Source2:	filter-requires-perl-Pg.sh
Patch2:		%{sname}-%{version}-doc.patch
BuildRoot:	%{_tmppath}/%{sname}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	postgresql-devel, postgresql-server, initscripts, byacc, flex
Requires:	postgresql-server, perl-DBD-Pg
Conflicts:	slony1

%if %docs
BuildRequires:	docbook-style-dsssl postgresql_autodoc docbook-utils
%endif

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
Requires:	%{sname}
BuildRequires:	libjpeg, netpbm-progs, groff, docbook-style-dsssl, ghostscript
Obsoletes:	slony1-docs

%description docs
The slony1-docs package includes some documentation for Slony-I.
%endif

%global __perl_requires %{SOURCE2}

%prep
%setup -q -n %{sname}-%{version}
%patch2 -p0
%build

# Fix permissions of docs.
%if %docs
find doc/ -type f -exec chmod 600 {} \;
%endif

CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS
CPPFLAGS="${CPPFLAGS} -I%{_includedir}/et -I%{kerbdir}/include" ; export CPPFLAGS
CFLAGS="${CFLAGS} -I%{_includedir}/et -I%{kerbdir}/include" ; export CFLAGS

export LIBNAME=%{_lib}
%configure --includedir %{_includedir} --with-pgconfigdir=%{_bindir} --libdir=%{_libdir} \
	--with-perltools=%{_bindir} \
%if %docs
	--with-docs --with-docdir=%{_docdir}/%{sname}-%{version} \
%endif
	--datadir=%{_datadir} --with-pglibdir=%{_libdir} 

make %{?_smp_mflags}
make %{?_smp_mflags} -C tools

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_datadir}/pgsql/
install -d %{buildroot}%{_libdir}/pgsql/
make %{?_smp_mflags} DESTDIR=%{buildroot} install
install -m 0755 src/backend/slony1_funcs.so %{buildroot}%{_libdir}/pgsql/slony1_funcs.so
install -m 0644 src/backend/*.sql %{buildroot}%{_datadir}/pgsql/
install -m 0755 tools/*.sh  %{buildroot}%{_bindir}/
install -m 0755 tools/*.pl  %{buildroot}%{_bindir}/
install -m 0644 share/slon.conf-sample %{buildroot}%{_sysconfdir}/slon.conf
/bin/chmod 644 COPYRIGHT UPGRADING SAMPLE HISTORY-1.1 RELEASE

install -d %{buildroot}%{_initrddir}
install -m 755 redhat/slon.init %{buildroot}%{_initrddir}/slony1-II

# Temporary measure for 1.2.X
%if %docs
	rm -f doc/implementation/.cvsignore
	rm -f doc/concept/.cvsignore
%endif

cd tools
make %{?_smp_mflags} DESTDIR=%{buildroot} install
/bin/rm -rf altperl/*.pl altperl/ToDo altperl/README altperl/Makefile altperl/CVS
install -m 0644 altperl/slon_tools.conf-sample  %{buildroot}%{_sysconfdir}/slon_tools.conf
install -m 0755 altperl/* %{buildroot}%{_bindir}/
install -m 0644 altperl/slon-tools  %{buildroot}%{_libdir}/pgsql/slon-tools.pm
/bin/rm -f %{buildroot}%{_sysconfdir}/slon_tools.conf-sample
/bin/rm -f %{buildroot}%{_bindir}/slon_tools.conf-sample
/bin/rm -f  %{buildroot}%{_bindir}/slon-tools.pm
/bin/rm -f %{buildroot}%{_bindir}/slon-tools
/bin/rm -f %{buildroot}%{_bindir}/pgsql/slon-tools
/bin/rm -f %{buildroot}%{_bindir}/old-apache-rotatelogs.patch

%clean
rm -rf %{buildroot}

%post
chkconfig --add slony1-II
if [ ! -e "/var/log/slony1" -a ! -h "/var/log/slony1" ]
then
        mkdir /var/log/slony1
        chown postgres:postgres /var/log/slony1
fi

%preun
if [ $1 = 0 ] ; then
	/sbin/service slony1-II condstop >/dev/null 2>&1
	chkconfig --del slony1-II
fi

%postun
if [ $1 -ge 1 ]; then
	/sbin/service slony1-II condrestart >/dev/null 2>&1
fi

%files
%defattr(-,root,root,-)
%attr(644,root,root) %doc COPYRIGHT UPGRADING HISTORY-1.1 INSTALL SAMPLE RELEASE
%{_bindir}/*
%{_libdir}/pgsql/slony1_funcs.so
%{_datadir}/pgsql/*.sql
%config(noreplace) %{_sysconfdir}/slon.conf
%{_libdir}/pgsql/slon-tools.pm
%{_libdir}/slon-tools.pm
%config(noreplace) %{_sysconfdir}/slon_tools.conf
%attr(755,root,root) %{_initrddir}/slony1-II

%if %docs
%files docs
%attr(644,root,root) %doc doc/adminguide  doc/concept  doc/howto  doc/implementation  doc/support
%endif

%changelog
* Wed Apr 21 2010 Devrim Gunduz <devrim@gunduz.org> 2.0.3-2
- Fix an issue regarding slon_tools.pm, per report from David Fetter.
- Use Conflicts, instead of Obsoletes.

* Sat Apr 10 2010 Devrim Gunduz <devrim@gunduz.org> 2.0.3-1
- Initial packaging of 2.0 branch for EL-5, per request from users.
