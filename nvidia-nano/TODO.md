# To-Do Backlog

This is an organized list of the items that are left to complete for the Nvidia Nano platform support.

# Priority Items

1. Organize the README better
   - move the images to a sub-folder
   - minimize the README to make it less scary
   - Break the README into "sections" that link off to other guides ("hardware setup", "flashing the SD card", "running the Ansible script", "Verify / Test Nano")
   - Copy over hardware from SageEdu repo
   - Add more details to the [hardware list](./bom.md) and keep it up-to-date. Also label them with pictures, so it's easier to connect the hardware

2. Tech items to fix in the Ansible script
   - update the docker part to delete all pre-existing docker images (rm docker folder) and always create a new empty one to start from
   - combine networkmanager items into 1 with_items. remove the extra permissions apply to the NetworkManager folder
   - when combining all the files from ROOTFS and setting specific permissions, we can loop the permissions in the next step with_items to ensure they are correct
   - update the /etc/sysctl.conf check for the rp_filter to use a "in file" ansible command to ensure it is there. use `blockinfile` ansible builtin
   - make the default/motd-news a ROOTFS file

3. Change how the 'hosts: all" works. we only want to do this for nano hosts.  and then we can have a nano-agent host?  i dont know quite yet how we want to do this.
    - reference: https://github.com/NVIDIA/cloud-native-core/blob/master/playbooks/guides/Jetson_Xavier_v7.0.md#using-the-ansible-playbooks

4. Update the `inventory` file to use a username / password instead of needing a user to create a `ssh` key-pair and do all the hacking of getting the key onto the device.
    - See below: we could have the `setup.sh` script do alot of this. Create a ssh key-pair, execute `ssh copy-id` to the node (using the known user/password), and then run the playbook
    - reference: https://github.com/NVIDIA/cloud-native-core/blob/master/playbooks/guides/Jetson_Xavier_v7.0.md#using-the-ansible-playbooks

5. Create a `setup.sh` script takes arguments (i.e. node IP address), configures the inventory file and runs the `ansible-playbook`
   - Can also optionally install `ansible` to the user's host machine and do some other "connection tests"
   - reference: https://github.com/NVIDIA/cloud-native-core/blob/master/playbooks/setup.sh

6. Split the Ansible script into different grouped parts that be eventually imported into other platforms.  Need to consider 'core' vs 'agent' here
    - Docker section, k3s section, docker local registry section, waggle apps section, etc.
    - reference: https://github.com/NVIDIA/cloud-native-core/blob/master/playbooks/cnc-installation.yaml

7. `/etc/resolv.conf` on the 'core' should be `127.0.0.53`.  Need to be sure this is the case. On 1 node, this was `127.0.0.1` and I think it was being managed by `resolvconf`.  This `resolvconf` service exists, and it does not on the WWN so it should probably be removed.

8. Figure out how to generate a random VSN. NXXX where X is a random value between [0-9A-Z]

9. Update the Ansible script with the URL to go-to for registration.

10. Figure out how to Ansible flash a `sda` usb drive that already has partitions on it. Figure out how to disable "auto-mount" which seems to be messing things up (see: `systemctl --failed`).

11. Add microphone support. WES needs to be configured to detect the microphone and run the audio-server on the k3s node that contains the microphone.

12. The camera will have an IP in the range of 10.31.81.10 - 19. Do we want to set the Amcrest camera to a static IP (i.e. 10.31.8.20 ), so that it's easy to get be used by `pywaggle` / WES. With a static IP address the camera can be easily discovered and "hard-coded" into the WES config for `pywaggle` to discover.

13. Investigate if the `ip_set` kernel module is needed. This was something that was required to enable some kubernetes networking features on the WWN and therefore might be needed here.

14. Add the BME680 sensor support steps to the Ansible script

15. Add a Ansible script for configuring the Nano to operate as an "agent" instead of a "core".  Maybe use a "global variable" to control the Ansible scripts. And/or we do differnet 'hosts' in the inventory file.
   - required ssh key access to be able to ssh to the agents from the core (for admin stuff)
   - local docker registry access
     - don't include local docker registry service
   - k3s-agent instead of k3s
   - exclude waggle apps (registration, reverse tunnel, wan-tunnel, hostname)
   - remove nfs-kernel-server, dnsmasq, etc.
   - agent config.ini

# Nice-to-Have / Investigation Items

1. Investigate how to simplify the initial steps of setup where the user must serial (or monitor & keyboard) connect to the device and entire a bunch of information (user, eth0, etc.). These steps are prone to human error and we should figure out the best way to avoid that. This includes maybe adding the creation of the `waggle` user to the Ansible script.
   - Maybe we can create a script that the user runs that does the setup for them so they don't have to type anything in.

1. Enable the `overlayfs` file-system to prevent file system writes to the eMMC / SDcard from filling up the disk. Leverage the external media for the overlay to (a) ensure disk space and (b) allow an easy roll-back if the user messes up their system.  Should this be done before registration, probably.

1. Add version to `/etc/waggle_version_os`

1. Install and have the Nano's use the wan-tunnel to route all Internet traffic through beekeeper. This ensure system's will work the same no matter where they are residing.

1. Have the user login to the node as the `root` user so they don't have to type sudo for anything.
   - Or we have the same experience on the WWN where the `sudoers` file for the `waggle `user enables `sudo` access to development tools (`docker`, `kubectl`, `pluginctl`, etc.) and we update the `waggle` user's `.bashrc` to allow them to type the commands without needing to type `sudo`.

1. Create /var/lib/nvpmodel/status file to set the default operating mode and fmode (fan mode) to `cool`.  We don't even know if there are more then 1 mode even supported.

1. The fan does not seem to spin at all, need to figure this out.

1. Check the different run `nvpmodel` run modes (10W vs ?) and ensure we have it set to max and that the `nvpmodel` service is started on boot to configure it from the saved config.

1. Add the sage and docker.io mirror to allow agents to take advantage.
    - this also assumes sagecontinuum.org ECR which isn't necessarily true.

1. Remove the X server and other gui elements that take up a a lot of space/resources
    - We need to validate if this is a good idea or not, as some developers may want to use a monitor, mouse & keyboard.

1. Create unit-testing scripts / Ansible that can be run after complete to ensure system health.  Do we want as `waggle-sanity-check` running?  Maybe this Ansible script could be run on any WWN node too?  It should be able to do most of the same stuff (be conditional based on the type of node we are connecting to)
   - check lan IP 
   - check k3s is running
   - check docker is running
   - check docker local registry working
   - check internet connection
   - check `lsblk` drives / partitions
   - reference: https://github.com/NVIDIA/cloud-native-core/blob/master/playbooks/cnc-validation.yaml

1. Add support for RPI PxE booting, to allow for an easy downstream "agent".  We need to figure out how to "download" and install this onto the system into the limited 16GB that we have on the production Nano units.
   - this also requires the fix to allow the rpi to use the local docker registry on the core (TBD)

1. How to detect which nano is whose? how will you do this? imagine a class setting with many nanos being configured. We want to blink an LED or something for someone so they can identify their Nano in a table full of them.

# Items to Verify

1. Check service startup order (svg) to confirm its all good

1. `dhcpd` is no longer running now that `isc-dhcp-server` is removed.

