%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

Name:             openstack-nova
Version:          2012.2
Release:          7%{?dist}
Summary:          OpenStack Compute (nova)

Group:            Applications/System
License:          ASL 2.0
URL:              http://openstack.org/projects/compute/
#Source0:          http://launchpad.net/nova/essex/2012.1/+download/nova-2012.1.tar.gz
Source0:          nova-2012.2.tar.gz
Source1:          nova.conf
Source6:          nova.logrotate

Source10:         openstack-nova-api.init
Source11:         openstack-nova-cert.init
Source12:         openstack-nova-compute.init
Source13:         openstack-nova-network.init
Source14:         openstack-nova-objectstore.init
Source15:         openstack-nova-scheduler.init
Source16:         openstack-nova-volume.init
Source17:         openstack-nova-direct-api.init
Source18:         openstack-nova-xvpvncproxy.init
Source19:         openstack-nova-console.init
Source24:         openstack-nova-consoleauth.init
Source25:         openstack-nova-metadata-api.init

Source20:         nova-sudoers
Source21:         nova-polkit.pkla
Source22:         nova-ifc-template

#
# patches_base=2012.1
#
#Patch0001: 0001-fix-bug-where-nova-ignores-glance-host-in-imageref.patch
#Patch0002: 0002-Stop-libvirt-test-from-deleting-instances-dir.patch
#Patch0003: 0003-Allow-unprivileged-RADOS-users-to-access-rbd-volumes.patch
#Patch0004: 0004-Fixed-bug-962840-added-a-test-case.patch
#Patch0005: 0005-Fix-errors-in-os-networks-extension.patch
#Patch0006: 0006-Create-compute.api.BaseAPI-for-compute-APIs-to-use.patch
#Patch0007: 0007-Populate-image-properties-with-project_id-again.patch
#Patch0008: 0008-Use-project_id-in-ec2.cloud._format_image.patch
#Patch0009: 0009-Implement-quotas-for-security-groups.patch
#Patch0010: 0010-Delete-fixed_ips-when-network-is-deleted.patch
#Patch0011: 0011-Xen-Pass-session-to-destroy_vdi.patch
#Patch0012: 0012-add-libvirt_inject_key-flag.patch
#Patch0013: 0013-Cloudpipe-tap-vpn-not-always-working.patch
#Patch0014: 0014-Don-t-leak-RPC-connections-on-timeouts-or-other-exce.patch
#Patch0015: 0015-Fixes-bug-987335.patch
#Patch0016: 0016-Fix-timeout-in-EC2-CloudController.create_image.patch
#Patch0017: 0017-Update-KillFilter-to-handle-deleted-exe-s.patch
#Patch0018: 0018-Get-unit-tests-functional-in-OS-X.patch
#Patch0019: 0019-Introduced-flag-base_dir_name.-Fixes-bug-973194.patch
#Patch0020: 0020-Fix-bug-983206-_try_convert-parsing-string.patch
#Patch0021: 0021-QuantumManager-will-start-dnsmasq-during-startup.-Fi.patch
#Patch0022: 0022-Fixes-bug-952176.patch
#Patch0023: 0023-Fix-nova.tests.test_nova_rootwrap-on-Fedora-17.patch
#Patch0024: 0024-ensure-atomic-manipulation-of-libvirt-disk-images.patch
#Patch0025: 0025-Ensure-we-don-t-access-the-net-when-building-docs.patch
#Patch0026: 0026-fix-useexisting-deprecation-warnings.patch
#Patch0027: 0027-support-a-configurable-libvirt-injection-partition.patch
#Patch0028: 0028-handle-updated-qemu-img-info-output.patch

# This is EPEL specific and not upstream
Patch100:         openstack-nova-newdeps.patch

BuildArch:        noarch
BuildRequires:    intltool
BuildRequires:    python-setuptools
BuildRequires:    python-distutils-extra >= 2.18
BuildRequires:    python-netaddr
BuildRequires:    python-lockfile
# These are required to build due to the requirements check added
BuildRequires:    python-paste-deploy1.5
BuildRequires:    python-routes1.12
BuildRequires:    python-sqlalchemy0.7
BuildRequires:    python-webob1.0

Requires:         python-nova = %{version}-%{release}

Requires:         python-paste
Requires:         python-paste-deploy1.5
Requires:         python-setuptools

