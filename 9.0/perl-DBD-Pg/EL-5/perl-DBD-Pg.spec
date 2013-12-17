%global pgmajorversion 90
%global pginstdir /usr/pgsql-9.0

Name:           perl-DBD-Pg
Summary:        A PostgreSQL interface for perl
Version:        2.17.2
Release:        1%{?dist}
License:        GPLv2+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/T/TU/TURNSTEP/DBD-Pg-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/DBD-Pg/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# Prevent bug #443495
BuildRequires:  perl(DBI) >= 1.607
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More) >= 0.61
BuildRequires:  perl(version)
BuildRequires:  postgresql%{pgmajorversion}-devel
BuildRequires:  perl(Test::Simple), postgresql%{pgmajorversion}-server

Requires:       perl(DBI) >= 1.52
Requires:       perl(version)

# Missed by the find provides script:
Provides:       perl(DBD::Pg) = %{version}

%{?perl_default_filter}
%{?perl_default_subpackage_tests}

%description
An implementation of DBI for PostgreSQL for Perl.


%prep
%setup -q -n DBD-Pg-%{version}

%build
POSTGRES_HOME=%{pginstdir} %{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w %{buildroot}/*

%check
# Full test coverage requires a live PostgreSQL database (see the README file)
#export DBI_DSN=dbi:Pg:dbname=<database>
#export DBI_USER=<username>
#export DBI_PASS=<password>
# If variables undefined, package test will create it's own database. All
# tests pass then if LC_ALL=C. Otherwise
# <https://rt.cpan.org/Public/Bug/Display.html?id=56705> appears.
LC_ALL=C make test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README README.dev TODO
%{perl_vendorarch}/DBD/
%{perl_vendorarch}/auto/DBD/
%{perl_vendorarch}/Bundle/DBD/Pg.pm
%{_mandir}/man3/*.3*

%changelog
* Thu Jan 6 2011 Devrim Gündüz <devrim@gunduz.org> 2.17.2-1
- Initial packaging for PostgreSQL RPM Repository, based on Fedora spec.
  Applied only 9.0 specific layout changes.

