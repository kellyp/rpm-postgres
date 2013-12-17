Summary:	Oracle to PostgreSQL database schema converter
Name:		ora2pg
Version:	12.0
Release:	1%{?dist}
Group:		Applications/Databases
License:	GPLv3+
URL:		http://ora2pg.darold.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

BuildRequires:	perl
Requires:	perl(DBD::Oracle) perl(DBI) perl(String::Random) perl(IO::Compress::Base)

%description
This package contains a Perl module and a companion script to convert an
Oracle database schema to PostgreSQL and to migrate the data from an
Oracle database to a PostgreSQL database.

%prep
%setup -q

%build
# Make Perl and Ora2Pg distrib files
%{__perl} Makefile.PL \
    INSTALLDIRS=vendor \
    QUIET=1 \
    CONFDIR=%{_sysconfdir} \
    DOCDIR=%{_docdir}/%{name}-%{version} \
    DESTDIR=%{buildroot}
%{__make}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}

%{__install} -D -m 0644 doc/%{name}.3 \
    %{buildroot}/%{_mandir}/man3/%{name}.3

# Remove unpackaged files.
rm -f `find %{buildroot}/%{_libdir}/perl*/ -name perllocal.pod -type f`
rm -f `find %{buildroot}/%{_libdir}/perl*/ -name .packlist -type f`

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%attr(0755,root,root) %{_bindir}/%{name}
%attr(0644,root,root) %{_mandir}/man3/%{name}.3.gz
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf.dist
%{perl_vendorlib}/Ora2Pg/PLSQL.pm
%{perl_vendorlib}/Ora2Pg.pm
%{_docdir}/%{name}/*

%changelog
* Wed Oct 23 2013 Devrim GUNDUZ <devrim@gunduz.org> 12.0-1
- Update to 12.0, per changes described at:
  http://www.postgresql.org/message-id/52664854.30200@dalibo.com

* Thu Sep 12 2013 Devrim GUNDUZ <devrim@gunduz.org> 11.4-1
- Update to 11.4

* Thu Sep 13 2012 Devrim GUNDUZ <devrim@gunduz.org> 9.2-1
- Update to 9.2
- Update URL, License, Group tags
- Fix spec per rpmlint warnings
- Apply some changes from upstream spec

* Fri Mar 20 2009 Devrim GUNDUZ <devrim@gunduz.org> 5.0-1
- Initial release, based on Peter's spec file.
