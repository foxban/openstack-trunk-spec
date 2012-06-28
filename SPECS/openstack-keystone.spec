#
# This is 2012.1 essex release
#
%global release_name essex
%global release_letter rc
%global milestone 2
%global snapdate 20120404
%global git_revno r2201

%global snaptag ~%{release_letter}%{milestone}~%{snapdate}.%{git_revno}

Name:           openstack-keystone
Version:        2012.2
Release:        3%{?dist}
#Release:       0.1.%{release_letter}%{milestone}%{?dist}
Summary:        OpenStack Identity Service

License:        ASL 2.0
URL:            http://keystone.openstack.org/
#Source0:        http://launchpad.net/keystone/%{release_name}/%{version}/+download/keystone-%{version}.tar.gz
#Source0:        http://launchpad.net/keystone/%{release_name}/%{release_name}-%{milestone}/+download/keystone-%{version}~%{release_letter}%{milestone}.tar.gz
#Source0:        http://keystone.openstack.org/tarballs/keystone-%{version}%{snaptag}.tar.gz
Source0:        keystone-2012.2.tar.gz
Source1:        openstack-keystone.logrotate
Source2:        openstack-keystone.init
Source3:        openstack-keystone-db-setup
Source4:        openstack-config-set
Source5:        openstack-keystone-sample-data

Patch0:       openstack-keystone-newdeps.patch

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-sphinx10
BuildRequires:  python-iniparse
# These are required to build due to the requirements check added
BuildRequires:  python-sqlalchemy0.7
BuildRequires:  python-webob1.0
BuildRequires:  python-paste-deploy1.5
BuildRequires:  python-routes1.12

Requires:       python-keystone = %{version}-%{release}
Requires:       python-keystoneclient >= 2012.1-0.4.e4

Requires(post):   chkconfig
Requires(postun): initscripts
Requires(preun):  chkconfig
Requires(preun):  initscripts
Requires(pre):    shadow-utils

