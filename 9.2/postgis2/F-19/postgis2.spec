%global postgismajorversion 2.1
%global pgmajorversion 92
%global pginstdir /usr/pgsql-9.2
%global sname	postgis
%{!?utils:%define	utils 1}
%{!?raster:%define	raster 1}

Summary:	Geographic Information Systems Extensions to PostgreSQL
Name:		%{sname}2_%{pgmajorversion}
Version:	2.1.1
Release:	1%{?dist}
License:	GPLv2+
Group:		Applications/Databases
Source0:	http://download.osgeo.org/%{sname}/source/%{sname}-%{version}.tar.gz
Source2:	http://download.osgeo.org/%{sname}/docs/%{sname}-%{version}.pdf
Source4:	filter-requires-perl-Pg.sh

URL:		http://postgis.refractions.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	postgresql%{pgmajorversion}-devel, proj-devel, geos-devel >= 3.4.2
BuildRequires:	proj-devel, flex, json-c-devel, libxml2-devel
%if %raster
BuildRequires:	gdal-devel
%endif

Requires:	postgresql%{pgmajorversion}, geos >= 3.4.2, proj, hdf5, json-c
Requires(post):	%{_sbindir}/update-alternatives

Provides:	%{sname} = %{version}-%{release}

%description
PostGIS adds support for geographic objects to the PostgreSQL object-relational
database. In effect, PostGIS "spatially enables" the PostgreSQL server,
allowing it to be used as a backend spatial database for geographic information
systems (GIS), much like ESRI's SDE or Oracle's Spatial extension. PostGIS 
follows the OpenGIS "Simple Features Specification for SQL" and has been 
certified as compliant with the "Types and Functions" profile.

%package client
Summary:	Client tools and their libraries of PostGIS
Group:		Applications/Databases
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:	%{sname}-client = %{version}-%{release}

%description client
The postgis-client package contains the client tools and their libraries
of PostGIS.

%package devel
Summary:	Development headers and libraries for PostGIS
Group:		Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:	%{sname}-devel = %{version}-%{release}

%description devel
The postgis-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with PostGIS.

%package docs
Summary:	Extra documentation for PostGIS
Group:		Applications/Databases

%description docs
The postgis-docs package includes PDF documentation of PostGIS.

%if %utils
%package utils
Summary:	The utils for PostGIS
Group:		Applications/Databases
Requires:	%{name} = %{version}-%{release}, perl-DBD-Pg
Provides:	%{sname}-utils = %{version}-%{release}

%description utils
The postgis-utils package provides the utilities for PostGIS.
%endif

%define __perl_requires %{SOURCE4}

%prep
%setup -q -n %{sname}-%{version}
# Copy .pdf file to top directory before installing.
cp -p %{SOURCE2} .

%build
# We need the below for GDAL:
export LD_LIBRARY_PATH=%{pginstdir}/lib

%configure --with-pgconfig=%{pginstdir}/bin/pg_config \
%if !%raster
        --without-raster \
%endif
	 --disable-rpath --libdir=%{pginstdir}/lib

make %{?_smp_mflags} LPATH=`%{pginstdir}/bin/pg_config --pkglibdir` shlib="%{name}.so"
make -C extensions

%if %utils
 make -C utils
%endif

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%if %utils
install -d %{buildroot}%{_datadir}/%{name}
install -m 644 utils/*.pl %{buildroot}%{_datadir}/%{name}
%endif

# Create alternatives entries for common binaries
%post
%{_sbindir}/update-alternatives --install /usr/bin/pgsql2shp postgis-pgsql2shp %{pginstdir}/bin/pgsql2shp 930
%{_sbindir}/update-alternatives --install /usr/bin/shp2pgsql postgis-shp2pgsql %{pginstdir}/bin/shp2pgsql 930

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

%files
%defattr(-,root,root)
%doc COPYING CREDITS NEWS TODO README.%{sname} doc/html loader/README.* doc/%{sname}.xml doc/ZMSgeoms.txt
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis_comments.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis_upgrade*.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis_restore.pl
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/uninstall_postgis.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/*legacy*.sql
%attr(755,root,root) %{pginstdir}/lib/%{sname}-*.so
%{pginstdir}/share/extension/%{sname}-*.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/lib/liblwgeom*.so
%if %raster
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/raster_comments.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/*rtpostgis*.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/spatial*.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/topology*.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/uninstall_sfcgal.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/uninstall_topology.sql
%{pginstdir}/lib/rtpostgis-%{postgismajorversion}.so
%{pginstdir}/share/extension/%{sname}_topology-*.sql
%{pginstdir}/share/extension/%{sname}_topology.control
%{pginstdir}/share/extension/%{sname}_tiger_geocoder*.sql
%{pginstdir}/share/extension/%{sname}_tiger_geocoder.control
%endif

%files client
%defattr(644,root,root)
%attr(755,root,root) %{pginstdir}/bin/*

%files devel
%defattr(644,root,root)
%{_includedir}/liblwgeom.h
%{pginstdir}/lib/liblwgeom*.a
%{pginstdir}/lib/liblwgeom*.la

%if %utils
%files utils
%defattr(-,root,root)
%doc utils/README
%attr(755,root,root) %{_datadir}/%{name}/*.pl
%endif

%files docs
%defattr(-,root,root)
%doc %{sname}-%{version}.pdf

%changelog
* Sat Nov 9 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 2.1.1-1
- Update to 2.1.1

* Tue Sep 10 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 2.1.0-2
- Remove ruby bindings, per
  http://lists.osgeo.org/pipermail/postgis-devel/2013-August/023690.html
- Move extension related files under main package,
  per report from Daryl Herzmann

* Mon Sep 9 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 2.1.0-1
- Update to 2.1.0

* Fri Aug 9 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 2.1.0rc2
- Update to 2.1.0rc2
- Remove patch0, it is now in upstream.

* Wed Jul 31 2013 Davlet Panech <dpanech@ubitech.com> - 2.1.0beta3-2
- Fixed "provides postgis" to avoid self-conflicts
- BuildRequires: libxml2-devel

* Sun Jun 30 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 2.1.0beta3-1
- Update to 2.1.0 beta3
- Support multiple version installation 
- Split "client" tools into a separate subpackage, per
  http://wiki.pgrpms.org/ticket/108
- Bump up alternatives version.
- Add dependency for mysql-devel, since Fedora / EPEL gdal packages
  are built with MySQL support, too. (for now). This is needed for
  raster support.
- Push raster support into conditionals, so that we can use similar 
  spec files for RHEL and Fedora.
- Add a patch to get rid of dependency hell from gdal. Per 
  http://lists.osgeo.org/pipermail/postgis-devel/2013-June/023605.html
  and a tweet from Mike Toews.

* Thu Apr 11 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 2.0.3-2
- Provide postgis, to satisfy OS dependencies. Per #79.

* Thu Mar 14 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 2.0.3-1
- Update to 2.0.3 

* Mon Dec 10 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 2.0.2-1
- Update to 2.0.2.
- Update download URL.
- Add deps for JSON-C support.

* Wed Nov 07 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 2.0.1-2
- Add dependency to hdf5, per report from Guillaume Smet.

* Wed Jul 4 2012 Devrim GUNDUZ <devrim@gunduz.org> - 2.0.0-1
- Update to 2.0.1, for changes described at:
  http://postgis.org/news/20120622/

* Tue Apr 3 2012 Devrim GUNDUZ <devrim@gunduz.org> - 2.0.0-1
- Initial packaging with PostGIS 2.0.0.
- Drop java bits from spec file.
