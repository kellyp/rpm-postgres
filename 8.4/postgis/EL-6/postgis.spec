%global postgismajorversion 1.5
%global pgmajorversion 84
%global pginstdir /usr/pgsql-8.4
%global sname	postgis
%{!?javabuild:%define	javabuild 0}
%{!?utils:%define	utils 1}
%{!?gcj_support:%define	gcj_support 1}

Summary:	Geographic Information Systems Extensions to PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	1.5.3
Release:	1%{?dist}
License:	GPLv2+
Group:		Applications/Databases
Source0:	http://postgis.refractions.net/download/%{sname}-%{version}.tar.gz
Source2:	http://www.postgis.org/download/%{sname}-%{version}.pdf
Source4:	filter-requires-perl-Pg.sh
URL:		http://postgis.refractions.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	postgresql%{pgmajorversion}-devel, proj-devel, geos-devel, byacc, proj-devel, flex, java-devel, java, ant

Requires:	postgresql%{pgmajorversion}, geos, proj
Requires(post):	%{_sbindir}/update-alternatives

%description
PostGIS adds support for geographic objects to the PostgreSQL object-relational
database. In effect, PostGIS "spatially enables" the PostgreSQL server,
allowing it to be used as a backend spatial database for geographic information
systems (GIS), much like ESRI's SDE or Oracle's Spatial extension. PostGIS 
follows the OpenGIS "Simple Features Specification for SQL" and has been 
certified as compliant with the "Types and Functions" profile.

%package docs
Summary:	Extra documentation for PostGIS
Group:		Applications/Databases
%description docs
The postgis-docs package includes PDF documentation of PostGIS.

%if %javabuild
%package jdbc
Summary:	The JDBC driver for PostGIS
Group:		Applications/Databases
License:	LGPL
Requires:	%{name} = %{version}-%{release}, postgresql%{pgmajorversion}-jdbc
BuildRequires:	ant >= 0:1.6.2, junit >= 0:3.7

%if %{gcj_support}
BuildRequires:		gcc-java, postgresql%{pgmajorversion}-jdbc
Requires(post):		java-1.4.2-gcj-compat
Requires(postun):	java-1.4.2-gcj-compat
%endif

%description jdbc
The postgis-jdbc package provides the essential jdbc driver for PostGIS.
%endif

%if %utils
%package utils
Summary:	The utils for PostGIS
Group:		Applications/Databases
Requires:	%{name} = %{version}-%{release}, perl-DBD-Pg

%description utils
The postgis-utils package provides the utilities for PostGIS.
%endif

%define __perl_requires %{SOURCE4}

%prep
%setup -q -n %{sname}-%{version}
# Copy .pdf file to top directory before installing.
cp -p %{SOURCE2} .

%build
%configure --with-pgconfig=%{pginstdir}/bin/pg_config
make %{?_smp_mflags} LPATH=`%{pginstdir}/bin/pg_config --pkglibdir` shlib="%{name}.so"

%if %javabuild
export BUILDXML_DIR=%{_builddir}/%{name}-%{version}/java/jdbc
JDBC_VERSION_RPM=`rpm -ql postgresql%{pgmajorversion}-jdbc| grep 'jdbc2.jar$'|awk -F '/' '{print $5}'`
sed 's/postgresql.jar/'${JDBC_VERSION_RPM}'/g' $BUILDXML_DIR/build.xml > $BUILDXML_DIR/build.xml.new
mv -f $BUILDXML_DIR/build.xml.new $BUILDXML_DIR/build.xml
pushd java/jdbc
ant
popd
%endif

%if %utils
 make -C utils
%endif

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
install -d  %{buildroot}%{pginstdir}/share/contrib/

#if [ "%{_libdir}" = "/usr/lib64" ] ; then
#	mv %{buildroot}%{pginstdir}/share/contrib/lwpostgis.sql %{buildroot}%{pginstdir}/share/contrib/lwpostgis-64.sql
#	mv %{buildroot}%{pginstdir}/share/contrib/lwpostgis_upgrade.sql %{buildroot}%{pginstdir}/share/contrib/lwpostgis_upgrade-64.sql
#fi

%if %javabuild
install -d %{buildroot}%{_javadir}
install -m 755 java/jdbc/%{name}_%{version}.jar %{buildroot}%{_javadir}
%if %{gcj_support}
aot-compile-rpm
%endif
strip %{buildroot}/%{_libdir}/gcj/%{name}/*.jar.so
%endif

%if %utils
install -d %{buildroot}%{_datadir}/%{name}
install -m 644 utils/*.pl %{buildroot}%{_datadir}/%{name}
%endif

# Create alternatives entries for common binaries
%post
%{_sbindir}/update-alternatives --install /usr/bin/pgsql2shp postgis-pgsql2shp %{pginstdir}/bin/pgsql2shp 840
%{_sbindir}/update-alternatives --install /usr/bin/shp2pgsql postgis-shp2pgsql %{pginstdir}/bin/shp2pgsql 840

# Drop alternatives entries for common binaries and man files
%postun
if [ "$1" -eq 0 ]
  then
	# Only remove these links if the package is completely removed from the system (vs.just being upgraded)
	%{_sbindir}/update-alternatives --remove postgis-pgsql2shp	%{pginstdir}/bin/pgsql2shp
	%{_sbindir}/update-alternatives --remove postgis-shp2pgsql	%{pginstdir}/bin/shp2pgsql
fi

%clean
rm -rf %{buildroot}

%if %javabuild
%if %gcj_support
%post -p %{_bindir}/rebuild-gcj-db
%postun -p %{_bindir}/rebuild-gcj-db
%endif
%endif

%files
%defattr(-,root,root)
%doc COPYING CREDITS NEWS TODO README.%{sname} doc/html loader/README.* doc/%{sname}.xml doc/ZMSgeoms.txt
%attr(755,root,root) %{pginstdir}/bin/*
%attr(755,root,root) %{pginstdir}/lib/%{sname}-*.so
%attr(755,root,root) %{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/*.sql

%if %javabuild
%files jdbc
%defattr(-,root,root)
%doc java/jdbc/COPYING_LGPL java/jdbc/README
%attr(755,root,root) %{_javadir}/%{sname}_%{version}.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%{_libdir}/gcj/%{name}/*.jar.so
%{_libdir}/gcj/%{name}/*.jar.db
%endif
%endif

%if %utils
%files utils
%defattr(-,root,root)
%doc utils/README
%{_datadir}/%{name}/*.pl
%endif

%files docs
%defattr(-,root,root)
%doc postgis*.pdf

%changelog
* Thu Aug 11 2011 - Devrim GÜNDÜZ <devrim@gunduz.org> - 1.5.3-1
- Update to 1.5.3
- Fix error in uninstall, per report from Pete Deffendol.

* Sun Jan 9 2011 Oct 6 2010 Devrim GUNDUZ <devrim@gunduz.org> - 1.5.2-2
- Add alternatives entries for pgsql2shp and shp2pgsql binaries. Per
  suggestion from Pete Deffendol.

* Wed Dec 1 2010 Devrim GUNDUZ <devrim@gunduz.org> - 1.5.2-1
- Update to 1.5.2, and refactor spec file for PostgreSQL 8.4 RPMs.
- on RHEL/CentOS 6.
- Disable javabuild for now, until I find a good solution for that.
- Trim changelog
