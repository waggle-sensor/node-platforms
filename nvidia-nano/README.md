# NVidia Nano Node Platform

Contains the specific instructions and `ansible` scripts for the NVidia Nano Node Platform.

## Hardware needed
 - nvidia nano
 - power supply
   - barrel - set the jumper next to barrel connector to use barrel power (see SageEdu instructions)
 - card reader
 - sdcard

### Special Setup Instructions
- the node can NOT have an IP on the ethernet in the 10.42.0.0 IP space as k3s internal network uses that subnet.  it breaks stuff.

## Bootstrap Steps
1. Install [NVidia Nano OS version 4.6](https://developer.nvidia.com/embedded/jetpack-sdk-461)


### During the headless install to get `root` SSH access
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

### Setup the extra drive
- insert drive
- should enumerate as /dev/sda1
- setup a SWAP 16GB
- setup a rw for the `/` overlay
- setup a the /media/plugin-data drive (the rest of the drive)

**clear the current partition table, create GPT table**
  ```
  fdisk --wipe always --wipe-partitions always /dev/sda
  g
  w
  ```
  **make the swap partition (16GB SWAP)**
  ```
  fdisk --wipe always --wipe-partitions always /dev/sda
  n
  ""
  ""
  +16G
  t
  19
  w
  ```

  **make the overlayfs (16GB)**
  ```
  fdisk --wipe always --wipe-partitions always /dev/sda
  n
  ""
  ""
  +16G
  w
  ```
  
  **make the plugin-data (* the rest of the space)**
  ```
  fdisk --wipe always --wipe-partitions always /dev/sda
  n
  ""
  ""
  ""
  w
```

**turn on the swap**
format the swap
```
  root@localhost:~# mkswap /dev/sda1 -L ext-swap
Setting up swapspace version 1, size = 16 GiB (17179865088 bytes)
LABEL=ext-swap, UUID=6863907e-fe44-4d50-956b-cdc98490a059
```

**put the swap in the startup partition file**
```
echo "/dev/sda1 swap swap defaults,nofail 0 0" >> /etc/fstab
```

**setup the overlayfs partition**
```
    mkfs.ext4 /dev/sda2
    e2label /dev/sda2 system-data
echo "${PLUGIN_DEVICE} ${NVME_PART_MOUNT_PLUGIN} ext4 defaults,nofail,x-systemd.after=local-fs-pre.target,x-systemd.before=local-fs.target 0 2" >> /etc/fstab
```

> NOTE we will actually enable the overlayfs at the very end

**set the default mount of /media/plugin-data in the /etc/fstab**
```
    mkfs.ext4 /dev/sda3
    e2label /dev/sda3 plugin-data
    echo "/dev/sda3 /media/plugin-data ext4 defaults,nofail,x-systemd.after=local-fs-pre.target,x-systemd.before=local-fs.target 0 2" >> /etc/fstab
```

**Configure docker to use external media**

```
service docker stop
mv /var/lib/docker /media/plugin-data/
ln -s /media/plugin-data/docker/ /var/lib/docker
service docker start
```

> note: docker is already installed by the native L4T / Jetson so we will use that

**configure the network interface, udev rules**
```
/etc/udev/rules.d/10-waggle.rules in ROOTFS
```

> note: TODO we need to change the above as it configures for `wan0` on the ethernet and we need that to be `lan0`

**install k3s**
```
apt-get update ; apt-get install curl
curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION=v1.20.2+k3s1 INSTALL_K3S_SKIP_ENABLE=true K3S_CLUSTER_SECRET=4tX0DUZ0uQknRtVUAKjt sh -
```

**configure k3s to use the external media**
```
service k3s status
● k3s.service - Lightweight Kubernetes
   Loaded: loaded (/etc/systemd/system/k3s.service; disabled; vendor preset: enabled)
   Active: inactive (dead)
     Docs: https://k3s.io


NVMEMOUNT=/media/plugin-data

ls ${NVMEMOUNT}
docker  lost+found

mkdir -p ${NVMEMOUNT}/k3s/etc/rancher
mkdir -p ${NVMEMOUNT}/k3s/kubelet
mkdir -p ${NVMEMOUNT}/k3s/rancher

NVME_PART_MOUNT_PLUGIN=/media/plugin-data

ln -s ${NVME_PART_MOUNT_PLUGIN}/k3s/etc/rancher /etc/rancher
ln -s ${NVME_PART_MOUNT_PLUGIN}/k3s/kubelet /var/lib/kubelet
ln -s ${NVME_PART_MOUNT_PLUGIN}/k3s/rancher /var/lib/rancher

systemctl enable k3s.service
Created symlink /etc/systemd/system/multi-user.target.wants/k3s.service → /etc/systemd/system/k3s.service.
root@localhost:/usr/local/bin#
```

**configure network manager to not manage the k3s networks**
see file: /etc/NetworkManager/conf.d/cni.conf

IN PROGRESS here

**test k3s is working**
```
kubectl get node
kubectl get pod -A
```

# configured to run WES

-- set the nodes VSN
-- other stuff.... still figuring out what all of this is

# TODO ITEMS

## currently working on
- we need dnsmasq so that the camera gets an IP address on the lan port
  - need to host the 10.31.81.1/24 network
- configure the lan network rules
- set the node's hostname (becomes the k3s node name)
- k3s service override settings
- k3s shutdown service to ensure shutdown doesnt leave files open on file system

## later
- minimal Waggle config (node ID, VSN, kubernetes config) and try to connect to beekeeper for registration
- waggle elevated sudo access to docker, k3s, etc. (sudeors file)
- enable the overlayfs
- configure the wifi network rules
- figure out the correct udev rule for the lan ethernet adapter (based on the mac) (https://www.amazon.com/uni-Ethernet-Internet-Compatible-Notebook/dp/B087QFQW6F)
- list of apt-get install packages
  - probably want to split them into their own groups (dont install them all at the start, but instead when configure dnsmasq, install dnsmasq)
  - python2.7 and python3.6 (click, pip, etc.)

## Optional / research / unknown
- (optional) create /var/lib/nvpmodel/status file to set the default operating mode and fmode (fan mode) to `cool`
  - it seems that `cool` is not allowed.  so need to figure out what fan modes ARE supported, if any
- figure out if we want to allow `root` user to be able to login with ssh with password or not??
- some basic unit test / sanity test / health script to ensure the device is healthy (see the waggle-sanity-check - for the students)
  - check lan IP 
  - check k3s is running
  - check docker is running
  - check docker mirrors working
  - check internet connection
