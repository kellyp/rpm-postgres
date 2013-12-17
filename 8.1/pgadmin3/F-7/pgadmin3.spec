Summary:	Graphical client for PostgreSQL
Name:		pgadmin3
Version:	1.10.3
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source:		ftp://ftp.postgresql.org/pub/pgadmin3/release/v%{version}/src/%{name}-%{version}.tar.gz
Patch0:		%{name}-%{version}-optflags.patch
URL:		http://www.pgadmin.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	wxGTK-devel postgresql-devel desktop-file-utils openssl-devel libxml2-devel libxslt-devel
Requires:	wxGTK

%description
pgAdmin III is a powerful administration and development
platform for the PostgreSQL database, free for any use.
It is designed to answer the needs of all users,
from writing simple SQL queries to developing complex
databases. The graphical interface supports all PostgreSQL
features and makes administration easy.

pgAdmin III is designed to answer the needs of all users, 
from writing simple SQL queries to developing complex databases. 
The graphical interface supports all PostgreSQL features and 
makes administration easy. The application also includes a syntax 
highlighting SQL editor, a server-side code editor, an 
SQL/batch/shell job scheduling agent, support for the Slony-I 
replication engine and much more. No additional drivers are 
required to communicate with the database server.

%package docs
Summary:	Documentation for pgAdmin3
Group:		Applications/Databases
Requires:	%{name} = %{version}

%description docs
This package contains documentation for various languages,
which are in html format.

%prep
%setup -q -n %{name}-%{version}

# touch to avoid autotools re-run
for f in configure{,.ac} ; do touch -r $f $f.stamp ; done
%patch0 -p1
for f in configure{,.ac} ; do touch -r $f.stamp $f ; done

%build
export LIBS="-lwx_gtk2u_core-2.8"
%configure --disable-debug --disable-dependency-tracking --with-wx-version=2.8 --with-wx=/usr
make %{?_smp_mflags} all

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

cp -f ./pkg/debian/pgadmin3.xpm %{buildroot}/%{_datadir}/%{name}/%{name}.xpm

mkdir -p %{buildroot}/%{_datadir}/applications

desktop-file-install --vendor fedora --dir %{buildroot}/%{_datadir}/applications \
	--add-category X-Fedora\
	--add-category Application\
	--add-category Development\
	./pkg/%{name}.desktop


%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc BUGS CHANGELOG LICENSE README
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/applications/*

%files docs
%defattr(-,root,root)
%doc docs/*

%changelog
* Mon May 17 2010 Devrim GUNDUZ <devrim@gunduz.org> 1.10.3-1
- Update to 1.10.3

* Tue Mar 9 2010 Devrim GUNDUZ <devrim@gunduz.org> 1.10.2-1
- Update to 1.10.2

* Sat Dec 5 2009 Devrim GUNDUZ <devrim@gunduz.org> 1.10.1-1
- Update to 1.10.1     

* Mon Jun 29 2009 Devrim GUNDUZ <devrim@gunduz.org> 1.10.0
- Update to 1.10.0 Gold

* Wed Mar 25 2009 Devrim GUNDUZ <devrim@gunduz.org> 1.10.0-beta2
- Update to 1.10.0 beta2

* Fri Mar 13 2009 Devrim GUNDUZ <devrim@gunduz.org> 1.10.0-beta1
- Update to 1.10.0 beta1
- Update patch0

* Tue Jul 15 2008 Devrim GUNDUZ <devrim@gunduz.org> 1.8.4-2
- Use $RPM_OPT_FLAGS, build with dependency tracking disabled 
(#229054). Patch from Ville Skyttä

* Thu Jun 5 2008 Devrim GUNDUZ <devrim@gunduz.org> 1.8.4-1
- Update to 1.8.4

* Tue Jun 3 2008 Devrim GUNDUZ <devrim@gunduz.org> 1.8.3-1
- Update to 1.8.3

* Fri Feb 1 2008 Devrim GUNDUZ <devrim@gunduz.org> 1.8.2-1
- Update to 1.8.2

* Fri Jan 4 2008 Devrim GUNDUZ <devrim@gunduz.org> 1.8.1-1
- Update to 1.8.1

* Wed Dec 05 2007 Devrim GUNDUZ <devrim@gunduz.org> 1.8.0-2
- Rebuild for openssl bump

* Wed Nov 14 2007 Devrim GUNDUZ <devrim@gunduz.org> 1.8.0-1
- Update to 1.8.0
- Fix requires and buildrequires
- Improve description
- Added -docs subpackage
- add 2 new configure options, per upstream
- Fix path for xpm file

* Wed Apr 04 2007 Warren Togami <wtogami@redhat.com> - 1.6.3-1
- 1.6.3

* Thu Dec 28 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.6.1-2
- A couple of minor fixes to get things building in rawhide.

* Tue Dec 05 2006 Gavin Henry <ghenry@suretecsystems.com> - 1.6.1-1
- Update for 1.6.1. Now needs wxGTK 2.7+

* Mon Oct 09 2006 Gavin Henry <ghenry@suretecsystems.com> - 1.4.3-6
- Rebuild for FC6

* Tue Aug 29 2006 Gavin Henry <ghenry@suretecsystems.com> - 1.4.3-5
- Should have Developement and keeping this version one ahead for
  upgrading in FC-6

* Mon Aug 28 2006 Gavin Henry <ghenry@suretecsystems.com> - 1.4.3-3
- Moved icon to Devel and updated for FC-6

* Sat Jul 30 2006 Gavin Henry <ghenry@suretecsystems.com> - 1.4.3-2
- Removed gcc41 patch

* Sat Jul 29 2006 Gavin Henry <ghenry@suretecsystems.com> - 1.4.3-1
- Updated to latest 
- Sorry for delay

* Wed Feb 16 2006 Gavin Henry <ghenry@suretecsystems.com> - 1.4.1-2
- Applied Dennis' fixes according to Bug #181632

* Wed Feb 15 2006 Dennis Gilmore <dennis@ausil.us> - 1.4.1-1
- update to 1.4.1

* Thu Dec 8 2005 Gavin Henry <ghenry@suretecsystems.com> - 1.4.0-2
- Removed specific lib includes, not needed anymore 

* Wed Dec 7 2005 Gavin Henry <ghenry@suretecsystems.com> - 1.4.0-1
- Updated to latest release

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.0.2-5
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Thu Oct 07 2004 Nils O. Selåsdal <NOS|at|Utel.no> - 0:1.0.2-0.fdr.3
- include LICENCE.txt BUGS.txt README.txt
- Use master location in Source
- Don't --delete-original .desktop file.
* Thu Oct 07 2004 Nils O. Selåsdal <NOS|at|Utel.no> - 0:1.0.2-0.fdr.2
- Don't own _datadir/applications/
- Fedora -> fedora for .desktop file
- Use _smp_mflags for make
* Wed Oct 06 2004 Nils O. Selåsdal <NOS|at|Utel.no> - 0:1.0.2-0.fdr.1
- Initial RPM
