%global pginstdir /usr/pgsql-9.0
%global pgmajorversion 90
%global sname   skytools

# Python major version.
%{expand: %%define pyver %(python -c 'import sys;print(sys.version[0:3])')}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary:	PostgreSQL database management tools from Skype
Name:		%{sname}-%{pgmajorversion}
Version:	2.1.11
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://pgfoundry.org/frs/download.php/2561/%{sname}-%{version}.tar.gz
Patch0:		skytools-9.0-scankeywordlookup.patch
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
%patch0 -p1

%build
autoconf
./configure --with-pgconfig=%{pginstdir}/bin/pg_config  --prefix=%{pginstdir}

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
%attr(755,root,root) %{pginstdir}/bin/*.py
%attr(755,root,root) %{pginstdir}/bin/*.pyc
%ghost %attr(755,root,root) %{pginstdir}/bin/*.pyo
%{pginstdir}/man/man1/bulk_loader.*
%{pginstdir}/man/man1/cube_dispatcher.*
%{pginstdir}/man/man1/londiste.*
%{pginstdir}/man/man1/pgqadm.*
%{pginstdir}/man/man1/queue_mover.*
%{pginstdir}/man/man1/queue_splitter.*
%{pginstdir}/man/man1/scriptmgr.*
%{pginstdir}/man/man1/skytools_upgrade.*
%{pginstdir}/man/man1/table_dispatcher.*
%{pginstdir}/man/man1/walmgr.*
%{pginstdir}/man/man5/londiste.*
%{pginstdir}/share/contrib/londiste.sql
%{pginstdir}/share/contrib/londiste.upgrade.sql
%{pginstdir}/share/contrib/pgq.sql
%{pginstdir}/share/contrib/pgq.upgrade.sql
%{pginstdir}/share/contrib/pgq_ext.sql
%{pginstdir}/share/contrib/uninstall_pgq.sql
%{pginstdir}/lib*/*.so
%{pginstdir}/lib*/python%{pyver}/site-packages/londiste/*.py
%{pginstdir}/lib*/python%{pyver}/site-packages/skytools/*.py
%{pginstdir}/lib*/python%{pyver}/site-packages/pgq/*.py
%{pginstdir}/lib*/python%{pyver}/site-packages/londiste/*.pyo
%{pginstdir}/lib*/python%{pyver}/site-packages/skytools/*.pyo
%{pginstdir}/lib*/python%{pyver}/site-packages/pgq/*.pyo
%{pginstdir}/lib*/python%{pyver}/site-packages/londiste/*.pyc
%{pginstdir}/lib*/python%{pyver}/site-packages/skytools/*.pyc
%{pginstdir}/lib*/python%{pyver}/site-packages/pgq/*.pyc
%{pginstdir}/lib*/python%{pyver}/site-packages/skytools/_cquoting.so
%{pginstdir}/share/contrib/*.sql
%{pginstdir}/share/skytools/*.sql
%{pginstdir}/share/skytools/upgrade/final/v2.1**.sql
%{pginstdir}/share/doc/skytools/conf/*
%dir %{_docdir}/pgsql/contrib
%{_docdir}/pgsql/contrib/README.*

%changelog
* Thu Mar 11 2010 Devrim GUNDUZ <devrim@gunduz.org> - 2.1.11-1
- Update to 2.1.11
- Apply fixes for multiple PostgreSQL installation.
- Trim changelog