%description
Keystone is a Python implementation of the OpenStack
(http://www.openstack.org) identity service API.

This package contains the Keystone daemon.

%package -n       python-keystone
Summary:          Keystone Python libraries
Group:            Applications/System
# python-keystone added in 2012.1-0.2.e3
Conflicts:      openstack-keystone < 2012.1-0.2.e3

Requires:       python-crypto
Requires:       python-dateutil
Requires:       python-eventlet
Requires:       python-httplib2
Requires:       python-ldap
Requires:       python-lxml
Requires:       python-memcached
Requires:       python-migrate
Requires:       python-paste
Requires:       python-paste-deploy1.5
Requires:       python-paste-script
Requires:       python-prettytable
Requires:       python-routes1.12
Requires:       python-sqlalchemy0.7
Requires:       python-webob1.0
Requires:       python-passlib
Requires:       python-setuptools
Requires:       MySQL-python

%description -n   python-keystone
Keystone is a Python implementation of the OpenStack
(http://www.openstack.org) identity service API.

This package contains the Keystone Python library.

%prep
%setup -q -n keystone-%{version}
%patch0 -p1 -b .newdeps

# change default configuration
%{SOURCE4} etc/keystone.conf DEFAULT log_file %{_localstatedir}/log/keystone/keystone.log
%{SOURCE4} etc/keystone.conf sql connection mysql://keystone:keystone@localhost/keystone
%{SOURCE4} etc/keystone.conf catalog template_file %{_sysconfdir}/keystone/default_catalog.templates
%{SOURCE4} etc/keystone.conf catalog driver keystone.catalog.backends.sql.Catalog
%{SOURCE4} etc/keystone.conf identity driver keystone.identity.backends.sql.Identity
%{SOURCE4} etc/keystone.conf token driver keystone.token.backends.sql.Token
%{SOURCE4} etc/keystone.conf ec2 driver keystone.contrib.ec2.backends.sql.Ec2

find . \( -name .gitignore -o -name .placeholder \) -delete
find keystone -name \*.py -exec sed -i '/\/usr\/bin\/env python/d' {} \;

%build
%{__python} setup.py build

%install
%{__python} setup.py install --skip-build --root %{buildroot}

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/tests
rm -fr %{buildroot}%{python_sitelib}/run_tests.*

install -d -m 755 %{buildroot}%{_sysconfdir}/keystone
install -p -D -m 640 etc/keystone.conf %{buildroot}%{_sysconfdir}/keystone/keystone.conf
install -p -D -m 640 etc/default_catalog.templates %{buildroot}%{_sysconfdir}/keystone/default_catalog.templates
install -p -D -m 640 etc/policy.json %{buildroot}%{_sysconfdir}/keystone/policy.json
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-keystone
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/openstack-keystone
# Install database setup helper script.
install -p -D -m 755 %{SOURCE3} %{buildroot}%{_bindir}/openstack-keystone-db-setup
# Install sample data script.
install -p -D -m 755 tools/sample_data.sh %{buildroot}%{_datadir}/%{name}/sample_data.sh
install -p -D -m 755 %{SOURCE5} %{buildroot}%{_bindir}/openstack-keystone-sample-data

# Install configuration helper script.
install -p -D -m 755 %{SOURCE4} %{buildroot}%{_bindir}/openstack-config-set

install -d -m 755 %{buildroot}%{_sharedstatedir}/keystone
install -d -m 755 %{buildroot}%{_localstatedir}/log/keystone
install -d -m 755 %{buildroot}%{_localstatedir}/run/keystone

# docs generation requires everything to be installed first
export PYTHONPATH="$( pwd ):$PYTHONPATH"
make SPHINXAPIDOC=echo SPHINXBUILD=sphinx-1.0-build -C doc html
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo

%pre
getent group keystone >/dev/null || groupadd -r keystone
getent passwd keystone >/dev/null || \
useradd -r -g keystone -d %{_sharedstatedir}/keystone -s /sbin/nologin \
-c "OpenStack Keystone Daemons" keystone
exit 0

%post
if [ $1 -eq 1 ] ; then
    # Initial installation
%if 0%{?fedora} >= 15
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
%else
    /sbin/chkconfig --add openstack-keystone
%endif
fi

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
%if 0%{?fedora} >= 15
    /bin/systemctl --no-reload disable openstack-keystone.service > /dev/null 2>&1 || :
    /bin/systemctl stop openstack-keystone.service > /dev/null 2>&1 || :
%else
    /sbin/service openstack-keystone stop >/dev/null 2>&1
    /sbin/chkconfig --del openstack-keystone
%endif
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
%if 0%{?fedora} >= 15
    /bin/systemctl try-restart openstack-keystone.service >/dev/null 2>&1 || :
%else
    /sbin/service openstack-keystone condrestart >/dev/null 2>&1 || :
%endif
fi

%files
%doc LICENSE
%doc README.rst
%doc doc/build/html
%{_bindir}/keystone-all
%{_bindir}/keystone-manage
%{_bindir}/openstack-config-set
%{_bindir}/openstack-keystone-db-setup
%{_bindir}/openstack-keystone-sample-data
%{_datadir}/%{name}
%{_datadir}/%{name}/sample_data.sh
%{_initrddir}/openstack-keystone
%dir %{_sysconfdir}/keystone
%config(noreplace) %attr(-, root, keystone) %{_sysconfdir}/keystone/keystone.conf
%config(noreplace) %attr(-, root, keystone) %{_sysconfdir}/keystone/default_catalog.templates
%config(noreplace) %attr(-, keystone, keystone) %{_sysconfdir}/keystone/policy.json
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-keystone
%dir %attr(-, keystone, keystone) %{_sharedstatedir}/keystone
%dir %attr(-, keystone, keystone) %{_localstatedir}/log/keystone
%dir %attr(-, keystone, keystone) %{_localstatedir}/run/keystone

%files -n python-keystone
%defattr(-,root,root,-)
%doc LICENSE
%{python_sitelib}/keystone
%{python_sitelib}/keystone-%{version}-*.egg-info

%changelog
* Sun Apr 29 2012 Pádraig Brady <P@draigBrady.com> 2012.1-3
- Add the lookup for the parallel install of python-routes

* Thu Apr 26 2012 Pádraig Brady <P@draigBrady.com> 2012.1-2
- Use parallel installed versions of python-paste-deploy and python-routes

* Thu Apr 05 2012 Alan Pevec <apevec@redhat.com> 2012.1-1
- Essex release

* Wed Apr 04 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.13.rc2
- essex rc2

* Sat Mar 24 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.12.rc1
- update to final essex rc1

* Wed Mar 21 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.11.rc1
- essex rc1

* Thu Mar 08 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.10.e4
- change default catalog backend to sql rhbz#800704
- update sample-data script
- add missing keystoneclient dependency

* Thu Mar 01 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.9.e4
- essex-4 milestone
- change default database to mysql
- switch all backends to sql
- separate library to python-keystone

* Sun Dec 04 2011 Alan Pevec <apevec@redhat.com> 2011.3.1-4
- fix initscript for keystone

* Wed Nov 30 2011 Alan Pevec <apevec@redhat.com> 2011.3.1-3
- Use updated parallel install versions of epel packages (pbrady)
- Ensure the docs aren't built with the system glance module (pbrady)
- Ensure we don't access the net when building docs (pbrady)

* Thu Nov 24 2011 Alan Pevec <apevec@redhat.com> 2011.3.1-2
- include LICENSE, update package description from README.md

* Mon Nov 21 2011 Alan Pevec <apevec@redhat.com> 2011.3.1-1
- Update to 2011.3.1 stable/diablo release

* Fri Nov 11 2011 Alan Pevec <apevec@redhat.com> 2011.3-2
- Update to the latest stable/diablo snapshot

* Fri Oct 21 2011 David Busby <oneiroi@fedoraproject.com> - 2011.3-1
- Update to Diablo Final d3

* Wed Oct 19 2011 Matt Domsch <Matt_Domsch@dell.com> - 1.0-0.4.d4.1213
- add Requires: python-passlib

* Mon Oct 3 2011 Matt Domsch <Matt_Domsch@dell.com> - 1.0-0.2.d4.1213
- update to diablo release.
- BR systemd-units for _unitdir

* Fri Sep  2 2011 Mark McLoughlin <markmc@redhat.com> - 1.0-0.2.d4.1078
- Use upstream snapshot tarball
- No need to define python_sitelib anymore
- BR python2-devel
- Remove BRs only needed for unit tests
- No need to clean buildroot in install anymore
- Use slightly more canonical site for URL tag
- Prettify the requires tags
- Cherry-pick tools.tracer patch from upstream
- Add config file
- Add keystone user and group
- Ensure log file is in /var/log/keystone
- Ensure the sqlite db is in /var/lib/keystone
- Add logrotate support
- Add system units

* Thu Sep  1 2011 Matt Domsch <Matt_Domsch@dell.com> - 1.0-0.1.20110901git396f0bfd%{?dist}
- initial packaging
