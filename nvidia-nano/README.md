# NVidia Nano Node Platform

Contains the specific instructions and `ansible` scripts for the NVidia Nano Node Platform.

## Table of Contents
1. Hardware needed
2. Bootstrap Steps
3. Enabling `root` SSH access
4. Setup the Extra Drive
5. Configure Docker to use External Media
6. Configure the Network Interface, Udev Rules
7. Install the Internet sharing service
8. Install k3s
9. Configure k3s to Use External Media
10. Configure Network Manager to Not Manage the k3s Networks
11. Set up k3s Shutdown Service
12. k3s Service Startup Customizations
13. k3s GPU access Config
14. Test k3s and Docker's GPU Access
15. Configure The Local Dev Docker Registry


## Hardware needed
 - NVIDIA Jetson Nano, either Micro-USB or DC power supply, barrel to set the jumper next to barrel connector to use barrel power, uSD memory cards, SD card reader, etc.
 - Sensors: camera, microphone, simple environmental sensors such as BME680.

> Note: The jetson nano can NOT have an IP on the ethernet in the 10.42.0.0 IP space as k3s internal network uses that subnet.  it breaks stuff.

### Connecting the hardware

TODO: list the instructions on what other hardware needs to be connected at this time (to ensure the future `ansible` script will work)
- 512GB USB drive
- usb2.0 extension to usb <-> ethernet dongle

