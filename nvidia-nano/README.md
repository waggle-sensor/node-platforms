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
  ```bash
  fdisk --wipe always --wipe-partitions always /dev/sda
  g
  w
  ```
  **make the swap partition (16GB SWAP)**
  ```bash
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
  ```bash
  fdisk --wipe always --wipe-partitions always /dev/sda
  n
  ""
  ""
  +16G
  w
  ```
  
  **make the plugin-data (* the rest of the space)**
  ```bash
  fdisk --wipe always --wipe-partitions always /dev/sda
  n
  ""
  ""
  ""
  w
```

**turn on the swap**
format the swap
```bash
  root@localhost:~# mkswap /dev/sda1 -L ext-swap
Setting up swapspace version 1, size = 16 GiB (17179865088 bytes)
LABEL=ext-swap, UUID=6863907e-fe44-4d50-956b-cdc98490a059
```

**put the swap in the startup partition file**
```bash
echo "/dev/sda1 swap swap defaults,nofail 0 0" >> /etc/fstab
```

**setup the overlayfs partition**
```bash
    mkfs.ext4 /dev/sda2
    e2label /dev/sda2 system-data
echo "${PLUGIN_DEVICE} ${NVME_PART_MOUNT_PLUGIN} ext4 defaults,nofail,x-systemd.after=local-fs-pre.target,x-systemd.before=local-fs.target 0 2" >> /etc/fstab
```

> NOTE we will actually enable the overlayfs at the very end

**set the default mount of /media/plugin-data in the /etc/fstab**
```bash
    mkfs.ext4 /dev/sda3
    e2label /dev/sda3 plugin-data
    echo "/dev/sda3 /media/plugin-data ext4 defaults,nofail,x-systemd.after=local-fs-pre.target,x-systemd.before=local-fs.target 0 2" >> /etc/fstab
```

**Configure docker to use external media**

```bash
service docker stop
mv /var/lib/docker /media/plugin-data/
ln -s /media/plugin-data/docker/ /var/lib/docker
service docker start
```

> note: docker is already installed by the native L4T / Jetson so we will use that

**configure the network interface, udev rules**
```bash
/etc/udev/rules.d/10-waggle.rules in ROOTFS
```

> note: TODO we need to change the above as it configures for `wan0` on the ethernet and we need that to be `lan0`

**install k3s**
```bash
apt-get update ; apt-get install curl
curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION=v1.20.2+k3s1 INSTALL_K3S_SKIP_ENABLE=true K3S_CLUSTER_SECRET=4tX0DUZ0uQknRtVUAKjt sh -
```

**configure k3s to use the external media**
```bash
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

**k3s shutdown service**
see file: nvidia-nano/ROOTFS/etc/systemd/system/waggle-k3s-shutdown.service

enable service
```bash
systemctl daemon-reload
systemctl enable waggle-k3s-shutdown
```

**k3s service start-up ordering requirements (after sda)**

- nothing to do specifically here.. i dont think...

**k3s service startup customizations**

this requires a bunch of things to be installed

initial waggle config file
see file: ROOTFS/etc/waggle/config.ini

install the waggle-nodeid tool to generate the nodeid file used by other services
```bash
apt-get install python3-click
wget https://github.com/waggle-sensor/waggle-nodeid/releases/download/v1.0.7/waggle-nodeid_1.0.7_all.deb
dpkg -i waggle-nodeid_1.0.7_all.deb
```
^ this creates a waggle-nodeid service that should run on start-up and create the /etc/waggle/node-id file

configure the lan0 network interface to bind to 10.31.81.1
see file: ROOTFS/etc/NetworkManager/system-connections/lan
also did the wan and wifi files here too
see file: ROOTFS/etc/NetworkManager/system-connections/wan
see file: ROOTFS/etc/NetworkManager/system-connections/wifi

> note: the above files must have `0600` permissions

install and configure dnsmasq to create the device's internal 10.31.81.1/24 network (for use by kubernetes). enables agent k3s units (i.e. rpi) to be connected.
```bash
apt-get install dnsmasq
```

dnsmasq config file and service override file
see file: ROOTFS/etc/dnsmasq.d/10-waggle-base.conf
see file: ROOTFS/etc/systemd/system/dnsmasq.service.d/override.conf
```bash
systemctl daemon-reload
```

k3s service override
see file: ROOTFS/etc/systemd/system/k3s.service.d/override.conf
```bash
systemctl daemon-reload
```

install waggle-commontools to read the config
```bash
wget https://github.com/waggle-sensor/waggle-common-tools/releases/download/v1.0.0/waggle-common-tools_1.0.0_all.deb
dpkg -i waggle-common-tools_1.0.0_all.deb
```

k3s gpu access config
see folder: ROOTFS/etc/waggle/k3s_config/

setup the local docker registry mirrors (as the k3s config uses them)
see file: ROOTFS/etc/systemd/system/waggle-registry-local.service
see file: ROOTFS/etc/systemd/system/waggle-registry-mirror-docker.service
see file: ROOTFS/etc/systemd/system/waggle-registry-mirror-sage.service
see folder: ROOTFS/etc/waggle/docker_registry_config/
see folder: /ROOTFS/etc/waggle/docker/certs/

