Name:             openstack-glance
Version:          2012.1
Release:          5%{?dist}
Summary:          OpenStack Image Service

Group:            Applications/System
License:          ASL 2.0
URL:              http://glance.openstack.org
Source0:          http://launchpad.net/glance/essex/2012.1/+download/glance-%{version}.tar.gz
Source1:          openstack-glance-api.init
Source2:          openstack-glance-registry.init
Source3:          openstack-glance.logrotate
Source4:          openstack-glance-db-setup

#
# patches_base=2012.1
#
Patch0001: 0001-Ensure-swift-auth-URL-includes-trailing-slash.patch
Patch0002: 0002-search-for-logger-in-PATH.patch
Patch0003: 0003-Don-t-access-the-net-while-building-docs.patch

# EPEL specific
Patch100:         openstack-glance-newdeps.patch
Patch101:         crypto.random.patch

BuildArch:        noarch
BuildRequires:    python2-devel
BuildRequires:    python-setuptools
BuildRequires:    python-distutils-extra
BuildRequires:    intltool
# These are required to build due to the requirements check added
BuildRequires:    python-paste-deploy1.5
BuildRequires:    python-routes1.12
BuildRequires:    python-sqlalchemy0.7
BuildRequires:    python-webob1.0

Requires(post):   chkconfig
Requires(preun):  initscripts
Requires(preun):  chkconfig
Requires(pre):    shadow-utils
Requires:         python-glance = %{version}-%{release}

%description
OpenStack Image Service (code-named Glance) provides discovery, registration,
and delivery services for virtual disk images. The Image Service API server
provides a standard REST interface for querying information about virtual disk
images stored in a variety of back-end stores, including OpenStack Object
Storage. Clients can register new virtual disk images with the Image Service,
query for information on publicly available disk images, and use the Image
Service's client library for streaming virtual disk images.

This package contains the API and registry servers.

%package -n       python-glance
Summary:          Glance Python libraries
Group:            Applications/System

Requires:         MySQL-python
Requires:         pysendfile
Requires:         python-eventlet
Requires:         python-httplib2
Requires:         python-iso8601
Requires:         python-kombu
Requires:         python-migrate
Requires:         python-paste-deploy1.5
Requires:         python-routes1.12
Requires:         python-sqlalchemy0.7
Requires:         python-webob1.0
Requires:         python-setuptools
Requires:         python-crypto
Requires:         pyxattr

%description -n   python-glance
OpenStack Image Service (code-named Glance) provides discovery, registration,
and delivery services for virtual disk images.

This package contains the glance Python library.

%package doc
Summary:          Documentation for OpenStack Image Service
Group:            Documentation

Requires:         %{name} = %{version}-%{release}

BuildRequires:    python-sphinx10
BuildRequires:    graphviz

# Required to build module documents
BuildRequires:    python-boto
BuildRequires:    python-daemon
BuildRequires:    python-eventlet
BuildRequires:    python-gflags
BuildRequires:    python-routes1.12
BuildRequires:    python-sqlalchemy0.7
BuildRequires:    python-webob1.0

%description      doc
OpenStack Image Service (code-named Glance) provides discovery, registration,
and delivery services for virtual disk images.

This package contains documentation files for glance.

%prep
%setup -q -n glance-%{version}

%patch0001 -p1
%patch0002 -p1
%patch0003 -p1

%patch100 -p1
%patch101 -p1

sed -i 's|\(sql_connection = \)sqlite:///glance.sqlite|\1mysql://glance:glance@localhost/glance|' etc/glance-registry.conf

sed -i '/\/usr\/bin\/env python/d' glance/common/config.py glance/registry/db/migrate_repo/manage.py

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/tests

export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-1.0-build -b html source build/html
sphinx-1.0-build -b man source build/man

