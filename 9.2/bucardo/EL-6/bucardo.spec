%global pgmajorversion 92

%define         realname Bucardo
Name:           bucardo
Version:        4.5.0
Release:        1%{?dist}
Summary:        Postgres replication system for both multi-master and multi-slave operations

Group:          Applications/Databases
License:        BSD
URL:            http://bucardo.org/
Source0:        http://bucardo.org/downloads/Bucardo-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source1: master-master-replication-example.txt

BuildArch:     noarch

BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(DBI)
BuildRequires:  perl(DBD::Pg)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(Sys::Hostname)
BuildRequires:  perl(Sys::Syslog)
BuildRequires:  perl(Net::SMTP)
# available from fedora 10
BuildRequires:  perl(DBIx::Safe)

Requires:  perl(ExtUtils::MakeMaker)
Requires:  postgresql%{pgmajorversion}-plperl

Requires:  perl(DBI)
Requires:  perl(DBD::Pg)
Requires:  perl(DBIx::Safe)
Requires:  perl(IO::Handle)
Requires:  perl(Sys::Hostname)
Requires:  perl(Sys::Syslog)
Requires:  perl(Net::SMTP)

#testsuite
Requires:  perl(Test::Simple)
Requires:  perl(Test::Harness)

%description
Bucardo is an asynchronous PostgreSQL replication system, allowing for both
multi-master and multi-slave operations.It was developed at Backcountry.com
primarily by Greg Sabino Mullane of End Point Corporation.

%prep
%setup -q -n %{realname}-%{version}

%build

%{__perl} Makefile.PL INSTALLDIRS=vendor

make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} +
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

sed -i -e '1d;2i#!/usr/bin/perl' bucardo_ctl

rm -f %{buildroot}/%{_bindir}/bucardo_ctl
install -Dp -m 755 bucardo_ctl %{buildroot}/%{_sbindir}/bucardo_ctl
mkdir -p %{buildroot}/%{_localstatedir}/run/bucardo

install -Dp -m 644 %{SOURCE1} .

%{_fixperms} %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc bucardo_ctl.html Bucardo.pm.html Changes
%doc INSTALL LICENSE README SIGNATURE TODO
%doc master-master-replication-example.txt
%{perl_vendorlib}/*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_sbindir}/bucardo_ctl
%{_datadir}/bucardo/bucardo.schema
%dir %{_localstatedir}/run/bucardo

%changelog
* Thu Sep 6 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 4.5.0-1
- Update to 4.5.0

* Sat Apr 7 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 4.4.8-1
- Update to 4.4.8

* Tue Sep 27 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 4.4.6-2
- Fix PostgreSQL major number version. Per report from Phil Sorber .

* Tue Aug 9 2011 Devrim GUNDUZ <devrim@gunduz.org> - 4.4.6-1
- Update to 4.4.6

* Mon Apr 18 2011 Devrim GUNDUZ <devrim@gunduz.org> - 4.4.3-1
- Update to 4.4.3

* Thu Jan 6 2011 Devrim GUNDUZ <devrim@gunduz.org> - 4.4.0-3
- Add 9.0 dependency.

* Fri Mar 12 2010 Devrim GUNDUZ <devrim@gunduz.org> - 4.4.0-2
- Sync with Fedora spec again.
