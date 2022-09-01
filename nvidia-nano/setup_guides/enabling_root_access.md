# Enabling `root` SSH access on Jetson Nano

This guide shows how to access `root` on the nano from another computer

**Required skills:** 
* Using command line arguments in Linux
* Using VIM in Linux

**Helpful guides:**
* [Linux Command Line Interface Introduction: A Guide to the Linux CLI](https://www.linuxjournal.com/content/linux-command-line-interface-introduction-guide)
* [Classic SysAdmin: Vim 101: A Beginner’s Guide to Vim](https://linuxfoundation.org/blog/classic-sysadmin-vim-101-a-beginners-guide-to-vim/)

---

### SSH access steps

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
          >Note: Write down your Jetson Nano's ip address it is very important in the following steps
  2. Run command `sudo su`
      1. enter in your password ie `waggle`

  3. Set root user password
      1. run command `passwd root`

      2. set password to `waggle`

  4. Enable root user ssh login
      1. run command `vim /etc/ssh/sshd_config`
          1. Go to the bottom of the file
          2. Enter in `PermitRootLogin yes` and `PasswordAuthentication yes` (Make sure they are in seperate lines)
          3. Save and exit the file
          > Note: In vim to enter in insert mode press 'i'. To exit insert mode press 'esc'. To save and quit type in ':wq' and press enter when not in insert mode
      2. run command `service sshd restart` to restart ssh service

> Note: The jetson nano can NOT have an IP on the ethernet in the 10.42.0.0 IP space as k3s internal network uses that subnet.

Continue to [Setting up Ansible on your computer](./configuring_ansible.md)