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
                        default='secrets.vault')
    args, options = parser.parse_args()

    vaultfile = os.environ.get("VAULTFILE", None)
    if vaultfile is None:
        vaultfile = args.vault_file
    if not os.path.isfile(vaultfile):
        sys.stderr.write("No ansible vault found in %s. Either create one or set the environment variable VAULTFILE.\n" % vaultfile)
        sys.exit(3)

    vaultpass = os.environ.get("VAULTPASS", None)
    if vaultpass is None:
        sys.stderr.write("Set the VAULTPASS environment variable to unlock the ansible vault.\n")
        sys.exit(3)
    password = open(vaultpass).read().strip()

    vault = Vault(password)
    data = vault.load(open(vaultfile).read())

    cmd = ["terraform", args.action, "--var", "environment=%s" %args.environment ]

    for key, value in data.items():
        cmd.append("--var '{}={}'".format(key, value))

    cmd += string.join(options)
    x = os.system(string.join(cmd))
    sys.exit(x)
