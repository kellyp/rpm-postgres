%global pgmajorversion 93
%global pginstdir /usr/pgsql-9.4devel
%global sname orafce

Summary:	Implementation of some Oracle functions into PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	3.0.4
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
Patch0:		orafce-makefile.patch
Patch1:		orafce.control.patch
URL:		http://pgfoundry.org/projects/orafce/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	postgresql%{pgmajorversion}-devel, openssl-devel, krb5-devel, bison, flex 
Requires:	postgresql%{pgmajorversion}

%description 	
The goal of this project is implementation some functions from Oracle database. 
Some date functions (next_day, last_day, trunc, round, ...) are implemented 
now. Functionality was verified on Oracle 10g and module is useful 
for production work.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0
%patch1 -p0

%build
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS

USE_PGXS=1 make %{?_smp_mflags} 

%install
rm -rf %{buildroot}
make USE_PGXS=1 %{?_smp_mflags} DESTDIR=%{buildroot} install

#install -d %{buildroot}%{_libdir}/pgsql/
#install -d %{buildroot}%{_datadir}/%{sname}/
#install -d %{buildroot}%{_docdir}/%{sname}/

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)

%{pginstdir}/lib/orafunc.so
%{pginstdir}/share/extension/orafce--3.0.sql
%{pginstdir}/share/extension/orafce--unpackaged--3.0.sql
%{pginstdir}/share/extension/orafce.control
%{pginstdir}/share/extension/orafunc.sql
%{pginstdir}/share/extension/uninstall_orafunc.sql
%{_docdir}/pgsql/extension/COPYRIGHT.orafunc
%{_docdir}/pgsql/extension/INSTALL.orafunc
%{_docdir}/pgsql/extension/README.orafunc

%changelog
* Thu Sep 13 2012 - Devrim GUNDUZ <devrim@gunduz.org> 3.0.4-1
- Update to 3.0.4

* Fri Oct 2 2009 - Devrim GUNDUZ <devrim@gunduz.org> 3.0.1-1
- Update to 3.0.1
- Remove patch0, it is in upstream now.
- Apply some 3.0 fixes to spec.

* Wed Aug 20 2008 - Devrim GUNDUZ <devrim@gunduz.org> 2.1.4-1
- Update to 2.1.4

* Sun Jan 20 2008 - Devrim GUNDUZ <devrim@gunduz.org> 2.1.3-2
- Spec file fixes, per bz review #251805

* Mon Jan 14 2008 - Devrim GUNDUZ <devrim@gunduz.org> 2.1.3-1
- Update to 2.1.3

* Fri Aug 10 2007 - Devrim GUNDUZ <devrim@gunduz.org> 2.1.1-1
- Update to 2.1.1
- Spec file cleanup

* Wed Aug 30 2006 - Devrim GUNDUZ <devrim@gunduz.org> 2.0.1-1
- Initial packaging
