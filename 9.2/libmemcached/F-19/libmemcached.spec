Name:		libmemcached
Summary:	Client library and command line tools for memcached server
Version:	0.40
Release:	1%{?dist}
License:	BSD
Group:		System Environment/Libraries
URL:		http://libmemcached.org/
Source0:	http://launchpad.net/libmemcached/1.0/%{version}/+download/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# checked during configure (for test suite)
BuildRequires: memcached

%description
libmemcached is a C client library to the memcached server
(http://danga.com/memcached). It has been designed to be light on memory
usage, and provide full access to server side methods.

It also implements several command line tools:

memcat - Copy the value of a key to standard output.
memflush - Flush the contents of your servers.
memrm - Remove a key(s) from the server.
memstat - Dump the stats of your servers to standard output.
memslap - Generate testing loads on a memcached cluster.
memcp - Copy files to memcached servers.
memerror - Creates human readable messages from libmemcached error codes.


%package devel
Summary:	Header files and development libraries for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description devel
This package contains the header files and development libraries
for %{name}. If you like to develop programs using %{name}, 
you will need to install %{name}-devel.

%prep
%setup -q

%{__rm} -f libmemcached/hsieh_hash.c 

%{__mkdir} examples
%{__cp} -p tests/*.{c,cpp,h} examples/


%build
%configure
%{__make} %{_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__make} install  DESTDIR="%{buildroot}" AM_INSTALL_PROGRAM_FLAGS=""


%check
# For documentation only:
# test suite cannot run in mock (same port use for memcache servers on all arch)
# All tests completed successfully
# diff output.res output.cmp fails but result depend on server version
#%{__make} test


%clean
%{__rm} -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig
 

%files
%defattr (-,root,root,-) 
%doc AUTHORS COPYING README THANKS TODO ChangeLog
%{_bindir}/mem*
%exclude %{_libdir}/libmemcached.la
%exclude %{_libdir}/libmemcachedprotocol.la
%exclude %{_libdir}/libmemcachedutil.la
%exclude %{_libdir}/libhashkit.la
%{_libdir}/libhashkit.so.*
%{_libdir}/libmemcached.so.*
%{_libdir}/libmemcachedprotocol.so.*
%{_libdir}/libmemcachedutil.so.*
%{_mandir}/man1/mem*

%files devel
%defattr (-,root,root,-) 
%doc examples
%{_includedir}/libmemcached
%{_includedir}/libhashkit
%{_libdir}/libhashkit.so
%{_libdir}/libmemcached.so
%{_libdir}/libmemcachedprotocol.so
%{_libdir}/libmemcachedutil.so
%{_libdir}/pkgconfig/libmemcached.pc
%{_mandir}/man3/libmemcached*.3.gz
%{_mandir}/man3/memcached_*.3.gz
%{_mandir}/man3/hashkit*

%changelog
* Sat Jul 3 2010 Devrim GÜNDÜZ <devrim@gunduz.org> 0.40-1
- Initial packaging for PostgreSQL RPM Repository, to satisfy
  pgmemcached requirement.
