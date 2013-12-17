%global pginstdir /usr/pgsql-8.4
%global pgmajorversion 84
%global sname	slony1
%{!?docs:%global docs 0}

Summary:	A "master to multiple slaves" replication system with cascading and failover
Name:		%{sname}-%{pgmajorversion}-II
Version:	2.0.7
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
URL:		http://main.slony.info/
Source0:	http://main.slony.info/downloads/2.0/source/%{sname}-%{version}.tar.bz2
Source2:	filter-requires-perl-Pg.sh
BuildRoot:	%{_tmppath}/%{sname}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	postgresql%{pgmajorversion}-devel, postgresql%{pgmajorversion}-server, initscripts, byacc, flex
Requires:	postgresql%{pgmajorversion}-server, perl-DBD-Pg
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
Requires:	%{sname}-%{pgmajorversion}-II
BuildRequires:	libjpeg, netpbm-progs, groff, docbook-style-dsssl, ghostscript
Obsoletes:	slony1-docs

%description docs
The slony1-docs package includes some documentation for Slony-I.
%endif

%global __perl_requires %{SOURCE2}

%prep
%setup -q -n %{sname}-%{version}
%build

# Fix permissions of docs.
%if %docs
find doc/ -type f -exec chmod 600 {} \;
%endif

CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS
CPPFLAGS="${CPPFLAGS} -I%{_includedir}/et -I%{_includedir}" ; export CPPFLAGS
CFLAGS="${CFLAGS} -I%{_includedir}/et -I%{_includedir}" ; export CFLAGS

export LIBNAME=%{_lib}
%configure --prefix=%{pginstdir} --includedir %{pginstdir}/include --with-pgconfigdir=%{pginstdir}/bin --libdir=%{pginstdir}/lib \
	--with-perltools=%{pginstdir}/bin \
%if %docs
	--with-docs --with-docdir=%{_docdir}/%{sname}-%{version} \
%endif
	--datadir=%{pginstdir}/share --with-pglibdir=%{pginstdir}/lib 

make %{?_smp_mflags}
make %{?_smp_mflags} -C tools

%install
rm -rf %{buildroot}
make %{?_smp_mflags} DESTDIR=%{buildroot} install

# Install sample slon.conf file
install -m 0644 share/slon.conf-sample %{buildroot}%{_sysconfdir}/slon.conf
install -m 0644 tools/altperl/slon_tools.conf-sample %{buildroot}%{_sysconfdir}/slon_tools.conf

# change file modes of docs.
/bin/chmod 644 COPYRIGHT UPGRADING SAMPLE HISTORY-1.1 RELEASE

# Install init script
install -d %{buildroot}%{_initrddir}
install -m 755 redhat/slony1.init %{buildroot}%{_initrddir}/%{sname}-%{pgmajorversion}-II

# Temporary measure for 1.2.X
%if %docs
	rm -f doc/implementation/.cvsignore
	rm -f doc/concept/.cvsignore
%endif

cd tools
make %{?_smp_mflags} DESTDIR=%{buildroot} install
/bin/rm -f %{buildroot}%{_sysconfdir}/slon_tools.conf-sample
# Perform some cleanup
/bin/rm -f %{buildroot}%{_datadir}/pgsql/*.sql
/bin/rm -f %{buildroot}%{_libdir}/slony1_funcs.so

%clean
rm -rf %{buildroot}

%post
chkconfig --add slony-84-II
if [ ! -e "/var/log/slony1-84" -a ! -h "/var/log/slony1-84" ]
then
        mkdir /var/log/slony1-84
        chown postgres:postgres /var/log/slony1-84
fi

%preun
if [ $1 = 0 ] ; then
	/sbin/service slony1-84-II condstop >/dev/null 2>&1
	chkconfig --del slony1-84-II
fi

%postun
if [ $1 -ge 1 ]; then
	/sbin/service slony1-84-II condrestart >/dev/null 2>&1
fi

%files
%defattr(-,root,root,-)
%attr(644,root,root) %doc COPYRIGHT UPGRADING HISTORY-1.1 INSTALL SAMPLE RELEASE
%{pginstdir}/bin/slon*
%{pginstdir}/lib/slon*
%{pginstdir}/share/slon*
%config(noreplace) %{_sysconfdir}/slon.conf
%config(noreplace) %{_sysconfdir}/slon_tools.conf
%attr(755,root,root) %{_initrddir}/slony1-%{pgmajorversion}-II

%if %docs
%files docs
%attr(644,root,root) %doc doc/adminguide  doc/concept  doc/howto  doc/implementation  doc/support
%endif

%changelog
* Wed Aug 10 2011 Devrim Gunduz <devrim@gunduz.org> 2.0.7-1
- Update to 2.0.7

* Thu Dec 9 2010 Devrim Gunduz <devrim@gunduz.org> 2.0.6-1
- Update to 2.0.6

* Fri Nov 19 2010 Devrim Gunduz <devrim@gunduz.org> 2.0.6.rc2-1
- Update to 2.0.6 rc2
- Use 9.0 layout

* Sat Sep 18 2010 Devrim Gunduz <devrim@gunduz.org> 2.0.4-1
- Update to 2.0.4, and perform a major cleanup and bugfix.
- Apply changes for 9.0+
- Update source2, to supress weird dependency for slon_tools.conf.

* Wed Apr 21 2010 Devrim Gunduz <devrim@gunduz.org> 2.0.3-2
- Fix an issue regarding slon_tools.pm, per report from David Fetter.
- Use Conflicts, instead of Obsoletes.
- Create log directory if it does not exist.

* Sat Apr 10 2010 Devrim Gunduz <devrim@gunduz.org> 2.0.3-1
- Initial packaging of 2.0 branch for EL-5, per request from users.
