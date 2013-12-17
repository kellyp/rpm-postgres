%global postgismajorversion 2.0
%global pgmajorversion 91
%global pginstdir /usr/pgsql-9.1
%global sname	pgrouting

# Add Traveling Salesperson functionality
%{!?tsp_support:%define	tsp_support 1}
# Add Driving Distance functionality
%{!?dd_support:%define	dd_support 1}

Summary:	Routing functionality for PostGIS
Name:		%{sname}_%{pgmajorversion}
Version:	1.05
Release:	1%{dist}
License:	GPLv2
Group:		Applications/Databases
Source0:	http://download.osgeo.org/pgrouting/source/%{sname}-%{version}.tar.gz
Patch0:		pgrouting-cmake-pgconfig-path.patch
Patch1:		pgrouting-remove-createlang-quotes.patch
URL:		http://pgrouting.org/
BuildRequires:	gcc-c++, cmake
BuildRequires:	postgresql%{pgmajorversion}-devel, proj-devel, geos-devel
BuildRequires:	boost-devel >= 1.33
%if %{tsp_support}
BuildRequires:	gaul-devel
%endif
%if %{dd_support}
BuildRequires:	CGAL-devel
%endif
Requires:	postgis2_%{pgmajorversion} >= 2.0
Requires:	postgresql%{pgmajorversion}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Routing functionality for PostgreSQL/PostGIS system.

%prep

%setup -q -n %{sname}-%{version}
%patch0 -p0
%patch1 -p0

%build
install -d build
cd build
%cmake .. \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
%if %{tsp_support}
	-DWITH_TSP=ON \
%endif
	-DCMAKE_BUILD_TYPE=Release \
%if %{dd_support}
	-DWITH_DD=ON \
%endif
%if "%{_lib}" == "lib64"
	-DLIB_SUFFIX=64
%endif

%{__make}

%install
rm -rf %{buildroot}

%{__make} -C build install \
	DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.routing COPYING authors.txt  BOOST_LICENSE_1_0.txt RELEASE_NOTES
%attr(755,root,root) %{pginstdir}/lib/librouting.so
%if %{tsp_support}
%attr(755,root,root) %{pginstdir}/lib/librouting_tsp.so
%endif
%if %{dd_support}
%attr(755,root,root) %{pginstdir}/lib/librouting_dd.so
%endif
/usr/share/postlbs/matching.sql
/usr/share/postlbs/routing_*.sql

%changelog
* Mon Nov 12 2012 Devrim GÜNDÜZ <devrim@gunduz.org> 1.0.5-2
- Add the following features, sponsored by "Norsk institutt for skog og landskap":
 -- Add Traveling Salesperson functionality
 -- Add Driving Distance functionality
- Fix packaging issues, sponsored again by "Norsk institutt for skog og landskap".
- Update URL
- Add a new patch so that pgrouting can find PostgreSQL libs.
- Remove obsoleted patch (pgrouting-pg84.patch) -- already in upstream.
- Add a patch for 9.2, that removes quotes around LANGUAGE 'C'.

* Sat Sep 15 2012 Devrim GÜNDÜZ <devrim@gunduz.org> 1.0.5-1
- Update to 1.05

* Wed Jan 20 2010 Devrim GÜNDÜZ <devrim@gunduz.org> 1.0.3-5
- Initial import to PostgreSQL RPM repository, with very little cosmetic 
  changes Thanks Peter	for sending spec to me.

* Wed Dec 09 2009 Peter HOPFGARTNER <peter.hopfgartner@r3-gis.com> - 1.0.3-4
- New build for PostGIS 1.4.

* Tue May 05 2009 Peter HOPFGARTNER <peter.hopfgartner@r3-gis.com> - 1.0.3-3
- Adapted to CentOS 5.

