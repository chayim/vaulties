# Vaulties

This repository contains a wrapper script for [terraform](https://www.terraform.io/), making it easy to inject variables into a terraform run from an [ansible vault](https://docs.ansible.com/ansible/latest/user_guide/vault.html). Ditto a vagrant wrapper, making it easier to drive vagrant and terraform from a single encrypted source.

## Tooling

I follow standard python practices:

* [pyenv](https://github.com/pyenv/pyenv) is used to manage the python version
* Given the single package requirement, *pip install -r requirements.txt* is your friend, but first create a dedicated virtualenv.

## Examples

* VAULTFILE=/path/to/file VAULTPASS=yourvaultpassword python terrarist.py -a plan -x

* VAULTFILE=/path/to/file VAULTPASS=yourvaultpassword python terrarist.py -a apply