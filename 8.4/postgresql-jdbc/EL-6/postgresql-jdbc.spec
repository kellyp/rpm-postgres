# Conventions for PostgreSQL Global Development Group RPM releases:

# Official PostgreSQL Development Group RPMS have a PGDG after the release number.
# Integer releases are stable -- 0.1.x releases are Pre-releases, and x.y are
# test releases.

# Pre-releases are those that are built from CVS snapshots or pre-release
# tarballs from postgresql.org.  Official beta releases are not
# considered pre-releases, nor are release candidates, as their beta or
# release candidate status is reflected in the version of the tarball. Pre-
# releases' versions do not change -- the pre-release tarball of 7.0.3, for
# example, has the same tarball version as the final official release of 7.0.3:

# Major Contributors:
# ---------------
# Tom Lane
# Devrim Gunduz
# Peter Eisentraut

# This spec file and ancilliary files are licensed in accordance with
# The PostgreSQL license.
# In this file you can find the default build package list macros.  These can be overridden by defining
# on the rpm command line

%{!?gcj_support:%define gcj_support	1}
%{!?upstreamserver:%define upstreamver	8.4-703}
%global pgmajorversion 84
%global pginstdir /usr/pgsql-8.4
%global sname postgresql-jdbc

%global beta 0
%{?beta:%define __os_install_post /usr/lib/rpm/brp-compress}

Summary:	JDBC driver for PostgreSQL
Name:		postgresql%{pgmajorversion}-jdbc
Version:	8.4.703
Release:	1PGDG%{?dist}
Epoch:		0
License:	BSD
Group:		Applications/Databases
URL:		http://jdbc.postgresql.org/

Source0:	http://jdbc.postgresql.org/download/%{sname}-%{upstreamver}.src.tar.gz

Provides:	postgresql-jdbc

%if ! %{gcj_support}
BuildArch:	noarch
%endif
BuildRequires:  jpackage-utils >= 0:1.5
BuildRequires:  ant >= 0:1.6.2
BuildRequires:  ant-junit >= 0:1.6.2
BuildRequires:  junit >= 0:3.7
BuildRequires:	findutils gettext
%if %{gcj_support}
BuildRequires:	gcc-java
Requires(post):	/usr/bin/rebuild-gcj-db
Requires(postun):	/usr/bin/rebuild-gcj-db
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-jdbc package includes the .jar files needed for
Java programs to access a PostgreSQL database.

%prep
%setup -c -q
mv -f %{sname}-%{upstreamver}.src/* .
rm -f %{sname}-%{upstreamver}.src/.cvsignore
rmdir %{sname}-%{upstreamver}.src

# remove any binary libs
find -name "*.jar" -or -name "*.class" | xargs rm -f

%build
export OPT_JAR_LIST="ant/ant-junit junit"
export CLASSPATH=
sh update-translations.sh
ant

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_javadir}
# Per jpp conventions, jars have version-numbered names and we add
# versionless symlinks.
install -m 644 jars/postgresql.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar

pushd %{buildroot}%{_javadir}
ln -s %{name}-%{version}.jar %{name}.jar
# We are breaking  backwards compatibility here, and not adding symlinks anymore.
popd

%if %{gcj_support}
aot-compile-rpm
%endif

%clean
rm -rf %{buildroot}

%if %{gcj_support}
%post -p /usr/bin/rebuild-gcj-db
%postun -p /usr/bin/rebuild-gcj-db
%endif

%files
%defattr(-,root,root)
%doc LICENSE README doc/* 
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%{_libdir}/gcj/%{name}/*.jar.so
%{_libdir}/gcj/%{name}/*.jar.db
%endif

%changelog
* Mon Sep 19 2011 Devrim GÜNDÜZ <devrim@gunduz.org> 0:8.4.703-1PGDG
- Update to build 703

* Wed Dec 1 2010 Devrim Gunduz <devrim@gunduz.org> 0:8.4.702-1PGDG
- Initial packaging of build 702, for PostgreSQL 8.4 and RHEL/CentOS 6.
- Trim changelog
