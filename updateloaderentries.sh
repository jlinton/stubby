#!/bin/bash
# this utility should take the boot params from existing
# loader entries files (from anaconda+linux-kernel install)
# which should be a clone of the machine's /proc/cmdline
# and removes the "inst." options "BOOT_IMG="
# and then merges it with the /etc/kernel/cmdline
# which is generated from anaconda
#
# eventually it should probably also convert
# the root= option to UUID= via blkid?
#
# maybe some other choices as well

NEW_PARMS=$1

fixcmdline='
/^options/ {
  for (i=2;i<=NF;i++) {
    if ($i ~ /^BOOT_IMAGE/)
      continue;
    if ($i ~ /^inst\./)
      continue;
    options[$i] = "1"
  }
  # merge /etc/kernel/cmdline
  while (getline<"/etc/kernel/cmdline") {
    for (i=1;i<=NF;i++) {
        options[$i] = "1"
    }
  }
  printf "options    "
  for (i in options)
      printf "%s ",i
  printf "\n"
  next
}
{ print }
'

/usr/bin/awk -i inplace "$fixcmdline" /boot/efi/loader/entries/*

# just in case, relink if needed
if ! [[ -e /sbin/installkernel ]]; then
   /usr/bin/ln -s /usr/bin/kernel-install /sbin/installkernel
fi
