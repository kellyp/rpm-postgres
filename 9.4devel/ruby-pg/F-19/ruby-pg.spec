%{!?ruby_sitearch: %define ruby_sitearch %(ruby -rrbconfig -e "puts Config::CONFIG['sitearchdir']")}

%global pgmajorversion 90
%global pginstdir /usr/pgsql-9.0
%global sname ruby-pg

Name:           %{sname}
Version:	0.9.0
Release:	1%{?dist}
Summary:	A Ruby interface for the PostgreSQL database engine
Group:		Development/Languages
License:	Ruby
URL: 		http://rubyforge.org/projects/ruby-pg
Source:		http://bitbucket.org/ged/%{sname}/downloads/pg-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  ruby >= 1.8.6 ruby-devel >= 1.8.6 postgresql%{pgmajorversion}-devel

Obsoletes:	ruby-postgres >= 0.7.1

%description
ruby-pg is a Ruby interface to the PostgreSQL Relational Database 
Management System. ruby-pg is a fork of the  unmaintained 
ruby-postgres project. ruby-pg is API-compatible (a drop-in 
replacement) with ruby-postgres.

%prep
%setup -q -n pg-%{version}
#chmod a-x sample/psql.rb

%build
ruby ext/extconf.rb --with-pg-config=%{pginstdir}/bin/pg_config --with-cflags="$RPM_OPT_FLAGS"

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} %{?_smp_mflags} install

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc BSD ChangeLog Contributors GPL LICENSE README README.ja README.OS_X README.windows 
%{ruby_sitearch}/pg_ext.so

%changelog
* Tue Oct 12 2010 Devrim GUNDUZ <devrim@gunduz.org> - 0.9.0-1
- Update to 0.9.0
- Apply 9.0 specific changes.

* Sat Aug 30 2008 Devrim GUNDUZ <devrim@gunduz.org> - 0.7.9.2008.08.17-1
- Update to 0.7.9.2008.08.17

* Tue Mar 18 2008 Devrim GUNDUZ <devrim@gunduz.org> - 0.7.9.2008.03.18-1
- Update to 0.7.9.2008.03.18

* Fri Mar 14 2008 Devrim GUNDUZ <devrim@gunduz.org> - 0.7.9.2008.02.05-1
- Initial build
