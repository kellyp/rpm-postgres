Name:		MigrationWizard
Version:        1.1
Release:        2%{?dist}
Summary:	MySQL to PostgreSQL Migration Wizard

Group:		Application/Databases
License:	BSD
URL:		http://www.enterprisedb.com/
Source0:	http://files.pgrpms.org/%{name}-%{version}.tar.bz2
Patch0:		MigrationWizard-jdk-1.7.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:	noarch

BuildRequires:	ant
Requires:	java

%description
This is MySQL to PostgreSQL Migration Wizard by EnterpriseDB.

%prep
%setup -q -n wizard
%patch0 -p0

%build
ant compile

%install
rm -rf %{buildroot}
ant dist
install -d %{buildroot}%{_datadir}/%{name}
install -d %{buildroot}%{_datadir}/%{name}/lib
install -m 644 dist/*.jar %{buildroot}%{_datadir}/%{name}
install -m 644 dist/lib/* %{buildroot}%{_datadir}/%{name}/lib

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.jar
%{_datadir}/%{name}/lib/*

%changelog
* Thu Jan 10 2013 Devrim Gunduz <devrim@gunduz.org> 1.1-2
- Add a patch to compile on Fedora 17 (jdk 1.7)

* Wed Oct 28 2009 Devrim Gunduz <devrim@gunduz.org> 1.1-1
- Initial build for PostgreSQL RPM Repository