mkdir -p %{buildroot}%{_mandir}/man1
install -p -D -m 644 build/man/*.1 %{buildroot}%{_mandir}/man1/
popd

# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo
rm -f %{buildroot}%{_sysconfdir}/glance*.conf
rm -f %{buildroot}%{_sysconfdir}/glance*.ini
rm -f %{buildroot}%{_sysconfdir}/logging.cnf.sample
rm -f %{buildroot}%{_sysconfdir}/policy.json
rm -f %{buildroot}/usr/share/doc/glance/README.rst

# Setup directories
install -d -m 755 %{buildroot}%{_sharedstatedir}/glance/images

# Config file
install -p -D -m 644 etc/glance-api.conf %{buildroot}%{_sysconfdir}/glance/glance-api.conf
install -p -D -m 644 etc/glance-api-paste.ini %{buildroot}%{_sysconfdir}/glance/glance-api-paste.ini
# glance-registry.conf contains a db password
install -p -D -m 640 etc/glance-registry.conf %{buildroot}%{_sysconfdir}/glance/glance-registry.conf
install -p -D -m 644 etc/glance-registry-paste.ini %{buildroot}%{_sysconfdir}/glance/glance-registry-paste.ini
install -p -D -m 644 etc/glance-cache.conf %{buildroot}%{_sysconfdir}/glance/glance-cache.conf
install -p -D -m 644 etc/glance-cache-paste.ini %{buildroot}%{_sysconfdir}/glance/glance-cache-paste.ini
install -p -D -m 644 etc/glance-scrubber.conf %{buildroot}%{_sysconfdir}/glance/glance-scrubber.conf
install -p -D -m 644 etc/glance-scrubber-paste.ini %{buildroot}%{_sysconfdir}/glance/glance-scrubber-paste.ini
install -p -D -m 644 etc/policy.json %{buildroot}%{_sysconfdir}/glance/policy.json

# Initscripts
install -p -D -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/openstack-glance-api
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/openstack-glance-registry

# Logrotate config
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-glance

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/glance

# Install log directory
install -d -m 755 %{buildroot}%{_localstatedir}/log/glance

# Install database setup helper script.
install -p -D -m 755 %{SOURCE4} %{buildroot}%{_bindir}/openstack-glance-db-setup

%pre
getent group glance >/dev/null || groupadd -r glance -g 161
getent passwd glance >/dev/null || \
useradd -u 161 -r -g glance -d %{_sharedstatedir}/glance -s /sbin/nologin \
-c "OpenStack Glance Daemons" glance
exit 0

%post
/sbin/chkconfig --add openstack-glance-api
/sbin/chkconfig --add openstack-glance-registry

%preun
if [ $1 = 0 ] ; then
    /sbin/service openstack-glance-api stop >/dev/null 2>&1
    /sbin/chkconfig --del openstack-glance-api
    /sbin/service openstack-glance-registry stop >/dev/null 2>&1
    /sbin/chkconfig --del openstack-glance-registry
fi

%files
%doc README.rst
%{_bindir}/glance
%{_bindir}/glance-api
%{_bindir}/glance-control
%{_bindir}/glance-manage
%{_bindir}/glance-registry
%{_bindir}/glance-cache-cleaner
%{_bindir}/glance-cache-manage
%{_bindir}/glance-cache-prefetcher
%{_bindir}/glance-cache-pruner
%{_bindir}/glance-scrubber
%{_bindir}/openstack-glance-db-setup
%{_initrddir}/openstack-glance-api
%{_initrddir}/openstack-glance-registry
%{_mandir}/man1/glance*.1.gz
%dir %{_sysconfdir}/glance
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-api.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-api-paste.ini
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-registry.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-registry-paste.ini
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-cache.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-cache-paste.ini
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-scrubber.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-scrubber-paste.ini
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/policy.json
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/logrotate.d/openstack-glance
%dir %attr(0755, glance, nobody) %{_sharedstatedir}/glance
%dir %attr(0755, glance, nobody) %{_localstatedir}/log/glance
%dir %attr(0755, glance, nobody) %{_localstatedir}/run/glance

%files -n python-glance
%doc README.rst
%{python_sitelib}/glance
%{python_sitelib}/glance-%{version}-*.egg-info

%files doc
%doc doc/build/html

%changelog
* Wed Apr 25 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-5
- Use parallel installed versions of python-routes and python-paste-deploy

* Wed Apr 25 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-4
- Fix leak of swift objects on deletion

* Tue Apr 10 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-3
- Fix db setup script to correctly start mysqld

* Tue Apr 10 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-2
- Fix startup failure due to a file ownership issue (#811130)

* Mon Apr  9 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-1
- Update to Essex final

* Mon Feb 13 2012 Russell Bryant <rbryant@redhat.com> - 2011.3.1-3
- Add dependency on python-crypto. (rhbz#789943)

* Thu Jan 26 2012 Russell Bryant <rbryant@redhat.com> - 2011.3.1-2
- Add python-migrate dependency to python-glance (rhbz#784891)

* Fri Jan 20 2012 Pádraig Brady <P@draigBrady.com> - 2011.3.1-1
- Update to 2011.3.1 final

* Wed Jan 18 2012 Mark McLoughlin <markmc@redhat.com> - 2011.3.1-0.2.1063%{?dist}
- Update to latest 2011.3.1 release candidate

* Tue Jan 17 2012 Mark McLoughlin <markmc@redhat.com> - 2011.3.1-0.1.1062%{?dist}
- Update to 2011.3.1 release candidate
- Includes 6 new patches from upstream

* Fri Jan  6 2012 Pádraig Brady <P@draigBrady.com> - 2011.3-6
- Reapply patch to use parallel install versions of epel packages

* Fri Jan  6 2012 Mark McLoughlin <markmc@redhat.com> - 2011.3-5
- Rebase to latest upstream stable/diablo branch adding ~20 patches

* Tue Dec 20 2011 David Busby <oneiroi@fedoraproject.org> - 2011.3-4
- Depend on python-httplib2

* Tue Nov 22 2011 Pádraig Brady <P@draigBrady.com> - 2011.3-3
- Use updated parallel install versions of epel packages

* Tue Nov 22 2011 Pádraig Brady <P@draigBrady.com> - 2011.3-2
- Ensure the docs aren't built with the system glance module
- Ensure we don't access the net when building docs
- Depend on python-paste-deploy (#759512)

* Tue Sep 27 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-1
- Update to Diablo final

* Tue Sep  6 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-0.8.d4
- fix DB path in config
- add BR: intltool for distutils-extra

* Wed Aug 31 2011 Angus Salkeld <asalkeld@redhat.com> - 2011.3-0.7.d4
- Use the available man pages
- don't make service files executable
- delete unused files
- add BR: python-distutils-extra (#733610)

* Tue Aug 30 2011 Angus Salkeld <asalkeld@redhat.com> - 2011.3-0.6.d4
- Change from LSB scripts to systemd service files (#732689).

* Fri Aug 26 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-0.5.d4
- Update to diablo4 milestone
- Add logrotate config (#732691)

* Wed Aug 24 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-0.4.992bzr
- Update to latest upstream
- Use statically assigned uid:gid 161:161 (#732687)

* Mon Aug 22 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-0.3.987bzr
- Re-instate python2-devel BR (#731966)

* Mon Aug 22 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-0.2.987bzr
- Fix rpmlint warnings, reduce macro usage (#731966)

* Wed Aug 17 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-0.1.987bzr
- Update to latest upstream
- Require python-kombu for new notifiers support

* Mon Aug  8 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-0.1.967bzr
- Initial package from Alexander Sakhnov <asakhnov@mirantis.com>
  with cleanups by Mark McLoughlin
