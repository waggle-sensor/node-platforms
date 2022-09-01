## Running The Ansible Playbook

This guide will show how to run the Ansible Playbook

**Required Skills:**
* Using command line interface

---

Ansible should now bet set up to run the playbook that will configure your nano to run Waggle Edge Stack (WES). 
In the `~/node-platforms/nvidia-nano` directory, run this command to start the playbook
```
ansible-playbook -i ansible_inventory 01_ansible_nvidia-nano_base.yaml 
```

Stuff to keep in mind while the ansible script runs:

- **Don't play with the nano while the playbook runs**. It can mess it up!

- **Don't leave your desk while the playbook runs**! The playbook will give you more instructions on what to do as it runs

- If you are ssh-ing over wifi it can cause the ansible playbook to disconnect when the nano reboots

- Connect your hardware when the ansible playbook tells you to

- In the playbook output, `ok` in green means nothing was changed and `changed` in yellow means something was changed in the client (i.e. the Jetson Nano). **Anything in red means something failed and the playbook will stop executing**

- If the playbook fails, it is safe to re run it nothing will be duplicated

##### Your nano can now run WES!

Continue to [Configuring the Sensors](./configure_sensors.md)