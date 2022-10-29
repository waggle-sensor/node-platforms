import argparse

CORE = "core"
AGENT = "agent"

def main(args):
    print(f'Creating Ansible script for {args.type}')


    script = """
---
- name: Set up root access
  ansible.builtin.import_playbook: root_access.yaml

- name: Check Jetpack version
  ansible.builtin.import_playbook: ansible_check_jetpack.yaml
"""
    if args.extra_drive:
        print("Extra drive is enabled")
        script += """
- name: Set up extra drive
  ansible.builtin.import_playbook: ansible_setup_extra_drive.yaml
"""
    else:
        script += """
- name: Create /media for storage
  ansible.builtin.file:
    path: /media
    state: directory
    mode: '0755'
"""
    if args.type == CORE:
        script += """
- name: Install Tools for core
  ansible.builtin.import_playbook: ansible_install_tools_core.yaml

- name: Remove Uneeded Items for core
  ansible.builtin.import_playbook: ansible_remove_unneeded_items_core.yaml

- name: Configure ROOTFS for core
  ansible.builtin.import_playbook: ansible_copy_rootfs_core.yaml

- name: Configure docker
  ansible.builtin.import_playbook: ansible_configure_docker.yaml

- name: Configure k3s for core
  ansible.builtin.import_playbook: ansible_configure_k3s_core.yaml

- name: Configure local registry for core
  ansible.builtin.import_playbook: ansible_configure_local_registry_core.yaml

- name: Configure Waggle edge stack for core
  ansible.builtin.import_playbook: ansible_configure_wes_core.yaml
"""
    else:
        script += """
- name: Install Tools for agent
  ansible.builtin.import_playbook: ansible_install_tools_agent.yaml

- name: Remove Uneeded Items for agent
  ansible.builtin.import_playbook: ansible_remove_unneeded_items_agent.yaml

- name: Configure ROOTFS for agent
  ansible.builtin.import_playbook: ansible_copy_rootfs_agent.yaml

- name: Configure docker
  ansible.builtin.import_playbook: ansible_configure_docker.yaml

- name: Configure k3s for agent
  ansible.builtin.import_playbook: ansible_configure_k3s_agent.yaml

- name: Configure Waggle edge stack for agent
  ansible.builtin.import_playbook: ansible_configure_wes_agent.yaml
"""
    print(f'Creating Ansible at {args.path}...')
    with open(args.path, "w") as file:
        file.write(script)
    print("Done")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--type",
        dest="type",
        choices=[CORE, AGENT],
        required=True,
        help="Specify Waggle device type from either core or agent")
    parser.add_argument("--enable-extra-drive",
        dest="extra_drive",
        action="store_true",
        help="Flag if the device has a USB storage plugged in")
    parser.add_argument("--output",
        dest="path",
        default="my_ansible.yaml",
        help="File path to create an Ansible script")
    main(parser.parse_args())