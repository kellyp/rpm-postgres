Summary:	Break a PostgreSQL dump file into pre-data and post-data segments
Name:		split_postgres_dump
Version:	1.3.3
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://bucardo.org/downloads/%{name}
Source2:	README.%{name}
URL:		http://bucardo.org/wiki/Boxinfo
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Buildarch:	noarch

%description
split_postgres_dump is a small Perl script that breaks a --schema-only 
dump file into pre and post sections. The pre section contains everything 
needed to import the data, while the post section contains those actions 
that should be done after the data is loaded, namely the creation of 
indexes, constraints, and triggers. 

%prep

%build

%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{_bindir}
install -d -m 755 %{buildroot}%{_docdir}/%{name}

install -m 755 %{SOURCE0} %{buildroot}%{_bindir}/
install -m 644 %{SOURCE2} %{buildroot}%{_docdir}/%{name}/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%attr(755,root,root) %{_bindir}/%{name}
%attr(644,root,root) %{_docdir}/%{name}/README.%{name}

%changelog
* Mon Apr 8 2013 - Devrim GUNDUZ <devrim@gunduz.org> 1.3.3-1
- Initial RPM packaging for PostgreSQL RPM Repository
