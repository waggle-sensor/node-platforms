# Configure Ansible

This guide shows how to access the IP address of the nano, clone the **waggle-sensor/node-platforms** repository, and configure the Ansible inventory file

**Required skills:** 
* Using the Command Line Interface of your computer
* Using command line arguments in Linux
* Cloning a GitHub repository

**Helpful guides:**
* [Linux Command Line Interface Introduction: A Guide to the Linux CLI](https://www.linuxjournal.com/content/linux-command-line-interface-introduction-guide)
* [Cloning a GitHub repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)  

---

### SSH access steps

  1. Connect to the nano's command line again by following step 9 in <a href="https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#setup-headless">Initial Setup Headless Mode</a>
  2. Get IP for eth0
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
  3. Open a terminal on your computer and travel to your home directory (`cd ~` on macOS)
  4. Clone this repository using this command:
        ```
        git clone https://github.com/waggle-sensor/node-platforms.git
        ```
  5. Travel into the folder that is holding the Ansible Playbooks using this command:
        ```
        cd ~/node-platforms/nvidia-nano
        ```
        >Note: Everytime you run an ansible commmand make sure you are in this directory
  6. Replace `{ip}` in the `ansible_inventory` file with your Jetson Nano's ip address using vim or any other text editor program
       - After it is replaced it should look similiar to this
           ```
           [nano:vars]
           ansible_host=0.0.0.0
           ```

##### Ansible is all setup!

Continue to [Running The Ansible Playbook](./running_ansible.md)