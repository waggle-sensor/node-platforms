## Setting up Ansible on your computer

This guide will go through installing ansible on your computer, creating a ssh-key pair with the nano, cloning this repository, and configuring the `ansible_inventory` file.

**Required skills:** 
* Using command line interface for your computer
* Editing a file using Vim
* Cloning a GitHub repository

**Helpful guides:**
* [Cloning a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)

---

> Note: `ansible` is _not_ needed on the Nano in order to perform `ansible` provisioning.


1. On your computer, install Ansible

    1. Intructions for Linux

        1. Open a terminal and install pip

            1. Within the terminal, install python 3 and related packages using the command  
                `sudo apt install python3-pip python3-dev`

            2. Make sure to have every package on your system up-to-date so there aren't any dependency issues:  
                `sudo apt update`  
                `sudo apt upgrade`

            3. Upgrade pip by running:  
                `python3 -m pip install --upgrade pip`

        2. Within the terminal, install Ansible using the command `sudo pip install ansible`

        3. You can test that Ansible is installed correctly by checking the version:
            `ansible --version`

    2. Instructions for Macos

        1. Open a terminal and install Homebrew via this command:
            ```
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            ```
        > Dev Note: check if you need to add Homebrew shell configuration for apple silicon machines
        1. You can test that Homebrew is installed correctly by checking the version: 
            `brew --version`

        2. Within the terminal, install Ansible using the command 
            `brew install ansible`

        3. You can test that Ansible is installed correctly by checking the version:
            `ansible --version`

    3. Instructions for Windows

        1. You cannot use a Windows system for the Ansible control node, so you need to install Windows Subsystem for Linux (WSL)

            1. Prerequisites

                - You must be running Windows 10 version 2004 and higher (Build 19041 and higher) or Windows 11.
                > Note: To check your Windows version and build number, select Windows logo key + R, type winver, select OK. You can update to the latest Windows version by selecting Start > Settings > Windows Update > Check for updates.

            2. You can now install everything you need to run Windows Subsystem for Linux (WSL) by entering this command in Windows Command Prompt
                `wsl --install`

            3. Restart your computer.
        
        2. Once you have installed WSL, you will need to create a user account and password for Ubuntu

            1. You can directly open Ubuntu by visiting the Windows Start menu and typing `Ubuntu`

            2. Once you open Ubuntu, follow the on screen instructions to set up a user account

            3. You are now in Ubuntu's command line!

        3. Installing pip

            1. Within the Ubuntu terminal, install python 3 and related packages using the command  
                `sudo apt install python3-pip python3-dev`

            2. Make sure to have every package on your system up-to-date so there aren't any dependency issues:  
                `sudo apt update`  
                `sudo apt upgrade`

            3. Upgrade pip by running:  
                `python3 -m pip install --upgrade pip`

        4. Within the Ubuntu terminal, install Ansible using the command `sudo pip install ansible`

        5. You can test that Ansible is installed correctly by checking the version:
            `ansible --version`
        >Note: Everytime you need to need to use a terminal for the preceding instructions open Ubuntu by visiting the Windows Start menu and typing `Ubuntu`

2. Set up ssh-keypair with the Jetson Nano

    1. Open a terminal and run the command `ssh-keygen` to create a ssh-key

        1. When asked to enter a file in which to save the key, copy the file path inside the parenthesis ex; `/Users/flozano/.ssh/id_rsa`. Then leave the entry blank and press enter to keep the default file.

        2. If asked to overwrite press `y` and then enter

        3. If asked to enter in a passphrase leave it blank and press enter

    2. Share the ssh-key with your Jetson Nano following this command template
        ```
        ssh-copy-id -i {file path} root@{ip}
        ```
    
    3. After you have replaced `{file path}` with the file path you just coppied and replaced `{ip}` with your Jetson Nano's ip address you can now run the command to share the ssh-key
        - Example
            ```
            ssh-copy-id -i /Users/flozano/.ssh/id_rsa root@130.202.141.76
            ```

3. Open a terminal and travel to your home directory `cd ~`

4. Clone this repository using this command:
    ```
    git clone https://github.com/waggle-sensor/node-platforms.git
    ```

5. Travel into the folder that is holding the Ansible Playbook using this command:
    ```
    cd ~/node-platforms/nvidia-nano
    ```
>Note: Everytime you run an ansible commmand make sure you are in this directory

6. Replace `{ip}` in the `ansible_inventory` file with your Jetson Nano's ip address using vim or any other text editor program
    - After it is replaced it should look similiar to this
        ```
        [nano]
        0.0.0.0 ansible_user=root
        ```

7. You can now test if the Ansible script can reach your Jetson Nano via this command:
    ```
    ansible all -i ansible_inventory -m ping
    ```

Continue to [Running The Ansible Playbook](./running_ansible.md)