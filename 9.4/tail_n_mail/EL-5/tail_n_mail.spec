Summary:	Check Log Files and Mail Related Parties
Name:		tail_n_mail
Version:	1.26.3
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://bucardo.org/downloads/%{name}
Source2:	README.tail_n_mail
URL:		http://bucardo.org/wiki/Tail_n_mail
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Buildarch:	noarch

%description
tail_n_mail (sometimes abbreviated TNM or tnm) is a Perl script for 
automatically detecting interesting items that appear in log files 
and mailing them out to interested parties. It is primarily aimed 
at Postgres log files but can be used for any files. It was developed 
at End Point Corporation by Greg Sabino Mullane. 

%prep
cp -p %{SOURCE0} %{name}.pl

%build

%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{_bindir}
install -d -m 755 %{buildroot}%{_docdir}/%{name}

install -m 755 %{name}.pl %{buildroot}%{_bindir}/%{name}.pl
ln -s %{_bindir}/%{name}.pl %{buildroot}/%{_bindir}/%{name}
install -m 644 %{SOURCE2} %{buildroot}%{_docdir}/%{name}/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%attr(755,root,root) %{_bindir}/%{name}*
%attr(644,root,root) %{_docdir}/%{name}/README.%{name}

%changelog
* Wed Dec 11 2013 - Devrim GUNDUZ <devrim@gunduz.org> 1.26.3-1
- Update to 1.26.3

* Thu Sep 6 2012 - Devrim GUNDUZ <devrim@gunduz.org> 1.26.1-1
- Update to 1.26.1

* Fri Jul 27 2012 - Devrim GUNDUZ <devrim@gunduz.org> 1.26.0-1
- Update to 1.26.0

* Mon Oct 03 2011 - Devrim GUNDUZ <devrim@gunduz.org> 1.20.3-1
- Update to 1.20.3

* Mon Jan 10 2011 - Devrim GUNDUZ <devrim@gunduz.org> 1.17-4-1
- Update to 1.17.4

* Sat Nov 13 2010 - Devrim GUNDUZ <devrim@gunduz.org> 1.17-2-1
- Update to 1.17.2

* Fri Sep 17 2010 - Devrim GUNDUZ <devrim@gunduz.org> 1.16.5-1
- Update to 1.16.5
- Apply a few stylistic fixes.
- Update download URL.

* Sat Sep 11 2010 - Devrim GUNDUZ <devrim@gunduz.org> 1.16.3-1
- Update to 1.16.3
- Update README.

* Sat May 15 2010 - Devrim GUNDUZ <devrim@gunduz.org> 1.10.3-1
- Update to 1.10.3

* Tue Apr 27 2010 - Devrim GUNDUZ <devrim@gunduz.org> 1.9.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
