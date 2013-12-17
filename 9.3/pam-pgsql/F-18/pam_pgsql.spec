%global pgmajorversion 93
%global pginstdir /usr/pgsql-9.3
%global sname pam_pgsql

Summary:	PAM module to authenticate using a PostgreSQL database 
Name:           %{sname}%{pgmajorversion}
Version:	0.7.3.1
Release:	1%{dist}
Source0:	http://downloads.sourceforge.net/%{sname}/%{sname}-%{version}.tar.gz

License:	GPLv2
URL:		http://sourceforge.net/projects/pam-pgsql/
Group:		System Environment/Base
BuildRequires:	postgresql%{pgmajorversion}-devel, pam-devel, mhash-devel
Requires:	postgresql%{pgmajorversion}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(post):	%{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives

Patch1:		pam-pgsql-getservice.patch

%description 
This module lets you authenticate users against a table in a 
PostgreSQL database. It also supports: 
- Checking account information (pam_acct_expired,new_authtok_reqd) 
- Updating auth to

%prep
%setup -q -n pam-pgsql-%{version}
%patch1 -p1

%build
%configure --with-postgresql=%{pginstdir}/bin/pg_config --prefix=%{pginstdir} --libdir=%{pginstdir}/lib/
make %{?_smp_mflags}

%install
%{__rm} -rf  %{buildroot}
make %{?_smp_mflags} DESTDIR=%{buildroot} install

%clean
%{__rm} -rf  %{buildroot}

%post
# Create alternatives entries for lib files
%{_sbindir}/update-alternatives --install /usr/lib/security/pam_pgsql.la pam-pgsql-la %{pginstdir}/lib/security/pam_pgsql.la 900
%{_sbindir}/update-alternatives --install /usr/lib/security/pam_pgsql.so pam-pgsql-so %{pginstdir}/lib/security/pam_pgsql.so 900

%preun
# Drop alternatives entries for lib files
%{_sbindir}/update-alternatives --remove pam-pgsql-so %{pginstdir}/lib/pam_pgsql.so
%{_sbindir}/update-alternatives --remove pam-pgsql-la %{pginstdir}/lib/pam_pgsql.la

%files
%defattr(-,root,root)
%doc %{pginstdir}/share/doc/pam-pgsql/*
%{pginstdir}/lib/security/pam_pgsql.la
%{pginstdir}/lib/security/pam_pgsql.so

%changelog
* Sun Sep 23 2012 Devrim Gunduz <devrim@gunduz.org> - 0.7.3.1-1
- Update to 0.7.3.1

* Tue Oct 12 2010 Devrim Gunduz <devrim@gunduz.org> - 0.7.1-1
- Update to 0.7.1-1
- Apply 9.0 specific changes.

* Sat Jun 14 2008 Devrim Gunduz <devrim@gunduz.org> - 0.6.4-1
- Update to 0.6.4-1

* Sun Feb 3 2008 Devrim Gunduz <devrim@gunduz.org> - 0.6.3-1
- Initial packaging for Fedora