Requires:         bridge-utils
# tunctl is needed where `ip tuntap` is not available
Requires:         tunctl
#TODO: Enable when available in RHEL 6.3
#Requires:         dnsmasq-utils
Requires:         libguestfs-mount >= 1.7.17
# The fuse dependency should be added to libguestfs-mount
Requires:         fuse
Requires:         libvirt-python
Requires:         libvirt >= 0.8.7
Requires:         libxml2-python
Requires:         python-cheetah
Requires:         MySQL-python

Requires:         euca2ools
Requires:         openssl
Requires:         sudo

Requires(post):   chkconfig
Requires(postun): initscripts
Requires(preun):  chkconfig
Requires(pre):    shadow-utils qemu-kvm

%description
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform. It gives you the
software, control panels, and APIs required to orchestrate a cloud,
including running instances, managing networks, and controlling access
through users and projects. OpenStack Compute strives to be both
hardware and hypervisor agnostic, currently supporting a variety of
standard hardware configurations and seven major hypervisors.

%package -n       python-nova
Summary:          Nova Python libraries
Group:            Applications/System

Requires:         vconfig
Requires:         PyXML
Requires:         curl
Requires:         m2crypto
Requires:         libvirt-python
Requires:         python-anyjson
Requires:         python-IPy
Requires:         python-boto
# TODO: make these messaging libs optional
Requires:         python-qpid
Requires:         python-carrot
Requires:         python-kombu
Requires:         python-amqplib
Requires:         python-daemon
Requires:         python-eventlet
Requires:         python-greenlet
Requires:         python-gflags
Requires:         python-iso8601
Requires:         python-lockfile
Requires:         python-lxml
Requires:         python-mox
Requires:         python-redis
Requires:         python-routes1.12
Requires:         python-sqlalchemy0.7
Requires:         python-tornado
Requires:         python-twisted-core
Requires:         python-twisted-web
Requires:         python-webob1.0
Requires:         python-netaddr
# TODO: remove the following dependency which is minimal
Requires:         python-glance
Requires:         python-novaclient
Requires:         python-paste-deploy1.5
Requires:         python-migrate
Requires:         python-ldap
Requires:         radvd
Requires:         iptables iptables-ipv6
Requires:         iscsi-initiator-utils
Requires:         scsi-target-utils
Requires:         lvm2
Requires:         coreutils

%description -n   python-nova
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform.

This package contains the nova Python library.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Compute
Group:            Documentation

Requires:         %{name} = %{version}-%{release}

BuildRequires:    python-sphinx10
BuildRequires:    graphviz
BuildRequires:    python-distutils-extra

BuildRequires:    python-nose
# Required to build module documents
BuildRequires:    python-IPy
BuildRequires:    python-boto
BuildRequires:    python-eventlet
BuildRequires:    python-gflags
BuildRequires:    python-tornado
BuildRequires:    python-twisted-core
BuildRequires:    python-twisted-web
# while not strictly required, quiets the build down when building docs.
BuildRequires:    python-carrot, python-mox, python-suds, m2crypto, bpython, python-memcached, python-migrate, python-iso8601

%description      doc
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform.

This package contains documentation files for nova.
%endif

%prep
%setup -q -n nova-%{version}

#%patch0001 -p1
#%patch0002 -p1
#%patch0003 -p1
#%patch0004 -p1
#%patch0005 -p1
#%patch0006 -p1
#%patch0007 -p1
#%patch0008 -p1
#%patch0009 -p1
#%patch0010 -p1
#%patch0011 -p1
#%patch0012 -p1
#%patch0013 -p1
#%patch0014 -p1
#%patch0015 -p1
#%patch0016 -p1
#%patch0017 -p1
#%patch0018 -p1
#%patch0019 -p1
#%patch0020 -p1
#%patch0021 -p1
#%patch0022 -p1
#%patch0023 -p1
#%patch0024 -p1
#%patch0025 -p1
#%patch0026 -p1
#%patch0027 -p1
#%patch0028 -p1

# Apply EPEL patch
%patch100 -p1

find . \( -name .gitignore -o -name .placeholder \) -delete

find nova -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# docs generation requires everything to be installed first
export PYTHONPATH="$( pwd ):$PYTHONPATH"

# TODO: possibly remove call to
# manually auto-generate to work around sphinx-build segfault
# This was not required on python-sphinx-1.0.7 at least
# but it's relatively quick at least
doc/generate_autodoc_index.sh

pushd doc

