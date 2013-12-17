#Python major version.
%{expand: %%define pybasever %(python -c 'import sys;print(sys.version[0:3])')}
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary:	htop like application for PostgreSQL server activity monitoring
Name:		pg_activity
Version:	0.2.0
Release:	1%{?dist}
License:	GPLv3
Group:		Applications/Databases
Url:		http://www.pgbarman.org/
Source0:	https://github.com/julmon/%{name}/archive/v%{version}.tar.gz
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
BuildArch:	noarch
Requires:	python > 2.6, python-psutil >= 0.4.1, python-psycopg2 > 2.2.1

%description
htop like application for PostgreSQL server activity monitoring.

%prep
%setup -n %{name}-%{version}

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%dir %{python_sitelib}/%{name}-%{version}-py%{pybasever}.egg-info/
%{_mandir}/man1/%{name}.1.gz
%{python_sitelib}/%{name}-%{version}-py%{pybasever}.egg-info/*


%changelog
* Thu Dec 20 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 0.2.0-1
- Initial packaging, based on the spec by Marco Neciarini
