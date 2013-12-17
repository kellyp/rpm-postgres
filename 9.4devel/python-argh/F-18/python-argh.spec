#Python major version.
%{expand: %%define pybasever %(python -c 'import sys;print(sys.version[0:3])')}
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: 	A simple argparse wrapper
Name: 		python-argh
Version: 	0.23.0
Release: 	1%{?dist}
License: 	LGPLv3
Group: 		Development/Libraries
Url: 		http://bitbucket.org/neithere/argh/
Source0: 	http://pypi.python.org/packages/source/a/argh/argh-%{version}.tar.gz
BuildRequires:  python-devel, python-setuptools
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
BuildArch: 	noarch
Requires:  	python-abi = %(%{__python} -c "import sys ; print sys.version[:3]")
Requires:  	python-argparse

%description
Agrh, argparse!
===============

Did you ever say "argh" trying to remember the details of optparse or argparse
API? If yes, this package may be useful for you. It provides a very simple
wrapper for argparse with support for hierarchical commands that can be bound
to modules or classes. Argparse can do it; argh makes it easy.

%prep
%setup -n argh-%{version} -q

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README
%{python_sitelib}/argh-%{version}-py%{pybasever}.egg-info/*
%{python_sitelib}/argh/

%changelog
* Tue Feb 26 2013 - Devrim Gündüz <devrim@gunduz.org> 0.23.0-1
- Update to version 0.23.0

* Wed May 9 2012 - Marco Neciarini <marco.nenciarini@2ndquadrant.it> 0.15.0-1
- Update to version 0.15.0

* Sat Dec 4 2011 - Marco Neciarini <marco.nenciarini@2ndquadrant.it> 0.14.2-1
- Initial packaging.
