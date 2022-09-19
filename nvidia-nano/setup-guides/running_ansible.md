## Running the Ansible Playbook

This guide will show how to run the Ansible Playbook

**Required Skills:**
* Using the Command Line Interface of your computer

---

Ansible should now be set up to run the playbook that will configure your nano to run Waggle Edge Stack (WES). 

Stuff to keep in mind while the ansible script runs:

- **Don't play with the nano while the playbook runs**. It can mess it up!

- **Don't leave your desk while the playbook runs**! The playbook will give you more instructions on what to do as it runs

- If you are connecting over wifi it can cause the ansible playbook to disconnect when the nano reboots, so having both the nano and your computer on ethernet connections is reccomended

- Connect your hardware when the ansible playbook tells you to

- In the playbook output, `ok` in green means nothing was changed and `changed` in yellow means something was changed in the client (i.e. the Jetson Nano). **Anything in red means something failed and the playbook will stop executing**

- If the playbook fails, it is safe to re run it nothing will be duplicated

- The playbook will enable root ssh, so to connect to the nano in the future use the command `ssh root@<IP>`

In the **~/node-platforms/nvidia-nano** directory, run this command to start the playbook
```
ansible-playbook -i ansible_inventory 01_ansible_nvidia-nano_base.yaml 
```

##### Your nano can now run WES!

Continue to [Configuring the Sensors](./configure_sensors.md)