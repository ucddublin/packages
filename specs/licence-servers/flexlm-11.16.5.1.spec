%define tarball Linux_FLEXnet_Server

Name:           flexlm
Version:        11.16.5.1
Release:        1%{?dist}
Summary:        The FLEXlm licence manager

License:        Commercial
Group:          System Environment/Daemons
URL:            https://www.flexerasoftware.com
Source0:        %{tarball}_ver_%{version}.zip
Source1:        lmgrd@.service

Vendor:         OriginLab
Packager:       Tacaíocht Ríomhaireachta <tacaiocht.riomhaireachta@ucd.ie>

BuildArch:      i686

BuildRequires:  coreutils, sed, systemd, systemd-rpm-macros
Requires:       coreutils, redhat-lsb-core, shadow-utils, systemd

%description
This package installs the 32-bit FLEXlm licence manager daemon (lmgrd).

%prep
cd %{_builddir}
%{__rm} -rf %{tarball}_ver_%{version}
unzip %{SOURCE0}
if [ $? -ne 0 ]; then
  exit $?
fi
cd %{tarball}_ver_%{version}
%{__rm} -f _readme_.txt
%{__rm} -f fnp_LicAdmin.pdf
%{__rm} -f orglab
%{__cat} << 'EOF' > FLEXlm.conf
# Space-separated list of vendor daemons to start
# The licence and log files will be derived from these names
# NOTE: This file is no longer used since moving to systemd service management
FLEXLM_VENDORS=""
EOF
%{__cp} -a %{SOURCE1} ./

%install
%{__rm} -rf %{buildroot}
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/sysconfig
%{__mkdir} -p %{buildroot}/%{_unitdir}
%{__mkdir} -p %{buildroot}/%{_sharedstatedir}/FLEXlm/bin
%{__mkdir} -p %{buildroot}/%{_sharedstatedir}/FLEXlm/licences
%{__mkdir} -p %{buildroot}/%{_localstatedir}/log/FLEXlm
%{__install} -m 644 %{tarball}_ver_%{version}/FLEXlm.conf %{buildroot}/%{_sysconfdir}/sysconfig/FLEXlm
%{__install} -m 644 %{tarball}_ver_%{version}/lmgrd@.service %{buildroot}/%{_unitdir}/lmgrd@.service
%{__install} -m 755 %{tarball}_ver_%{version}/lmgrd %{buildroot}/%{_sharedstatedir}/FLEXlm/bin/
%{__install} -m 755 %{tarball}_ver_%{version}/lmutil %{buildroot}/%{_sharedstatedir}/FLEXlm/bin/

%clean
rm -rf %{buildroot}

%preun
if [ "$1" = "0" ]; then
    /usr/bin/systemctl stop lmgrd\@*.service > /dev/null 2>&1
fi

%files
%defattr(-,root,root,-)
%config %{_sysconfdir}/sysconfig/FLEXlm
%{_unitdir}/lmgrd@.service
%{_sharedstatedir}/FLEXlm/bin/lmgrd
%{_sharedstatedir}/FLEXlm/bin/lmutil
%dir %{_sharedstatedir}/FLEXlm/licences
%dir %{_localstatedir}/log/FLEXlm

%changelog
* Tue Feb 22 2022 Tacaíocht Ríomhaireachta <tacaiocht.riomhaireachta@ucd.ie> - 11.16.5.1
- Package lmgrd and lmutil for CentOS 7 and i686 architecture
