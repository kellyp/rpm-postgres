#Python major version.
%{expand: %%define pybasever %(python -c 'import sys;print(sys.version[0:3])')}
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: 	Bash tab completion for argparse
Name: 		python-argcomplete
Version: 	0.3.7
Release: 	1%{?dist}
License: 	LGPLv3
Group: 		Development/Libraries
Url: 		https://pypi.python.org/pypi/argcomplete
Source0: 	https://pypi.python.org/packages/source/a/argcomplete/argcomplete-%{version}.tar.gz
BuildRequires:  python-devel, python-setuptools
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
BuildArch: 	noarch
Requires:  	python-abi = %(%{__python} -c "import sys ; print sys.version[:3]")
Requires:  	python-argparse

%description
Argcomplete provides easy, extensible command line tab completion of 
arguments for your Python script.

It makes two assumptions:

 * You're using bash as your shell
 * You're using argparse to manage your command line arguments/options

Argcomplete is particularly useful if your program has lots of options 
or subparsers, and if your program can dynamically suggest completions 
for your argument/option values (for example, if the user is browsing 
resources over the network).

%prep
%setup -n argcomplete-%{version} -q

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.rst
%{python_sitelib}/argcomplete-%{version}-py%{pybasever}.egg-info/*
%{python_sitelib}/argcomplete/
%{_bindir}/activate-global-python-argcomplete
%{_bindir}/python-argcomplete-check-easy-install-script
%{_bindir}/register-python-argcomplete

%changelog
* Tue Feb 26 2013 - Devrim Gündüz <devrim@gunduz.org> 0.3.7-1
- Initial packaging for PostgreSQL RPM repository
