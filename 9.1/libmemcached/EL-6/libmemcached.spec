# Regression tests take a long time, you can skip 'em with this
%{!?runselftest: %{expand: %%global runselftest 0}}

Name:		libmemcached
Summary:	Client library and command line tools for memcached server
Version:	1.0.17
Release:	1%{?dist}
License:	BSD
Group:		System Environment/Libraries
URL:		http://libmemcached.org/
# Original sources:
#   http://launchpad.net/libmemcached/1.0/%{version}/+download/libmemcached-%{version}.tar.gz
# The source tarball must be repackaged to remove the Hsieh hash
# code, since the license is non-free.  When upgrading, download the new
# source tarball, and run "./strip-hsieh.sh <version>" to produce the
# "-exhsieh" tarball.
Source0:	libmemcached-%{version}-exhsieh.tar.gz

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	cyrus-sasl-devel
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	python-sphinx
BuildRequires:	memcached
BuildRequires:	libevent-devel

%description
libmemcached is a C/C++ client library and tools for the memcached server
(http://memcached.org/). It has been designed to be light on memory
usage, and provide full access to server side methods.

It also implements several command line tools:

memaslap    Load testing and benchmarking a server
memcapable  Checking a Memcached server capibilities and compatibility
memcat      Copy the value of a key to standard output
memcp       Copy data to a server
memdump     Dumping your server
memerror    Translate an error code to a string
memexist    Check for the existance of a key
memflush    Flush the contents of your servers
memparse    Parse an option string
memping     Test to see if a server is available.
memrm       Remove a key(s) from the server
memslap     Generate testing loads on a memcached cluster
memstat     Dump the stats of your servers to standard output
memtouch    Touches a key

%package devel
Summary: Header files and development libraries for %{name}
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig
Requires: cyrus-sasl-devel%{?_isa}

%description devel
This package contains the header files and development libraries
for %{name}. If you like to develop programs using %{name}, 
you will need to install %{name}-devel.

%prep
%setup -q

mkdir examples
cp -p tests/*.{cc,h} examples/

%build
# option --with-memcached=false to disable server binary check (as we don't run test)
%configure \
%if %{runselftest}
   --with-memcached=%{_bindir}/memcached \
%else
   --with-memcached=false \
%endif
   --enable-sasl \
   --enable-libmemcachedprotocol \
   --enable-memaslap \
   --enable-dtrace \
   --disable-static

%if 0%{?fedora} < 14 && 0%{?rhel} < 7
# for warning: unknown option after '#pragma GCC diagnostic' kind
sed -e 's/-Werror//' -i Makefile
%endif

make %{_smp_mflags} V=1


%install
rm -rf %{buildroot}
make install  DESTDIR="%{buildroot}" AM_INSTALL_PROGRAM_FLAGS=""

# Hack: when sphinx-build too old (fedora < 14 and rhel < 7)
# install upstream provided man pages
if [ ! -d %{buildroot}%{_mandir}/man1 ]; then
   install -d %{buildroot}%{_mandir}/man1
   install -p -m 644 man/*1 %{buildroot}%{_mandir}/man1
   install -d %{buildroot}%{_mandir}/man3
   install -p -m 644 man/*3 %{buildroot}%{_mandir}/man3
fi


%check
%if %{runselftest}
make test 2>&1 | tee rpmtests.log
# Ignore test result for memaslap (XFAIL but PASS)
# https://bugs.launchpad.net/libmemcached/+bug/1115357
if grep "XPASS: clients/memaslap" rpmtests.log && grep "1 of 21" rpmtests.log
then
  exit 0
else
  exit 1
fi
%endif


%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr (-,root,root,-) 
%doc AUTHORS COPYING README THANKS TODO ChangeLog
%{_bindir}/mem*
%exclude %{_libdir}/lib*.la
%{_libdir}/libhashkit.so.2*
%{_libdir}/libmemcached.so.11*
%{_libdir}/libmemcachedprotocol.so.0*
%{_libdir}/libmemcachedutil.so.2*
%{_mandir}/man1/mem*

%files devel
%defattr (-,root,root,-) 
%doc examples
%{_includedir}/libmemcached
%{_includedir}/libmemcached-1.0
%{_includedir}/libhashkit
%{_includedir}/libhashkit-1.0
%{_includedir}/libmemcachedprotocol-0.0
%{_includedir}/libmemcachedutil-1.0
%{_libdir}/libhashkit.so
%{_libdir}/libmemcached.so
%{_libdir}/libmemcachedprotocol.so
%{_libdir}/libmemcachedutil.so
%{_libdir}/pkgconfig/libmemcached.pc
%{_datadir}/aclocal/ax_libmemcached.m4
%{_mandir}/man3/libmemcached*
%{_mandir}/man3/libhashkit*
%{_mandir}/man3/memcached*
%{_mandir}/man3/hashkit*

%changelog
* Wed Nov 20 2013 Devrim GÜNDÜZ <devrim@gunduz.org> 1.0.17-1
- Initial packaging for PostgreSQL RPM Repository, to satisfy
  pgmemcached requirement.
