%global pgmajorversion 93
%global pginstdir /usr/pgsql-9.4devel
%global sname	plv8

Summary:	PostgreSQL procedural language powered by V8 JavaScript Engine
Name:		plv8_%{pgmajorversion}
Version:	1.4.1
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://plv8js.googlecode.com/files/%{sname}-%{version}.zip
Patch0:		plv8-makefile.patch
URL:		http://code.google.com/p/plv8js/wiki/PLV8
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	postgresql%{pgmajorversion}-devel, v8-devel
Requires:	postgresql%{pgmajorversion}, v8

%description
plv8 is a shared library that provides a PostgreSQL procedural language
powered by V8 JavaScript Engine. With this program you can write in JavaScript
your function that is callable from SQL.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
make %{?_smp_mflags} LPATH=`%{pginstdir}/bin/pg_config --pkglibdir` shlib="%{name}.so"

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} %{?_smp_mflags}
rm -f  %{buildroot}%{_datadir}/*.sql

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYRIGHT README Changes doc/plv8.md
%{pginstdir}/lib/plv8.so
%{pginstdir}/share/extension/plcoffee--%{version}.sql
%{pginstdir}/share/extension/plcoffee.control
%{pginstdir}/share/extension/plls--%{version}.sql
%{pginstdir}/share/extension/plls.control
%{pginstdir}/share/extension/plv8--%{version}.sql
%{pginstdir}/share/extension/plv8.control

%changelog
* Thu Dec 12 2013 Devrim Gündüz <devrim@gunduz.org> 1.4.1-1
- Initial spec file, per RH #1036130, after doing modifications
  to suit community RPM layout. Original work is by David
  Wheeler and Mikko Tiihonen
