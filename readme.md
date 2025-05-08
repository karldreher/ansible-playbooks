# Ansible Playbooks
This repository collects ansible playbooks used for managing my own machines.

## Basic Usage
Typically playbooks within this repo are run locally.  The command below assumes allowing the `ansible.cfg` file to use the `inventory-local` folder to define inventory(which in this repo's case is localhost)

`ansible-playbook main.yml --extra-vars "email=EXAMPLE_EMAIL firstname=EXAMPLE_FIRSTNAME lastname=EXAMPLE_LASTNAME"`

It is **required** to set the `extra-vars` when running the playbook, as shown above.
Fill in the `EXAMPLE` values with ones meaningful for you.


## Tags
Some tags are used at the play level to describe what the tasks are doing.  They can be used to skip or include certain tasks using `--skip-tags` or `--tags` accordingly.

Current tags in use:

> packages
>
> prefs
>
