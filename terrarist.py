#!/usr/bin/env python

from optparse import OptionParser
import os
import subprocess
import string
import sys
from ansible_vault import Vault

if __name__ == "__main__":

    parser = OptionParser(description='Securely wrap terraform like a terrarist!')
    parser.add_option('-a', '--action', choices=['plan', 'apply', 'import'], help='Terraform action to execute', default='plan')
    parser.add_option('-v', '--vault', '--ansible-vault', dest='vault_file', help='Ansible Vault File',
                        default='terraform.vault')
    parser.add_option('-p', '--vault-password-file', dest='vault_password', help='Ansible Vault Password File',
                        default='vault.password')
    parser.add_option('-e', '--environment', dest='environment', help='Production, Staging, etc...', default='staging')

    args, options = parser.parse_args()

    if not os.path.isfile(args.vault_file):
        sys.stderr.write("Ansible vault file does not exist.\n")
        sys.exit(3)

    if not os.path.isfile(args.vault_password):
        sys.stderr.write("Ansible vault password does not exist.\n")
        sys.exit(3)

    password = open(args.vault_password).read().strip()

    vault = Vault(password)
    data = vault.load(open(args.vault_file).read())

    cmd = ["terraform", args.action, "--var", "environment=%s" %args.environment ]

    for key, value in data.items():
        cmd.append("--var '{}={}'".format(key, value))

    cmd += string.join(options)
    x = os.system(string.join(cmd))
    sys.exit(x)
