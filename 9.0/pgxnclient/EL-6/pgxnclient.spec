# Python major version.
%{expand: %%define pyver %(python -c 'import sys;print(sys.version[0:3])')}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary:	Command line tool designed to interact with the PostgreSQL Extension Network
Name:		pgxnclient
Version:	1.2.1
Release:	1%{?dist}
Source0:	http://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
License:	BSD
Group:		Applications/Databases
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Url:		http://pgxnclient.projects.postgresql.org/
BuildRequires:	python-devel python-setuptools

%description
The PGXN Client is a command line tool designed to interact with the 
PostgreSQL Extension Network allowing searching, compiling, installing and 
removing extensions in a PostgreSQL installation or database.

%prep
%setup -q -n %{name}-%{version}

%build
python setup.py build 

%install
rm -Rf %{buildroot}
mkdir -p %{buildroot}%{python_sitearch}/pgxnclient
mkdir -p %{buildroot}%{python_sitearch}/pgxnclient/tests
python setup.py install --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGES  COPYING docs/
%dir %{python_sitearch}/
%dir %{python_sitearch}/pgxnclient
%dir %{python_sitearch}/pgxnclient/tests
%{_bindir}/pgxn
%{_bindir}/pgxnclient
/usr/lib/python%{pyver}/site-packages/pgxnclient/*.py
/usr/lib/python%{pyver}/site-packages/pgxnclient/*.pyc
/usr/lib/python%{pyver}/site-packages/pgxnclient/*.pyo
/usr/lib/python%{pyver}/site-packages/pgxnclient/commands/*.py
/usr/lib/python%{pyver}/site-packages/pgxnclient/commands/*.pyc
/usr/lib/python%{pyver}/site-packages/pgxnclient/commands/*.pyo
/usr/lib/python%{pyver}/site-packages/pgxnclient/libexec/*
/usr/lib/python%{pyver}/site-packages/pgxnclient/tests/*.py
/usr/lib/python%{pyver}/site-packages/pgxnclient/tests/*.pyc
/usr/lib/python%{pyver}/site-packages/pgxnclient/tests/*.pyo
/usr/lib/python%{pyver}/site-packages/pgxnclient/utils/*.py
/usr/lib/python%{pyver}/site-packages/pgxnclient/utils/*.pyc
/usr/lib/python%{pyver}/site-packages/pgxnclient/utils/*.pyo
/usr/lib/python%{pyver}/site-packages/pgxnclient-%{version}-py%{pyver}.egg-info/*

%changelog
* Thu Sep 26 2013 Jeff Frost <jeff@pgexperts.com> 1.2.1-1
- Update to 1.2.1

* Mon Nov 28 2011 Devrim GUNDUZ <devrim@gunduz.org> 1.0-1
- Initial packaging for PostgreSQL RPM Repository
