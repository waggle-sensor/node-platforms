## Installing Ansible on your Computer

This guide will go through installing ansible on your computer

**Required skills:** 
* Using the Command Line Interface of your computer

**Helpful Guides**
* [Command Line Interface (CLI) definition](https://www.techtarget.com/searchwindowsserver/definition/command-line-interface-CLI)
---

> Note: **ansible** is _not_ needed on the Nano in order to perform **ansible** provisioning; i.e., you do not need to install ansible on the nano.


1. On your computer, install Ansible

    1. Instructions for Linux

        1. Open a terminal and install pip

            1. Within the terminal, install python 3 and related packages using the command  
                `sudo apt install python3-pip python3-dev python3-paramiko`

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
        
        2. You can test that Homebrew is installed correctly by checking the version: 
            `brew --version`

        3. Within the terminal, install Ansible using the command 
            `brew install ansible`

        4. You can test that Ansible is installed correctly by checking the version:
            `ansible --version`

        5. Get pip to install a dependent package
            `brew install pip`
            
            `pip install paramiko`

    3. Instructions for Windows

        1. You cannot use a Windows system for the Ansible control node, so you need to install Windows Subsystem for Linux (WSL)

            1. Prerequisites

                - You must be running Windows 10 version 2004 and higher (Build 19041 and higher) or Windows 11.
                > Note: To check your Windows version and build number, select Windows logo key + R, type `winver`, select OK. You can update to the latest Windows version by selecting Start > Settings > Windows Update > Check for updates.

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
        >Note: Every time you need to need to use a terminal for the preceding instructions open Ubuntu by visiting the Windows Start menu and typing `Ubuntu`

##### Ansible is now installed!

Continue to [Configure Ansible](./configure_ansible.md)
