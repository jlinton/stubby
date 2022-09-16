# A place to drop systemd-boot shimming utilities that don't yet have
# a better place to live. The name is a play on the grubby package
# which performs a similar function for grub2.

Name: stubby
Version: 1.0
Release: 1%{?dist}
Summary: Set of systemd-boot utilities that don't fit anywhere else in the distro.
License: GPLv2+
Source1: updateloaderentries.sh
Source2: COPYING
Source3: entries.srel

Requires: findutils
Requires: util-linux
Requires: systemd-udev
Requires: gawk
Requires: coreutils

ExcludeArch: %{ix86}
Conflicts:	uboot-tools < 2021.01-0.1.rc2
Conflicts:	grubby
Obsoletes:	%{name}-bls < %{version}-%{release}

%description
This package provides a place to drop systemd-boot shimming
utilities that don't yet have a better place to live. The name
is a play on the grubby package which performs a similar function
for grub2.

%prep
# Make sure the license can be found in mock
cp %{SOURCE2} . || true

%build

%install

mkdir -p %{buildroot}%{_sbindir}/
install -T -m 0755 %{SOURCE1} %{buildroot}%{_sbindir}/updateloaderentries.sh
install --directory %{buildroot}/boot/efi/loader/entries
install -T -m 444 %{SOURCE3} %{buildroot}/boot/efi/loader/entries.srel
# should we create /boot/efi/loader/loader.conf here?
# 

%pre
#create /boot/efi/loader/XXXX where XXXX is /etc/machine-id?

%post
/usr/bin/ln -s /usr/bin/kernel-install %{_sbindir}installkernel
# could do a bootctl install here too?

%files
%license COPYING
%attr(0755,root,root) %{_sbindir}/updateloaderentries.sh
%attr(0700,root,root) /boot/efi/loader/entries
%attr(0444,root,root) /boot/efi/loader/entries.srel

%changelog
* Sep 9 2022 Jeremy Linton <jlinton@arm.com> - 1.0
- Create package as a grubby alternative on systemd-boot systems

