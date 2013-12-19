%global pgmajorversion 93
%global pginstdir /usr/pgsql-9.4devel

Name:           libpqxx
Epoch:          1
Version:        4.0.1
Release:        1%{?dist}
Summary:        C++ client API for PostgreSQL

Group:          System Environment/Libraries
License:        BSD
URL:            http://pqxx.org/
Source0:        http://pqxx.org/download/software/libpqxx/libpqxx-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch3:         libpqxx-2.6.8-multilib.patch

BuildRequires:  postgresql%{pgmajorversion}-devel
BuildRequires:  pkgconfig

%description
C++ client API for PostgreSQL. The standard front-end (in the sense of
"language binding") for writing C++ programs that use PostgreSQL.
Supersedes older libpq++ interface.

%package devel
Summary:        Development tools for %{name} 
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       pkgconfig
Requires:       postgresql%{pgmajorversion}-devel
%description devel
%{summary}.

%prep
%setup -q

# fix spurious permissions
chmod -x COPYING

%patch3 -p1 -b .multilib


%build
export PG_CONFIG=%{pginstdir}/bin/pg_config 
%configure --enable-shared --disable-static

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

rm -f %{buildroot}%{_libdir}/lib*.la

%check 
# not enabled, by default, takes awhile.
%{?_with_check:make check}

%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README VERSION
%{_libdir}/libpqxx-4.0.so

%files devel
%defattr(-,root,root,-)
%doc README-UPGRADE
%{_bindir}/pqxx-config
%{_includedir}/pqxx/
%{_libdir}/libpqxx.so
%{_libdir}/pkgconfig/libpqxx.pc

%changelog
* Mon Sep 16 2013 Devrim GÜNDÜZ <devrim@gunduz.org> 4.0.1-1
- Update to 4.0.1, per changes described at:
  http://pqxx.org/development/libpqxx/browser/tags/4.0.1/NEWS

* Fri Apr 6 2012 Devrim Gunduz <devrim@gunduz.org> 4.0-1
- Update to 4.0

* Fri Aug 12 2011 Devrim Gunduz <devrim@gunduz.org> 3.1-1
- Update to 3.1
- Sync with Fedora rawhide spec
- Trim changelog
