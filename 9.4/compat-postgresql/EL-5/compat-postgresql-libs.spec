# Conventions for PostgreSQL Global Development Group RPM releases:
#
# Official PostgreSQL Development Group RPMS have a PGDG after the release number.
# Integer releases are stable -- 0.1.x releases are Pre-releases, and x.y are
# test releases.
#
# Major Contributors:
# ---------------
# Devrim Gunduz

# This spec file and ancilliary files are licensed in accordance with
# The PostgreSQL license.

# In this file you can find the default build package list macros.  These can be overridden by
# defining on

# This macro is needed in order not to terminate build because of unpackaged files.
%global _unpackaged_files_terminate_build 0

# Some pre-defined values:
%global pgversion 8.4.3
%global libpqmajorversion 8.4
%global beta 0
%{?beta:%global __os_install_post /usr/lib/rpm/brp-compress}
%{!?kerbdir:%define kerbdir "/usr"}
%{!?test:%global test 1}
%{!?plpython:%global plpython 1}
%{!?pltcl:%global pltcl 1}
%{!?plperl:%global plperl 1}
%{!?ssl:%global ssl 1}
%{!?intdatetimes:%global intdatetimes 1}
%{!?kerberos:%global kerberos 1}
%{!?nls:%global nls 1}
%{!?xml:%global xml 1}
%{!?pam:%global pam 1}
%{!?disablepgfts:%global disablepgfts 0}
%{!?runselftest:%global runselftest 1}
%{!?uuid:%global uuid 1}
%{!?ldap:%global ldap 1}

Summary:	Compat layer for PostgreSQL client programs and libraries
Name:		compat-postgresql-libs
Version:	4
Release:	1PGDG%{dist}
License:	BSD
Group:		Applications/Databases
Url:		http://www.postgresql.org/
Source0:	ftp://ftp.postgresql.org/pub/source/v%{pgversion}/postgresql-%{pgversion}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This package provides compatibility libraries for PostgreSQL

%prep
%setup -q -n postgresql-%{pgversion}

%build

CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS
%if %kerberos
CPPFLAGS="${CPPFLAGS} -I%{_includedir}/et" ; export CPPFLAGS
CFLAGS="${CFLAGS} -I%{_includedir}/et" ; export CFLAGS
%endif

# Strip out -ffast-math from CFLAGS....

CFLAGS=`echo $CFLAGS|xargs -n 1|grep -v ffast-math|xargs -n 100`

# Use --as-needed to eliminate unnecessary link dependencies.
# Hopefully upstream will do this for itself in some future release.
LDFLAGS="-Wl,--as-needed"; export LDFLAGS

export LIBNAME=%{_lib}
%configure --disable-rpath \
%if %beta
	--enable-debug \
	--enable-cassert \
%endif
%if %plperl
	--with-perl \
%endif
%if %plpython
	--with-python \
%endif
%if %pltcl
	--with-tcl \
	--with-tclconfig=%{_libdir} \
%endif
%if %ssl
	--with-openssl \
%endif
%if %pam
	--with-pam \
%endif
%if %kerberos
	--with-krb5 \
	--with-gssapi \
	--with-includes=%{kerbdir}/include \
	--with-libraries=%{kerbdir}/%{_lib} \
%endif
%if %nls
	--enable-nls \
%endif
%if !%intdatetimes
	--disable-integer-datetimes \
%endif
%if %disablepgfts
	--disable-thread-safety \
%endif
%if %uuid
	--with-ossp-uuid \
%endif
%if %xml
	--with-libxml \
	--with-libxslt \
%endif
%if %ldap
	--with-ldap \
%endif
	--with-system-tzdata=%{_datadir}/zoneinfo \
	--sysconfdir=/etc/sysconfig/pgsql \
	--with-docdir=%{_docdir}

make %{?_smp_mflags} all

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
install -d %{buildroot}%{_libdir}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/libpq.so.*
%{_libdir}/libecpg.so*
%{_libdir}/libpgtypes.so.*
%{_libdir}/libecpg_compat.so.*

%changelog
* Wed May 5 2010 - Devrim GUNDUZ <devrim@gunduz.org> 4.1PGDG
- New spec file, which builds compat packages from PostgreSQL tarball.