configure docker to use the local docker.io mirror registry
```bash
apt-get install jq
jq '. += {"registry-mirrors": [ "http://10.31.81.1:5001" ]}' /etc/docker/daemon.json > /tmp/daemon.json
mv /tmp/daemon.json /etc/docker/daemon.json
```

configure the local dev docker keys
```bash
chmod 600 /etc/waggle/docker/certs/domain.*
mkdir -p /etc/docker/certs.d/10.31.81.1\:5000/
cp /etc/waggle/docker/certs/domain.crt /etc/docker/certs.d/10.31.81.1\:5000/
mkdir -p /usr/local/share/ca-certificates
cp /etc/waggle/docker/certs/domain.crt /usr/local/share/ca-certificates/docker.crt
update-ca-certificates
```
output:
```bash
Updating certificates in /etc/ssl/certs...
1 added, 0 removed; done.
Running hooks in /etc/ca-certificates/update.d...
done.
```

make the directories for the docker registries
```bash
mkdir -p /media/plugin-data/docker_registry/mirrors/docker
mkdir -p /media/plugin-data/docker_registry/mirrors/sage
mkdir -p /media/plugin-data/docker_registry/local
```

enable the docker registry services
```bash
systemctl daemon-reload
systemctl enable waggle-registry-local.service
systemctl enable waggle-registry-mirror-docker.service
systemctl enable waggle-registry-mirror-sage.service
```

**LEFT OFF HERE**

to test:
- node-id file created using /etc/waggle/config.ini
- k3s service starts and the service override works
- k3s starts and basic pods run
- dnsmasq starts and the service override works
- run gpu-test in k3s to see if we get gpu access or not
- docker registries start and are being populated with the mirror
  - ensure can push to local registry and pull from local registry

**test k3s is working**
```bash
kubectl get node
kubectl get pod -A
```

**hostname configuration**

```bash
wget https://github.com/waggle-sensor/waggle-node-hostname/releases/download/v1.2.1/waggle-node-hostname_1.2.1_all.deb
dpkg -i waggle-node-hostname_1.2.1_all.deb
```

> NOTE: this is currently not working cause it relies on registration to be finished first
> ```bash
> Jun 21 18:14:36 localhost systemd[1]: Starting Waggle Hostname Service...
> Jun 21 18:14:36 localhost waggle_node_hostname.py[10208]: Waggle set hostname [node ID file: /etc/waggle/node-id | defer: True]
> Jun 21 18:14:36 localhost waggle_node_hostname.py[10208]: Registration key [/etc/waggle/bk_key.pem] missing, will NOT set hostname
> Jun 21 18:14:36 localhost systemd[1]: Started Waggle Hostname Service.
> ```

# configured to run WES

-- set the nodes VSN
-- other stuff.... still figuring out what all of this is

# random tool installation

`nslookup`
```bash
apt-get install dnsutils -y
```

# random tools to remove

`dhcpd` - we don't need this as we are not a dhcp server and we are using `dnsmasq` for this
```bash
apt-get purge isc-dhcp-server
```

# TODO ITEMS

## currently working on
- we need dnsmasq so that the camera gets an IP address on the lan port
  - need to host the 10.31.81.1/24 network
- configure the lan network rules
- set the node's hostname (becomes the k3s node name)
- k3s service override settings
- k3s shutdown service to ensure shutdown doesnt leave files open on file system
- internet share, to allow the camera to get internet access if it wants (and/or rpi)
- test the camera gets an IP on the 10.31.81.1/24 network
- set the default hostname to something like "pre-reg" or something like that
- update the MOTD to point out the url to go for registration

## later
- minimal Waggle config (node ID, VSN, kubernetes config) and try to connect to beekeeper for registration
- waggle elevated sudo access to docker, k3s, etc. (sudeors file)
- journal log config
- resolved config
- docker local registries
- enable the overlayfs
- configure the wifi network rules
- figure out the correct udev rule for the lan ethernet adapter (based on the mac) (https://www.amazon.com/uni-Ethernet-Internet-Compatible-Notebook/dp/B087QFQW6F)
- list of apt-get install packages
  - probably want to split them into their own groups (dont install them all at the start, but instead when configure dnsmasq, install dnsmasq)
  - python2.7 and python3.6 (click, pip, etc.)
- add the motd for waggle
- check service startup order (svg) to confirm its all good
- test camera connects and gets an IP in the dnsmasq pool

## Optional / research / unknown
- (optional) create /var/lib/nvpmodel/status file to set the default operating mode and fmode (fan mode) to `cool`
  - it seems that `cool` is not allowed.  so need to figure out what fan modes ARE supported, if any
- figure out if we want to allow `root` user to be able to login with ssh with password or not??
- the first time the external drive enumerated as `sdb` instead of `sda`, why?  we need to make sure this is consistent
- remove `dhcpd` service from running (its not running on a WSN)
- we _may_ not need the sage and docker.io mirror, as they just take up additional space and maybe take longer. there are no k3s agents to take advantage of the mirrors
  - plus this assumes a sagecontinuum.org ECR which we dont need to assume
- some basic unit test / sanity test / health script to ensure the device is healthy (see the waggle-sanity-check - for the students)
  - check lan IP 
  - check k3s is running
  - check docker is running
  - check docker mirrors working
  - check internet connection
