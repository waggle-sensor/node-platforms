## Running the Ansible Playbook

This guide will show how to run the Ansible Playbook

**Required Skills:**
* Using the Command Line Interface of your computer

---

Ansible should now be set up to run the playbook that will configure your Jetson to run Waggle Edge Stack (WES). 

Stuff to keep in mind while the ansible script runs:

- **Don't play with the Jetson while the playbook runs**. It can mess it up!

- **Don't leave your desk while the playbook runs**! The playbook will give you more instructions on what to do as it runs

- If you are connecting over wifi it can cause the ansible playbook to disconnect when the nano reboots, so having both the nano and your computer on ethernet connections is recommended

- Connect your hardware when the ansible playbook tells you to

- In the playbook output, `ok` in green means nothing was changed and `changed` in yellow means something was changed in the client (i.e. the Jetson Nano). **Anything in red means something failed and the playbook will stop executing**

- If the playbook fails, it is safe to re run it nothing will be duplicated

- The playbook will enable root ssh, so to connect to the nano in the future use the command `ssh root@<IP>`

## Selecting a recipe for your Jetson
Because your Jetson may have different hardware configuration, it is important to select the right recipe to convert the Jetson into a Waggle device. Please follow the steps below carefully to build up a recipe for configuring the Jetson.

0. Go to the **~/node-platforms/nvidia_jetson** directory
```
cd nvidia_jetson
```

1. Create an Ansible playbook for your configuration. You will need to add parameters based on the instructions below,
```bash
python3 create_ansible.py --help
```
```bash
usage: create_ansible.py [-h] --type {core,agent} [--enable-extra-drive] [--output PATH]

options:
  -h, --help            show this help message and exit
  --type {core,agent}   Specify Waggle device type from either core or agent
  --enable-extra-drive  Flag if the device has a USB storage plugged in
  --output PATH         File path to create an Ansible script
```

**Examples**
- If you are making your Jetson as Waggle core device with a USB drive,
```bash
python3 create_ansible.py --type core --enable-extra-drive
```
```bash
Creating Ansible script for core
Extra drive is enabled
Creating Ansible at my_ansible.yaml...
Done
```

- If you are making your Jetson as Waggle agent device without a USB drive,
```bash
python3 create_ansible.py --type agent
```
```bash
Creating Ansible script for agent
Creating Ansible at my_ansible.yaml...
Done
```

2. Run created Ansible,
```
ansible-playbook -i ansible_inventory my_ansible.yaml
```

##### Your Jetson can now run WES!

Continue to [Configuring the Sensors](./configure_sensors.md)