%if 0%{?with_doc}
SPHINX_DEBUG=1 sphinx-1.0-build -b html source build/html
# Fix hidden-file-or-dir warnings
rm -fr build/html/.doctrees build/html/.buildinfo
%endif

# Create dir link to avoid a sphinx-build exception
mkdir -p build/man/.doctrees/
ln -s .  build/man/.doctrees/man
SPHINX_DEBUG=1 sphinx-1.0-build -b man -c source source/man build/man
mkdir -p %{buildroot}%{_mandir}/man1
install -p -D -m 644 build/man/*.1 %{buildroot}%{_mandir}/man1/

popd

# Give stack, instance-usage-audit and clear_rabbit_queues a reasonable prefix
#mv %{buildroot}%{_bindir}/stack %{buildroot}%{_bindir}/nova-stack
#mv %{buildroot}%{_bindir}/instance-usage-audit %{buildroot}%{_bindir}/nova-instance-usage-audit
#mv %{buildroot}%{_bindir}/clear_rabbit_queues %{buildroot}%{_bindir}/nova-clear-rabbit-queues

# Setup directories
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/buckets
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/images
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/instances
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/keys
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/networks
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/tmp
install -d -m 755 %{buildroot}%{_localstatedir}/log/nova

# Setup ghost CA cert
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/CA
install -p -m 755 nova/CA/*.sh %{buildroot}%{_sharedstatedir}/nova/CA
install -p -m 644 nova/CA/openssl.cnf.tmpl %{buildroot}%{_sharedstatedir}/nova/CA
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/CA/{certs,crl,newcerts,projects,reqs}
touch %{buildroot}%{_sharedstatedir}/nova/CA/{cacert.pem,crl.pem,index.txt,openssl.cnf,serial}
install -d -m 750 %{buildroot}%{_sharedstatedir}/nova/CA/private
touch %{buildroot}%{_sharedstatedir}/nova/CA/private/cakey.pem

# Install config files
install -d -m 755 %{buildroot}%{_sysconfdir}/nova
install -p -D -m 640 %{SOURCE1} %{buildroot}%{_sysconfdir}/nova/nova.conf
install -p -D -m 640 etc/nova/api-paste.ini %{buildroot}%{_sysconfdir}/nova/api-paste.ini
install -p -D -m 640 etc/nova/policy.json %{buildroot}%{_sysconfdir}/nova/policy.json

# Install initscripts for Nova services
install -p -D -m 755 %{SOURCE10} %{buildroot}%{_initrddir}/openstack-nova-api
install -p -D -m 755 %{SOURCE11} %{buildroot}%{_initrddir}/openstack-nova-cert
install -p -D -m 755 %{SOURCE12} %{buildroot}%{_initrddir}/openstack-nova-compute
install -p -D -m 755 %{SOURCE13} %{buildroot}%{_initrddir}/openstack-nova-network
install -p -D -m 755 %{SOURCE14} %{buildroot}%{_initrddir}/openstack-nova-objectstore
install -p -D -m 755 %{SOURCE15} %{buildroot}%{_initrddir}/openstack-nova-scheduler
install -p -D -m 755 %{SOURCE16} %{buildroot}%{_initrddir}/openstack-nova-volume
install -p -D -m 755 %{SOURCE17} %{buildroot}%{_initrddir}/openstack-nova-direct-api
install -p -D -m 755 %{SOURCE18} %{buildroot}%{_initrddir}/openstack-nova-xvpvncproxy
install -p -D -m 755 %{SOURCE19} %{buildroot}%{_initrddir}/openstack-nova-console
install -p -D -m 755 %{SOURCE24} %{buildroot}%{_initrddir}/openstack-nova-consoleauth
install -p -D -m 755 %{SOURCE25} %{buildroot}%{_initrddir}/openstack-nova-metadata-api

# Install sudoers
install -p -D -m 440 %{SOURCE20} %{buildroot}%{_sysconfdir}/sudoers.d/nova

# Install logrotate
install -p -D -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-nova

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/nova

# Install template files
install -p -D -m 644 nova/auth/novarc.template %{buildroot}%{_datarootdir}/nova/novarc.template
install -p -D -m 644 nova/cloudpipe/client.ovpn.template %{buildroot}%{_datarootdir}/nova/client.ovpn.template
#install -p -D -m 644 nova/virt/libvirt.xml.template %{buildroot}%{_datarootdir}/nova/libvirt.xml.template
install -p -D -m 644 nova/virt/interfaces.template %{buildroot}%{_datarootdir}/nova/interfaces.template
install -p -D -m 644 %{SOURCE22} %{buildroot}%{_datarootdir}/nova/interfaces.template

install -d -m 755 %{buildroot}%{_sysconfdir}/polkit-1/localauthority/50-local.d
install -p -D -m 644 %{SOURCE21} %{buildroot}%{_sysconfdir}/polkit-1/localauthority/50-local.d/50-nova.pkla

# Remove unneeded in production stuff
rm -f %{buildroot}%{_bindir}/nova-debug
rm -fr %{buildroot}%{python_sitelib}/nova/tests/
rm -fr %{buildroot}%{python_sitelib}/run_tests.*
rm -f %{buildroot}%{_bindir}/nova-combined
rm -f %{buildroot}/usr/share/doc/nova/README*

%pre
getent group nova >/dev/null || groupadd -r nova --gid 162
if ! getent passwd nova >/dev/null; then
  useradd -u 162 -r -g nova -G nova,nobody,qemu -d %{_sharedstatedir}/nova -s /sbin/nologin -c "OpenStack Nova Daemons" nova
fi
# Add nova to the fuse group (if present) to support guestmount
if getent group fuse >/dev/null; then
  usermod -a -G fuse nova
fi
exit 0

%post
# Register the services
for svc in api cert compute network objectstore scheduler volume direct-api metadata-api console consoleauth xvpvncproxy; do
    /sbin/chkconfig --add openstack-nova-${svc}
done

%preun
if [ $1 -eq 0 ] ; then
    for svc in api cert compute network objectstore scheduler volume direct-api metadata-api console consoleauth xvpvncproxy; do
        /sbin/service openstack-nova-${svc} stop >/dev/null 2>&1
        /sbin/chkconfig --del openstack-nova-${svc}
    done
fi

%postun
if [ "$1" -ge 1 ] ; then
    for svc in api cert compute network objectstore scheduler volume direct-api metadata-api console consoleauth xvpvncproxy; do
        /sbin/service openstack-nova-${svc} condrestart > /dev/null 2>&1 || :
    done
fi

%files
%doc LICENSE
%dir %{_sysconfdir}/nova
%config(noreplace) %attr(-, root, nova) %{_sysconfdir}/nova/nova.conf
%config(noreplace) %attr(-, root, nova) %{_sysconfdir}/nova/api-paste.ini
%config(noreplace) %attr(-, root, nova) %{_sysconfdir}/nova/policy.json
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-nova
%config(noreplace) %{_sysconfdir}/sudoers.d/nova
%config(noreplace) %{_sysconfdir}/polkit-1/localauthority/50-local.d/50-nova.pkla

%dir %attr(0755, nova, root) %{_localstatedir}/log/nova
%dir %attr(0755, nova, root) %{_localstatedir}/run/nova

%{_bindir}/nova-*
%{_initrddir}/openstack-nova-*
%{_datarootdir}/nova
%{_mandir}/man1/nova*.1.gz

%defattr(-, nova, nova, -)
%dir %{_sharedstatedir}/nova
%dir %{_sharedstatedir}/nova/buckets
%dir %{_sharedstatedir}/nova/images
%dir %{_sharedstatedir}/nova/instances
%dir %{_sharedstatedir}/nova/keys
%dir %{_sharedstatedir}/nova/networks
%dir %{_sharedstatedir}/nova/tmp

%dir %{_sharedstatedir}/nova/CA/
%dir %{_sharedstatedir}/nova/CA/certs
%dir %{_sharedstatedir}/nova/CA/crl
%dir %{_sharedstatedir}/nova/CA/newcerts
%dir %{_sharedstatedir}/nova/CA/projects
%dir %{_sharedstatedir}/nova/CA/reqs
%{_sharedstatedir}/nova/CA/*.sh
%{_sharedstatedir}/nova/CA/openssl.cnf.tmpl
%ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sharedstatedir}/nova/CA/cacert.pem
%ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sharedstatedir}/nova/CA/crl.pem
%ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sharedstatedir}/nova/CA/index.txt
%ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sharedstatedir}/nova/CA/openssl.cnf
%ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sharedstatedir}/nova/CA/serial
%dir %attr(0750, -, -) %{_sharedstatedir}/nova/CA/private
%ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sharedstatedir}/nova/CA/private/cakey.pem

%files -n python-nova
%defattr(-,root,root,-)
%doc LICENSE
%{python_sitelib}/nova
%{python_sitelib}/nova-%{version}-*.egg-info

%if 0%{?with_doc}
%files doc
%doc LICENSE doc/build/html
%endif

%changelog
* Wed May 16 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-7
- Depend on tunctl which can be used when `ip tuntap` is unavailable
- Sync up with Essex stable branch
- Handle updated qemu-img info output
- Replace openstack-nova-db-setup with openstack-db

* Wed May 09 2012 Alan Pevec <apevec@redhat.com> - 2012.1-6
- Remove the socat dependency no longer needed by Essex

* Tue May 01 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-5
- Start the services later in the boot sequence

* Wed Apr 27 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-4
- Fix install issues with new Essex init scripts

* Wed Apr 25 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-3
- Use parallel installed versions of python-routes and python-paste-deploy

* Thu Apr 19 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-2
- Sync up with Essex stable branch
- Support more flexible guest image file injection
- Enforce quota on security group rules (#814275, CVE-2012-2101)
- Provide startup scripts for the Essex VNC services
- Provide a startup script for the separated metadata api service

* Fri Apr 13 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-1
- Update to Essex release

* Mon Apr 01 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-0.1.rc1
- Update to Essex release candidate 1

* Thu Mar 29 2012 Pádraig Brady <P@draigBrady.com> - 2011.3.1-8
- Remove the dependency on the not yet available dnsmasq-utils

* Thu Mar 29 2012 Russell Bryant <rbryant@redhat.com> - 2011.3.1-7
- CVE-2012-1585 - Long server names grow nova-api log files significantly
- Resolves: rhbz#808148

* Mon Mar  6 2012 Pádraig Brady <P@draigBrady.com> - 2011.3.1-5
- Require bridge-utils

* Mon Feb 13 2012 Pádraig Brady <P@draigBrady.com> - 2011.3.1-4
- Support --force_dhcp_release (#788485)

* Fri Jan 27 2012 Pádraig Brady <P@draigBrady.com> - 2011.3.1-3
- Suppress erroneous output to stdout on package install (#785115)

* Mon Jan 23 2012 Pádraig Brady <P@draigBrady.com> - 2011.3.1-2
- Fix a REST API v1.0 bug causing a regression with deltacloud

* Fri Jan 20 2012 Pádraig Brady <P@draigBrady.com> - 2011.3.1-1
- Update to 2011.3.1 release
- Allow empty mysql root password in mysql setup script
- Enable mysqld at boot in mysql setup script

* Wed Jan 18 2012 Mark McLoughlin <markmc@redhat.com> - 2011.3.1-0.4.10818%{?dist}
- Update to latest 2011.3.1 release candidate
- Re-add nova-{clear-rabbit-queues,instance-usage-audit}

* Tue Jan 17 2012 Mark McLoughlin <markmc@redhat.com> - 2011.3.1-0.3.10814
- nova-stack isn't missing after all

* Tue Jan 17 2012 Mark McLoughlin <markmc@redhat.com> - 2011.3.1-0.2.10814
- nova-{stack,clear-rabbit-queues,instance-usage-audit} temporarily removed because of lp#917676

* Tue Jan 17 2012 Mark McLoughlin <markmc@redhat.com> - 2011.3.1-0.1.10814
- Update to 2011.3.1 release candidate
- Only adds 4 patches from upstream which we didn't already have

* Wed Jan 11 2012 Pádraig Brady <P@draigBrady.com> - 2011.3-19
- Fix libguestfs support for specified partitions
- Fix tenant bypass by authenticated users using API (#772202, CVE-2012-0030)

* Fri Jan  6 2012 Mark McLoughlin <markmc@redhat.com> - 2011.3-18
- Fix up recent patches which don't apply

* Fri Jan  6 2012 Mark McLoughlin <markmc@redhat.com> - 2011.3-17
- Backport tgtadm off-by-one fix from upstream (#752709)

* Fri Jan  6 2012 Mark McLoughlin <markmc@redhat.com> - 2011.3-16
- Rebase to latest upstream stable/diablo, pulling in ~50 patches

* Fri Jan  6 2012 Mark McLoughlin <markmc@redhat.com> - 2011.3-15
- Move recent patches into git (no functional changes)

* Fri Dec 30 2011 Pádraig Brady <P@draigBrady.com> - 2011.3-14
- Don't require the fuse group (#770927)
- Require the fuse package (to avoid #767852)

* Tue Dec 14 2011 Pádraig Brady <P@draigBrady.com> - 2011.3-13
- Sanitize EC2 manifests and image tarballs (#767236, CVE 2011-4596)
- update libguestfs support

* Tue Dec 06 2011 Russell Bryant <rbryant@redhat.com> - 2011.3-11
- Add --yes, --rootpw, and --novapw options to openstack-nova-db-setup.

* Wed Nov 30 2011 Pádraig Brady <P@draigBrady.com> - 2011.3-10
- Use updated parallel install versions of epel packages
- Add libguestfs support

* Tue Nov 29 2011 Pádraig Brady <P@draigBrady.com> - 2011.3-9
- Update the libvirt dependency from 0.8.2 to 0.8.7
- Ensure we don't access the net when building docs

* Tue Nov 29 2011 Russell Bryant <rbryant@redhat.com> - 2011.3-8
- Change default database to mysql. (#735012)

* Mon Nov 14 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-8
- Add ~20 significant fixes from upstream stable branch

* Wed Oct 26 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-7
- Fix password leak in EC2 API (#749385, CVE 2011-4076)

* Mon Oct 24 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-5
- Fix block migration (#741690)

* Fri Oct 21 2011 David Busby <oneiroi@fedoraproject.org> 2011.3-5
- Changed requirement from python-sphinx, to python-sphinx10
- Switch back to SysV init for el6

* Mon Oct 17 2011 Bob Kukura <rkukura@redhat.com> - 2011.3-4
- Add dependency on python-amqplib (#746685)

* Wed Sep 28 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-3
- Fix lazy load exception with security groups (#741307)
- Fix issue with nova-network deleting the default route (#741686)
- Fix errors caused by MySQL connection pooling (#741312)

* Mon Sep 26 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-2
- Manage the package's patches in git; no functional changes.

* Thu Sep 22 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-1
- Update to Diablo final.
- Drop some upstreamed patches.
- Update the metadata-accept patch to what's proposed for essex.
- Switch rpc impl from carrot to kombu.

* Mon Sep 19 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-0.10.d4
- Use tgtadm instead of ietadm (#737046)

* Wed Sep 14 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-0.9.d4
- Remove python-libguestfs dependency (#738187)

* Mon Sep  5 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-0.8.d4
- Add iptables rule to allow EC2 metadata requests (#734347)

* Sat Sep  3 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-0.7.d4
- Add iptables rules to allow requests to dnsmasq (#734347)

* Wed Aug 31 2011 Angus Salkeld <asalkeld@redhat.com> - 2011.3-0.6.d4
- Add the one man page provided by nova.
- Start services with --flagfile rather than --flag-file (#735070)

* Tue Aug 30 2011 Angus Salkeld <asalkeld@redhat.com> - 2011.3-0.5.d4
- Switch from SysV init scripts to systemd units (#734345)

* Mon Aug 29 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-0.4.d4
- Don't generate root CA during %%post (#707199)
- The nobody group shouldn't own files in /var/lib/nova
- Add workaround for sphinx-build segfault

* Fri Aug 26 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-0.3.d4
- Update to diablo-4 milestone
- Use statically assigned uid:gid 162:162 (#732442)
- Collapse all sub-packages into openstack-nova; w/o upgrade path
- Reduce use of macros
- Rename stack to nova-stack
- Fix openssl.cnf.tmpl script-without-shebang rpmlint warning
- Really remove ajaxterm
- Mark polkit file as %%config

* Mon Aug 22 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-0.2.1449bzr
- Remove dependency on python-novaclient

* Wed Aug 17 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-0.1.1449bzr
- Update to latest upstream.
- nova-import-canonical-imagestore has been removed
- nova-clear-rabbit-queues was added

* Tue Aug  9 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-0.2.1409bzr
- Update to newer upstream
- nova-instancemonitor has been removed
- nova-instance-usage-audit added

* Tue Aug  9 2011 Mark McLoughlin <markmc@redhat.com> - 2011.3-0.1.bzr1130
- More cleanups
- Change release tag to reflect pre-release status

* Wed Jun 29 2011 Matt Domsch <mdomsch@fedoraproject.org> - 2011.3-1087.1
- Initial package from Alexander Sakhnov <asakhnov@mirantis.com>
  with cleanups by Matt Domsch
