# NVidia Nano Node Platform

Contains the specific instructions and `ansible` scripts for the NVidia Nano Node Platform.

## Bootstrap Steps

1. Install [NVidia Nano OS version 4.6](https://developer.nvidia.com/embedded/jetpack-sdk-461)

# Hardware needed
 - nvidia nano
 - power supply
   - barrel - set the jumper next to barrel connector to use barrel power (see SageEdu instructions)
 - card reader
 - sdcard

# During the headless install to get `root` SSH access
- user: `waggle`
- passwd: `waggle` (come up with a better password later)
- partiion size set to 0 (or max) (leave blank)
- eth0 as primary
- we will change hostname later, so just use localhost for now
- use default nvpmodel (MAXN) (10W) - we may be able to set this with ansible later
  - there are only 2 modes.  the maxn is mode 0001
- wait for system reboot
- serial back in, and setup ssh access for the `root` user
  - get IP for eth0
  - set root user password (`passwd`) - `waggle` for now
  - enable root user ssh login
    sed -i 's/^#\?PasswordAuthentication .*$/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/^#\?PermitRootLogin .*$/PermitRootLogin yes/' /etc/ssh/sshd_config
    service sshd restart
- login via `ssh root@<ip>` with the `waggle` password

# Setup the extra drive
- insert drive
- should enumerate as /dev/sdb1
- setup a SWAP 16GB
- setup a rw for the `/` overlay
- setup a the /media/plugin-data drive (the rest of the drive)
  # clear the current partition table, create GPT table
  fdisk --wipe always --wipe-partitions always /dev/sdb
  g
  w
  # make the swap partition (16GB SWAP)
  fdisk --wipe always --wipe-partitions always /dev/sdb
  n
  ""
  ""
  +16G
  t
  19
  w
  # make the overlayfs (16GB)
  fdisk --wipe always --wipe-partitions always /dev/sdb
  n
  ""
  ""
  +16G
  w
  # make the plugin-data (* the rest of the space)
  fdisk --wipe always --wipe-partitions always /dev/sdb
  n
  ""
  ""
  ""
  w

  # turn on the swap
  ## format the swap
  root@localhost:~# mkswap /dev/sdb1 -L ext-swap
Setting up swapspace version 1, size = 16 GiB (17179865088 bytes)
LABEL=ext-swap, UUID=6863907e-fe44-4d50-956b-cdc98490a059
  ## put the swap in the startup partition file
echo "/dev/sdb1 swap swap defaults,nofail 0 0" >> /etc/fstab

  # setup the overlayfs partition
    mkfs.ext4 /dev/sdb2
    e2label /dev/sdb2 system-data
echo "${PLUGIN_DEVICE} ${NVME_PART_MOUNT_PLUGIN} ext4 defaults,nofail,x-systemd.after=local-fs-pre.target,x-systemd.before=local-fs.target 0 2" >> /etc/fstab
  ## NOTE we will actually enable the overlayfs at the very end

  # set the default mount of /media/plugin-data in the /etc/fstab
    mkfs.ext4 /dev/sdb3
    e2label /dev/sdb3 plugin-data
    echo "/dev/sdb3 /media/plugin-data ext4 defaults,nofail,x-systemd.after=local-fs-pre.target,x-systemd.before=local-fs.target 0 2" >> /etc/fstab

**LEFT OFF HERE; next time**
- set network interfaces (`wan0`) & NetworkManager
  - udev rules, /etc/waggle/config.ini
- install docker (use the external media)
- install k3s (use the external media)
- minimal config (node ID, VSN, kubernetes config) and try to 

# NX Walk-through, what do we need
- # skip l4t depends, assume its all there
- apt-get update
- python2.7 and python3.6 (click, pip, etc.)
- install docker and its required apt-packages
- install k3s
  - we need to be sure our symlinks for k3s storage are set to the external drive


TODO items to add to our steps
- create /var/lib/nvpmodel/status file to set the default operating mode and fmode (fan mode) to `cool`
  - it seems that `cool` is not allowed.  so need to figure out what fan modes ARE supported, if any
- figure out if we want to allowe `root` user to be able to login with ssh with password or not??
  