## Bootstrap Steps
1. Install [NVidia Nano OS version 4.4.1](https://developer.nvidia.com/embedded/jetpack-sdk-441-archive) for Jetson Nano Developer Kit

2. Follow the instructions on the <a href="https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#write">
Getting Started with Jetson Nano Developer Kit</a> website to write the image to the microSD card
  
    1. Make sure to follow the correct set of instructions corresponding to your operating system

3. Insert the microSD card into the Nano
    1. The microSD card slot is located on the underside of the Nano
    >Dev Note (TODO): insert in image where the sd card is located
  
4. Jumper the J48 Power Selector Header Pins  
    1. Pins not jumpered:  
  <img alt='Not Jumpered Image'  src='non-jumpered.jpeg'></img>
  
    2. Pins Jumpered:
  <img alt='Jumpered Image'  src='jumpered.jpeg'></img>

5. Connect an ethernet cable that is connected to the internet into the port. This is where the nano will get access to WAN (Wide Area Network ie internet).

6. Connect your computer to the Nano via it's micro USB port
  
7. Follow the instructions on <a href="https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#setup-headless">Nvidia's website</a> 
to set up the Nano according to your operating system
<img alt='welcome' src='welcome.jpeg'></img>

8. Once you are connected to the nano go through the initial set up
    1. Set username to `waggle` and passwd to `waggle`
    > Dev note: come up with a better password later

    2. Set partition size to `0` or leave blank

    3. When you get to the Network Configuration Screen, select the `eth0` option

    4. Set hostname to localhost for now
        > Note: The hostname will change later to node id
    
    5. Use default nvpmodel (MAXN) (10W)
    > Dev note: we may be able to set this with ansible later. There are only 2 modes. the maxn is mode 001

## You should now be in the nano's command line!

Now let's setup `root` SSH access

## Enabling `root` SSH access (Jetson Nano Host)

  1. Get IP for `eth0`
      1. run command `ifconfig eth0`
      
          ```bash
          eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
          inet 000.000.0.000  netmask 000.000.000.0  broadcast 000.000.0.000
          inet6 fe80::4ab0:2dff:fe5b:fe63  prefixlen 64  scopeid 0x20<link>
          inet6 0000:000:0000:0000:0000:0000:0000:0000  prefixlen 00  scopeid 0x0<global>
          inet6 0000:000:0000:0000:0000:0000:0000:0000  prefixlen 00  scopeid 0x0<global>
          inet6 0000:000:0000:0000:0000:0000:0000:0000  prefixlen 00  scopeid 0x0<global>
          inet6 0000:000:0000:0000:0000:0000:0000:0000  prefixlen 00  scopeid 0x0<global>
          inet6 0000:000:0000:0000:0000:0000:0000:0000  prefixlen 00  scopeid 0x0<global>
          ether 00:00:00:00:00:00  txqueuelen 1000  (Ethernet)
          RX packets 1371647  bytes 1819095948 (1.8 GB)
          RX errors 0  dropped 0  overruns 0  frame 0
          TX packets 916252  bytes 87050219 (87.0 MB)
          TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
          device interrupt 151  base 0x5000
          ```

      2. The set of numbers next to inet is your ip address
          ```bash
          inet 000.000.0.000
          ```
  2. Run command `sudo su`
      1. enter in your password ie `waggle`

  3. Set root user password
      1. run comand `passwd root`

      2. set password to `waggle`
      > Dev note: come up with a better password later

  4. Enable root user ssh login
      1. run command `vim /etc/ssh/sshd_config`
          1. Go to the bottom of the file
          2. Enter in `PermitRootLogin yes` and `PasswordAuthentication yes` (Make sure they are in seperate lines)
          3. Save and exit the file
      > Note: In vim to enter in insert mode press 'i'. To exit insert mode press 'esc'. To save and quit type in ':wq' and press enter when not in insert mode

  5. Open another terminal and SSH as root into the nano `ssh root@<ip>`

### Set up SSH public key authentication to connect to a remote system (client side)

#### Getting a List of SSH Commands and Syntax
```ssh```

### Set up public key authentication using SSH on a Linux or macOS computer
To generate RSA keys, on the command line, enter:  ```ssh-keygen -t rsa```

### Use SFTP or SCP to copy the public key file (for example, ~/.ssh/id_rsa.pub) to your account on the remote system
```scp ~/.ssh/id_rsa.pub waggle@IP-Address```

### SSH Access
```ssh waggle@<ip> e.g., 10.0.0.151```

### SSH Access
```ssh-keygen -R <ip> e.g., 10.0.0.151```

### Install the same docker file from https://hub.docker.com/r/waggle/gpu-stress-test/tags
```docker pull waggle/gpu-stress-test:1.0.1```

### You won't see the any output on your current terminal. You can open another one.
```sudo docker run -it --rm --runtime nvidia --network host waggle/gpu-stress-test:1.0.1 -m 2```

## Ansible Provisioning

### Host machine (your laptop) Ansible setup

You will need to install `ansible` to the machine that you are using to `ssh` connect to the nano.

TOOD: fill in steps for configuring your laptop to run Nano.  With a link to some options (brew and/or pip for mac).

> Note: `ansible` is _not_ needed on the Nano in order to perform `ansible` provisioning.

## Setup the Extra Drive
1. Insert 512GB samsung usb stick into the nano

2. The drive should enumerate as `sda1`

    1. run command `lsblk` to check

3. Clear the current partition table and create GPT table

      ```bash
      fdisk --wipe always --wipe-partitions always /dev/sda
      g
      w
      ```
    1. run command `fdisk --wipe always --wipe-partitions always /dev/sda`
    2. press 'g' and then enter
    3. press 'w' and then enter

4. Make the SWAP partition (16GB SWAP)

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

    1. run command `fdisk --wipe always --wipe-partitions always /dev/sda`
    2. press 'n' and then enter
    3. leave blank and press enter
    4. leave blank and press enter
    5. type in '+16G' and press enter
    6. press 't' and press enter
    7. type in '19' and press enter
    8. press 'w' and press enter

5. Make the overlayfs 32GB

    ```bash
    fdisk --wipe always --wipe-partitions always /dev/sda
    n
    ""
    ""
    +32G
    w
    ```

    1. run command `fdisk --wipe always --wipe-partitions always /dev/sda`
    2. press 'n' and then enter
    3. leave blank and press enter
    4. leave blank and press enter
    5. type in '+32G' and press enter
    6. press 'w' and press enter

6. Make the plugin-data (the rest of the space)

    ```bash
      fdisk --wipe always --wipe-partitions always /dev/sda
      n
      ""
      ""
      ""
      w
    ```

    1. run command `fdisk --wipe always --wipe-partitions always /dev/sda`
    2. press 'n' and then enter
    3. leave blank and press enter
    4. leave blank and press enter
    5. leave blank and press enter
    6. press 'w' and press enter

7. Turn on the swap

    1. Run command `mkswap /dev/sda1 -L ext-swap`

        ```bash
          root@localhost:~ mkswap /dev/sda1 -L ext-swap
        Setting up swapspace version 1, size = 16 GiB (17179865088 bytes)
        LABEL=ext-swap, UUID=6863907e-fe44-4d50-956b-cdc98490a059
        ```

8. Put the swap in the startup partition file

    1. Run command `echo "/dev/sda1 swap swap defaults,nofail 0 0" >> /etc/fstab`

9. Setup the overlayfs partition

    1. run command `mkfs.ext4 /dev/sda2`
    2. run command `e2label /dev/sda2 system-data`

> Note: We will actually enable the overlayfs at the very end (TODO)

1.  Set the default mount of /media/plugin-data in the /etc/fstab

    1. Run command `mkfs.ext4 /dev/sda3`

    2. Run command `e2label /dev/sda3 plugin-data`

    3. Run command:
        ```bash
        echo "/dev/sda3 /media/plugin-data ext4 defaults,nofail,x-systemd.after=local-fs-pre.target,x-systemd.before=local-fs.target 0 2" >> /etc/fstab
        ```

2.  Reboot the nano by running command `reboot`

3.  SSH into the nano as root again

4.  run command `lsblk` to see the drive configured correctly
> Dev Note: insert in the correct output here

## Install Helpful Tools

1. Install helpful tools

```bash
apt-get update && apt-get install -y \
dnsutils \
htop \
iftop \
iotop \
jq \
nmap
```

## Remove Uneeded Items

1. Remove installs we don't need or conflict

```bash
apt-get purge -y \
isc-dhcp-server -y \
whoopsie
apt-get autoremove -y
```

2. Disable `apt` upgrade services

```bash
systemctl disable apt-daily.service && systemctl disable apt-daily.timer
systemctl disable apt-daily-upgrade.service && systemctl disable apt-daily-upgrade.timer
```

3. Disable the `motd` news updates

```bash
chmod -x /etc/update-motd.d/*
echo 'ENABLED=0' > /etc/default/motd-news
systemctl disable motd-news.service && systemctl disable motd-news.timer
```

## Add the WaggleOS MOTD

1. Copy file `/ROOTFS/etc/update-motd.d/05-waggle` to system and give execute permissions

```bash
scp ROOTFS/etc/update-motd.d/05-waggle <ip>:/etc/update-motd.d/05-waggle
```

```bash
chmod +x /etc/update-motd.d/05-waggle
```

## Configure the Network Interface, Udev Rules

1. Go into rules.d directory by running this command `cd /etc/udev/rules.d/`

2. Create a file using vim by running this command `vim 10-waggle.rules`

    1. Go into insert mode, and paste the following content
        ```bash
        ## WAN configuration
        # all: find the Nvidia native ethernet interface, assign to WAN
        KERNEL=="eth*", ATTR{address}=="48:b0:2d:*", NAME="wan0"

        ## LAN configuration
        KERNEL=="eth*", ATTR{address}=="f8:e4:3b:*", NAME="lan0"
        ```

    2. Escape insert mode, save and quit file

3. Reboot device to see eth0 change to wan0 

## Install the Internet sharing service

    ```bash
    wget https://github.com/waggle-sensor/waggle-internet-share/releases/download/v1.4.1/waggle-internet-share_1.4.1_all.deb

    dpkg -i waggle-internet-share_1.4.1_all.deb
    ```
    > Note: This creates a service that ensures that hardware on the 10.31.81.1 has Internet access (by sharing the Nano's Internet uplink)

## Configure `journalctl` to save historical logs

1. create the journal log folder
```bash
mkdir -p /var/log/journal
```

2. add the `journalctl` config

```bash
mkdir -p /etc/systemd/journald.conf.d/
````

```bash
scp ROOTFS/etc/systemd/journald.conf.d/10-waggle-journald.conf <ip>:/etc/systemd/journald.conf.d/10-waggle-journald.conf
```

## Configure Docker to use External Media

1. Stop docker by running command `service docker stop`
> Note: Docker is already installed by the native L4T / Jetpack so we will use that

2. Move docker by running command `mv /var/lib/docker /media/plugin-data/

3. Create a symbolic link by running command `ln -s /media/plugin-data/docker/ /var/lib/docker`

4. Start up docker by running command `service docker start`

## Install k3s

1. Install curl by running this command `apt-get install curl`

2. Install K3s via curl by running this command:
    ```bash
    curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION=v1.20.2+k3s1 INSTALL_K3S_SKIP_ENABLE=true K3S_CLUSTER_SECRET=4tX0DUZ0uQknRtVUAKjt sh -
    ```

## Configure k3s to Use External Media

1. Check the status of k3s by runnig this command `service k3s status`
    1. Output should look like this:
    ```bash
    ● k3s.service - Lightweight Kubernetes
    Loaded: loaded (/etc/systemd/system/k3s.service; disabled; vendor preset: enabled)
    Active: inactive (dead)
     Docs: https://k3s.io
    ```

2. Run this command to save external media dir as a variable `NVMEMOUNT=/media/plugin-data`

    1. Check if the variable was saved by running this command `ls ${NVMEMOUNT}`
        ```bash
        ls ${NVMEMOUNT}
        docker  lost+found
        ```

3. Run the following commands to create the neccessary directories in the external media
    ```bash
    mkdir -p ${NVMEMOUNT}/k3s/etc/rancher
    mkdir -p ${NVMEMOUNT}/k3s/kubelet
    mkdir -p ${NVMEMOUNT}/k3s/rancher
    ```

4. Run the following commands to create symbolic links in the newly created directories
    ```bash
    ln -s ${NVMEMOUNT}/k3s/etc/rancher /etc/rancher
    ln -s ${NVMEMOUNT}/k3s/kubelet /var/lib/kubelet
    ln -s ${NVMEMOUNT}/k3s/rancher /var/lib/rancher
    ```

5. Enable k3s by running this command `systemctl enable k3s.service`
    1. Output should look like this:
        ```bash
        Created symlink /etc/systemd/system/multi-user.target.wants/k3s.service → /etc/systemd/system/k3s.service.
        ```

## Configure Network Manager to Not Manage the k3s Networks

1. Go to directory `/etc/NetworkManager/conf.d/`

2. Create a file using vim by running this command `vim cni.conf`

    1. Go into insert mode, and paste the following content
        ```bash
        [keyfile]
        unmanaged-devices=interface-name:flannel.1;interface-name:veth*;interface-name:cni0
        ```

    2. Escape insert mode, save and quit file

## Set up k3s Shutdown Service

1. Go to directory `/etc/systemd/system/`

2. Create a file using vim by running this command `vim waggle-k3s-shutdown.service`

    1. Go into insert mode, and paste the following content
        ```bash
        [Unit]
        Description=Gracefully k3s Shutdown
        DefaultDependencies=no
        Before=shutdown.target

        [Service]
        Type=oneshot
        ExecStart=/usr/local/bin/k3s-killall.sh
        TimeoutStartSec=0

        [Install]
        WantedBy=shutdown.target 
        ```

    2. Escape insert mode, save and quit file

3. Enable service by running the following commands
    ```bash
    systemctl daemon-reload
    systemctl enable waggle-k3s-shutdown
    ```

## k3s Service Startup Customizations

1. Go to directory `/etc/`

2. Create a directory running this command `mkdir waggle`

3. Go into the waggle directory you just created

4. Create a file using vim by running this command `vim config.ini`

    1. Go into insert mode, and paste the following content
        ```bash
        [system]
        name = wd-nanocore

        [hardware]
        lan-interface = lan0
        wlan-interface = wan0
        wifi-interface = wifi0
        modem-interface = modem0

        [network]
        static-ip-nx = 10.31.81.1

        [registration]
        host = beekeeper.sagecontinuum.org
        port = 49190
        user = sage_registration
        key = /etc/waggle/sage_registration
        keycert = /etc/waggle/sage_registration-cert.pub

        [reverse-tunnel]
        host = beekeeper.sagecontinuum.org
        port = 49190
        key = /etc/waggle/bk_key.pem
        pubkey = /etc/waggle/bk_pubkey.pem
        ```

    2. Escape insert mode, save and quit file

5. Install python3-click by running this command `apt-get install python3-click`

6. Travel to home dir by running this command `cd ~`

7. Install the waggle-nodeid tool by running the follwing commands
    ```bash
    wget https://github.com/waggle-sensor/waggle-nodeid/releases/download/v1.0.7/waggle-nodeid_1.0.7_all.deb

    dpkg -i waggle-nodeid_1.0.7_all.deb
    ```
    > Note: This creates a waggle-nodeid service that should run on start-up and create the /etc/waggle/node-id file

8. Reboot the device so the service creates the /etc/waggle/node-id file

9. Execute this command to test if the service is working `service waggle-nodeid status`
    ```bash
    Dev Note: insert correct output here
    ```
    - If hostname does not resemble 'wd-nanocore-\<id\>' after the test was done then do the following:

        1. Go to home directory `cd ~`

        2. Install waggle-node-hostname by running the following commands:
            ```bash
            wget https://github.com/waggle-sensor/waggle-node-hostname/releases/download/v1.2.1/waggle-node-hostname_1.2.1_all.deb

            dpkg -i waggle-node-hostname_1.2.1_all.deb
            ```

        3. Run the following commands:
            ```bash
            touch /etc/waggle/bk_key.pem

            /usr/bin/waggle_node_hostname.py -n /etc/waggle/node-id

            rm /etc/waggle/bk_key.pem
            ```

            > Note: this is a work-around that will fixed better later (TODO)

        4. Reboot the device, Hostname should change after that


10. Configure the lan0 network interface to bind to 10.31.81.1

    1. Go to directory `/etc/NetworkManager/system-connections/`

    2. Create a file using vim by running this command `vim lan`

        1. Go into insert mode, and paste the following content
            ```bash
            [connection]
            id=lan
            type=ethernet
            autoconnect=true
            interface-name=lan0
            permissions=

            [ethernet]
            auto-negotiate=true
            mac-address-blacklist=

            [ipv4]
            address1=10.31.81.1/24
            dns-search=
            method=manual
            never-default=true

            [ipv6]
            addr-gen-mode=stable-privacy
            dns-search=
            method=ignore
            ```

        2. Escape insert mode, save and quit file

    3. Apply 0600 permission to lan file by running this command `chmod 0600 lan`
  
    4. Create a file using vim by running this command `vim wan`

        1. Go into insert mode, and paste the following content
            ```bash
            [connection]
            id=wan
            type=ethernet
            autoconnect=true
            interface-name=wan0
            permissions=

            [ethernet]
            auto-negotiate=true
            mac-address-blacklist=

            [ipv4]
            dns-search=
            method=auto

            [ipv6]
            addr-gen-mode=stable-privacy
            dns-search=
            method=ignore
            ```

        2. Escape insert mode, save and quit file

    5. Apply 0600 permission to wan file by running this command `chmod 0600 wan`

    6. Create a file using vim by running this command `vim wifi`

        1. Go into insert mode, and paste the following content
            ```bash
            [connection]
            id=wifi
            type=wifi
            autoconnect=true
            interface-name=wifi0
            permissions=

            [wifi]
            mac-address-blacklist=
            mode=infrastructure
            #ssid=<access_point>

            [wifi-security]
            auth-alg=open
            #key-mgmt=wpa-psk
            #psk=<password>

            [ipv4]
            dns-search=
            method=auto

            [ipv6]
            addr-gen-mode=stable-privacy
            dns-search=
            method=ignore
            ```

        2. Escape insert mode, save and quit file

    7. Apply 0600 permission to wan file by running this command `chmod 0600 wifi`

11. Install and configure dnsmasq to create the device's internal 10.31.81.1/24 network (for use by kubernetes).

    1. Install dnsmasq by running this command `apt-get install dnsmasq`

    2. Go to directory `/etc/dnsmasq.d`

    3. Create a file using vim by running this command `vim 10-waggle-base.conf`

        1. Go into insert mode, and paste the following content
            ```bash
            ## Basic global config
            log-dhcp
            #log-queries

            ## LAN DNS resolution / forwarding
            listen-address=10.31.81.1
            interface=lan0
            bind-interfaces

            ## Global DHCP Options
            dhcp-authoritative
            bogus-priv
            # gateway
            dhcp-option=3,10.31.81.1
            # DNS server
            dhcp-option=6,10.31.81.1

            ## DHCP address assignment
            dhcp-mac=set:rpi,DC:A6:32:*:*:*
            dhcp-mac=set:rpi,3A:35:41:*:*:*
            dhcp-mac=set:rpi,E4:5F:01:*:*:*
            dhcp-mac=set:rpi,28:CD:C1:*:*:*
            dhcp-range=tag:rpi,10.31.81.4,10.31.81.4,infinite
            dhcp-mac=set:camera,9C:8E:CD:*:*:* # AMCREST camera
            dhcp-mac=set:camera,E4:30:22:*:*:* # Hanwha camera
            dhcp-mac=set:camera,00:03:C5:*:*:* # Mobotix camera
            dhcp-range=tag:camera,10.31.81.10,10.31.81.19,infinite
            # general DHCP pool
            dhcp-range=10.31.81.50,10.31.81.254,10m
            ```

        2. Escape insert mode, save and quit file

    4. Go to directory `/etc/systemd/system`

    5. Create a directory by running this command `mkdir dnsmasq.service.d`

    6. Go into this newly created directory `cd dnsmasq.service.d`

    7. Create a file using vim by running this command `vim 10-waggle-base.conf`

        1. Go into insert mode, and paste the following content
            ```bash
            [Unit]
            # start after the lan0 bound interface is up
            Requires=network-online.target
            After=network-online.target

            [Service]
            Restart=always
            RestartSec=30
            ```

        2. Escape insert mode, save and quit file

    8. Reload daemon by running this command `systemctl daemon-reload`

12. Set up k3s service override

    1. Go to directory `/etc/systemd/system`

    2. Create a directory by running this command `mkdir k3s.service.d`

    3. Go into the directory you just created `cd k3s.service.d`

    4. Create a file using vim by running this command `vim override.conf`

        1. Go into insert mode, and paste the following content
            ```bash
            [Unit]
            After=waggle-nodeid.service
            Wants=waggle-nodeid.service
            # desire to start after dnsmasq creates the lan IP
            After=dnsmasq.service
            Wants=dnsmasq.service

            [Service]
            # Fail service if Node ID file does not exist
            ExecStartPre=/usr/bin/test -e /etc/waggle/node-id
            ExecStartPre=/usr/bin/nmcli conn up lan
            ExecStartPre=/etc/waggle/k3s_config/pre-run.sh
            ExecStart=
            ExecStart=/bin/bash -ce "/usr/local/bin/k3s server \
              --node-name $(cat /etc/waggle/node-id).$(waggle-get-config -s system -k name) \
              --disable=traefik \
              --bind-address $(waggle-get-config -s network -k static-ip-nx) \
              --node-ip $(waggle-get-config -s network -k static-ip-nx) \
              --advertise-address $(waggle-get-config -s network -k static-ip-nx) \
              --flannel-iface $(waggle-get-config -s hardware -k lan-interface) \
              --resolv-conf /etc/waggle/k3s_config/resolv.conf \
            " 
            ```

        2. Escape insert mode, save and quit file
    
    5. Reload daemon by running this command `systemctl daemon-reload`

13. Install waggle-commontools to read the config

    1. Travel to your home directory by running this command `cd ~`

    2. Install waggle-commontools by running the following commands:
        ```bash
        wget https://github.com/waggle-sensor/waggle-common-tools/releases/download/v1.0.0/waggle-common-tools_1.0.0_all.deb

        dpkg -i waggle-common-tools_1.0.0_all.deb
        ```

## k3s GPU access Config

1. Go to directory `/etc/waggle/`

2. Create a new directory by running this command `mkdir k3s_config`

3. Go into the directory you just created `cd k3s_config`

4. Create a file using vim by running this command `vim config.toml.tmpl`

    1. Go into insert mode, and paste the following content
        ```bash
        [plugins.opt]
          path = "/var/lib/rancher/k3s/agent/containerd"


        [plugins.cri]
          stream_server_address = "127.0.0.1"
          stream_server_port = "10010"
          enable_selinux = false
          sandbox_image = "rancher/pause:3.1"


        [plugins.cri.containerd]
          disable_snapshot_annotations = true
          snapshotter = "overlayfs"


        [plugins.cri.cni]
          bin_dir = "{{ .NodeConfig.AgentConfig.CNIBinDir }}"
          conf_dir = "{{ .NodeConfig.AgentConfig.CNIConfDir }}"


        [plugins.cri.containerd.runtimes.runc]
          runtime_type = "io.containerd.runc.v2"


        [plugins.cri.containerd.runtimes.runc.options]
          BinaryName = "nvidia-container-runtime" 
        ```

    2. Escape insert mode, save and quit file

5. Create a file using vim by running this command `vim pre-run.sh`

    1. Go into insert mode, and paste the following content
        ```bash
        #!/bin/bash -e

        # Script to be run before every execution of the K3s server

        CONFIG_DEST=/var/lib/rancher/k3s/agent/etc/containerd/config.toml.tmpl
        CONFIG_SRC=/etc/waggle/k3s_config/config.toml.tmpl

        # ensure the destination path exists
        mkdir -p $(dirname $CONFIG_DEST)

        cp $CONFIG_SRC $CONFIG_DEST
        ```

    2. Escape insert mode, save and quit file

6. Give execution permission to pre-run.sh by running this command `chmod +x pre-run.sh`

7. Create a file using vim by running this command `vim resolv.conf`

    1. Go into insert mode, and paste the following content
        ```bash
        # Use local dnsmasq DNS (backed by systemd-resolve)
        nameserver 10.31.81.1
        ```

    2. Escape insert mode, save and quit file

## Test k3s and Docker's GPU Access

1. Test k3s service override by running the following commands:
    ```bash
    service k3s status
    systemctl cat k3s
    ```

    - Make sure lan and wan are connected before testing k3s service
        ```
        wan0
        u should have your uplink (to network switch) plugged into the nano ethernet port

        lan0
        u should have the ethernet dongle connected to a usb port
        (this is what you connect the camera to)
        ```
    
        - if this is not the case then you will get this error when running `service k3s status`:
        ```bash
        Process: 7538 ExecStartPre=/usr/bin/nmcli conn up lan (code=exited, status=4)
        ```

    - k3s service should start and the service override should work
    >Dev Note: Insert correct Ouput here

2. If `service k3s status` returns active then test k3s and run basic pod by running the following commands:
    ```bash 
    kubectl get pod -A
    kubectl get node
    ```
    - The output should look like this:
        ```bash
        NAME                           STATUS   ROLES                  AGE   VERSION
        000048b02d5bfe58.wd-nanocore   Ready    control-plane,master   19h   v1.20.2+k3s1
        ```
3. Test dnsmasq by running the following commands:
    ```bash
    service dnsmasq status
    systemctl cat dnsmasq.service
    ```
    >Dev Note: insert the correct output here

4. Test docker's GPU access by running this command `docker run -ti --rm --gpus all waggle/gpu-stress-test:latest`

    - To see if the gpu is being used check the gpu frequency (GR3D_FREQ) by running this command `tegrastats` in a seperate terminal

5. If `service k3s status` returns active and `kubectl get node` returns an active node then test k3s' GPU access by running this command `kubectl run gpu-test --image=waggle/gpu-stress-test:latest --attach=true`
    > Note: You may see the error `error: timed out waiting for the condition`. that is okay. it just means it is taking a long time to create the container in `k3s`

    - It takes a while for the pod to create, to watch the pod creation status run this command `watch kubectl get pod`

    - To see if the gpu is being used check the gpu frequency (GR3D_FREQ) by running this command `tegrastats` in a seperate terminal

6. Once the pod stops running (~5 min) delete the pod by running this command `kubectl delete pod gpu-test &`

## Configure The Local Dev Docker Registry
> Dev Note: Skipping the sage and docker.io mirror registries as they just add a complexity we don't need

1. Setup the local docker registry mirrors (as the k3s config uses them)

    1. Go to directory `/etc/systemd/system/`

    2. Create a file using vim by running this command `vim waggle-registry-local.service`

        1. Go into insert mode, and paste the following content
            ```bash
            [Unit]
            Description=Waggle Docker Registry (Local)
            Requires=docker.service
            After=docker.service

            [Service]
            Restart=always
            RestartSec=30s
            ExecStart=/usr/bin/docker run --rm -p 5000:5000 --name local_registry \
                -v /media/plugin-data/docker_registry/local:/var/lib/registry \
                -v /etc/waggle/docker/certs:/certs \
                -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt \
                -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key \
                registry:2
            ExecStop=/usr/bin/docker stop local_registry
            ExecStopPost=-/usr/bin/docker container rm local_registry

            [Install]
            WantedBy=default.target
            ```

        2. Escape insert mode, save and quit file

    3. Go to directory `/etc/waggle/`
    
    4. Create a directory by running this command `mkdir docker`

    5. Travel into the newly created directory `cd docker`

    6. Create a directory by running this command `mkdir certs`

    7. Travel into the newly created directory `cd certs`

    8. Create a file using vim by running this command `vim domain.crt`

        1. Go into insert mode, and paste the following content
            ```bash
            -----BEGIN CERTIFICATE-----
            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
            -----END CERTIFICATE----- 
            ```

        2. Escape insert mode, save and quit file

    9. Create a file using vim by running this command `vim domain.key`

        1. Go into insert mode, and paste the following content
            ```bash
            -----BEGIN PRIVATE KEY-----
            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
            dNwDizqw0ZcIa06csX3gKiTtCsooW98=
            -----END PRIVATE KEY-----
            ```

        2. Escape insert mode, save and quit file

2. Configure the local dev docker keys
    
    1. Go to home directory `cd ~` and run the following commands:
        ```bash
        chmod 600 /etc/waggle/docker/certs/domain.*

        mkdir -p /etc/docker/certs.d/10.31.81.1\:5000/

        cp /etc/waggle/docker/certs/domain.crt /etc/docker/certs.d/10.31.81.1\:5000/

        mkdir -p /usr/local/share/ca-certificates

        cp /etc/waggle/docker/certs/domain.crt /usr/local/share/ca-certificates/docker.crt

        update-ca-certificates
        ```

    2. After running `update-ca-certificates` the ouput should look like the following:
        ```bash
        Updating certificates in /etc/ssl/certs...
        1 added, 0 removed; done.
        Running hooks in /etc/ca-certificates/update.d...
        done.
        ```
3. Make the directories for the docker registries `mkdir -p /media/plugin-data/docker_registry/local`

4. Enable the docker registry services by running the following commands:
    ```bash
    systemctl daemon-reload
    systemctl enable waggle-registry-local.service
    ```

5. To test the local dev docker registry run the following commands:
    ```bash
    curl https://10.31.81.1:5000/v2/_catalog
    ```
    - Output:
    ```bash
    {"repositories":[]}
    ```

6. Ensure you can pull from local registry by running the following commands:
    ```bash
    docker pull ubuntu:latest

    docker tag ubuntu:latest 10.31.81.1:5000/joe:latest

    curl https://10.31.81.1:5000/v2/_catalog
    ```
    - Output
    ```bash
    {"repositories":[]}
    ```

7. Ensure you can push to local registry by running this command:
    ```bash
    docker push 10.31.81.1:5000/joe:latest
    ```
    - Output
    ```bash
    13e8c0db60e7: Pushed
    latest: digest: sha256:0f744430d9643a0ec647a4addcac14b1fbb11424be434165c15e2cc7269f70f8 size: 529
    ```
    > Note: while doing the above `push` you should see logs in `docker logs -f local_registry`

8. You should now see a repository by running this command `curl https://10.31.81.1:5000/v2/_catalog`

    - Output
    ```bash
    {"repositories":["joe"]}
    ```

## Add fallback DNS

ROOTFS file: ROOTFS/etc/systemd/resolved.conf.d/10-waggle-resolved.conf

## Add wifi dongle support

ROOTFS file: ROOTFS/etc/udev/rules.d/10-waggle.rules
ROOTFS file: ROOTFS/etc/modprobe.d/rtl8821cu.conf
ROOTFS file: ROOTFS/etc/modprobe.d/rtl8822bu.conf

> Note: the modprobe conf files above disable the auto-power management (which is unstable)

### Add 'waggle' hotspot support

ROOTFS file: ROOTFS/etc/NetworkManager/system-connections/wifi-waggle

```bash
chmod 600 /etc/NetworkManager/system-connections/*
```

> Note: the device will auto-connect to a `ssid: waggle` / `passwd: Why1Not@Waggle` network now

## Enable NetworkManager Connectivity checks

ROOTFS file: ROOTFS/etc/NetworkManager/conf.d/99-connectivity.conf

```bash
echo 'net.ipv4.conf.default.rp_filter = 2' >> /etc/sysctl.conf
echo 'net.ipv4.conf.all.rp_filter = 2' >> /etc/sysctl.conf
```

> Note: this change ensures that default `ip route` that is used actually has an Internet connection

## Set the node friendly ID (VSN)

```bash
# echo N001 > /etc/waggle/vsn
```

> Note: the above instructions hard-code a static VSN.  In the future we will want to generate a random VSN (NXXX where X is a [0-9A-Z]) (TODO)

## Register node and establish connection to Beehive

1. Install the registration and reverse tunnel services

```bash
wget https://github.com/waggle-sensor/waggle-bk-registration/releases/download/v2.2.2/waggle-bk-registration_2.2.2_all.deb
wget https://github.com/waggle-sensor/waggle-bk-reverse-tunnel/releases/download/v2.3.2/waggle-bk-reverse-tunnel_2.3.2_all.deb
dpkg -i waggle-bk-registration_2.2.2_all.deb
dpkg -i waggle-bk-reverse-tunnel_2.3.2_all.deb
```

> note: we either need to reboot after the above steps or force start the services

2. Copy the Beekeeper known hosts public CA

ROOTFS: ROOTFS/etc/ssh/ssh_known_hosts

```bash
chmod 644 /etc/ssh/ssh_known_hosts
```

3. Copy registration private key

ROOTFS file: ROOTFS/etc/waggle/sage_registration

```bash
chmod 600 /etc/waggle/sage_registration
```

> note: this file is not checked into the code at this time, need to triple-check its safe to do so. (TODO)

3. Copy the registration certificate

Obtain the regristration certificate from the "node registration portal" and copy to: `/etc/waggle/sage_registration-cert.pub`

```bash
chmod 600 /etc/waggle/sage_registration-cert.pub
```

> Note: for the initial test the "production" registration certificate was used, which not be what is used long term
> Note: this will be the registration cert that is obtained from the "node registration portal"

4. Enable admin reverse tunnel access

ROOTFS: ROOTFS/root/.ssh/authorized_keys.prod

```bash
cat /root/.ssh/authorized_keys.prod >> /root/.ssh/authorized_keys
```

> note: the above file is _appended_ to the currently existing authorized_keys file, as the file was already created and has a key in it to enable the `ansible` ssh session

> note: at this time an admin should be able to login to the nano via the reverse tunnel through the beekeeper administrative services


# TODO ITEMS

## currently working on
 - launch and get WES running on the node

## later
- enable the overlayfs
- we need the `ip_set` kernel modules maybe
- check service startup order (svg) to confirm its all good
- get microphone running and wes configued to set the nano core as the node running the audio-server
- the camera will have an IP in the range of 10.31.81.10 - 19. do we want to set the Amcrest camera to a static IP (i.e. 10.31.8.20 ) ?
  - we also need to figure out how to connect the camera to pyWaggle / WES. we don't want to have to run the "camera provisioner"
- add version to `/etc/waggle_version_os`
- install and have the Nano's use the wan-tunnel to route all Internet traffice through beekeeper
- figure out how to generate a random VSN
  - NXXX where X is a random value between [0-9A-Z]

## Optional / research / unknown
- update the instructions for creating a "dummy" user on install and then adding the creation of the `waggle` user in the Ansible script so that it can be updated and easily versioned (instead of relying on the initial creation).  can tie this into sudoers access for `waggle` etc.
  - this may not be necessary as the user can operate as `root` on the node, and we should encourage that.
- (optional) create /var/lib/nvpmodel/status file to set the default operating mode and fmode (fan mode) to `cool`
  - it seems that `cool` is not allowed.  so need to figure out what fan modes ARE supported, if any
- figure out if we want to allow `root` user to be able to login with ssh with password or not??
- the first time the external drive enumerated as `sdb` instead of `sda`, why?  we need to make sure this is consistent
- remove `dhcpd` service from running (its not running on a WSN)
- we _may_ not need the sage and docker.io mirror, as they just take up additional space and maybe take longer. there are no k3s agents to take advantage of the mirrors
  - plus this assumes a sagecontinuum.org ECR which we dont need to assume
- remove the X server and other gui elements that take up a alot of space/resources
  - this also includes extras that NVidia put in there (examples maybe?)
- some basic unit test / sanity test / health script to ensure the device is healthy (see the waggle-sanity-check - for the students)
  - check lan IP 
  - check k3s is running
  - check docker is running
  - check docker mirrors working
  - check internet connection
- update the MOTD to point out the url to go for registration
- add support for RPI PxE booting, to allow for an easy downstream "agent"
  - this also requires the fix to allow the rpi to use the local docker registry on the core (TBD)
- add a Ansible script for configuring the Nano to operate as an "agent" instead of a "core"
  - this includes the required ssh key access to be able to ssh to the agents from the core (for admin stuff)
  - this includes the local docker registry access
- the `lsblk` is showing up as, why does it have the UUID in it?
  ```
  ├─sda2         8:2    1    16G  0 part /media/1aef5c37-a088-4343-9a55-530d68442109
  └─sda3         8:3    1 428.3G  0 part /media/df5990dc-414c-4aa4-975d-774bc8811a8a
  ```
  - auto-mount problem (see: `systemctl --failed`)
  
