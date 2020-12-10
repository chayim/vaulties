#!/usr/bin/env python

from optparse import OptionParser
import os
import subprocess
import string
import sys
import yaml
from ansible.constants import DEFAULT_VAULT_ID_MATCH
from ansible.parsing.vault import AnsibleVaultError, VaultLib, VaultSecret


if __name__ == "__main__":

    parser = OptionParser(description='Securely wrap terraform like a terrarist!')
    parser.add_option('-a', '--action', choices=['plan', 'apply', 'import'], help='Terraform action to execute', default='plan')
    parser.add_option('-v', '--vault', '--ansible-vault', dest='vault_file', help='Ansible Vault File',
                        default='secrets.vault')
    parser.add_option('-x', '--debug', dest='DEBUG', action='store_true', help='Set, to print the command output, and not run.')

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

    vault = VaultLib([(DEFAULT_VAULT_ID_MATCH, VaultSecret(vaultpass.encode('utf-8')))])
    try:
        content = vault.decrypt(open(vaultfile).read())
    except AnsibleVaultError:
        sys.stderr.write("Invalid vault password, could not decrypt vault.\n")
        sys.exit(3)
    data = yaml.load(content, Loader=yaml.CLoader)

    cmd = ["terraform", args.action]

    for key, value in data.items():
        cmd.append("--var '{}={}'".format(key, value))

    cmd += options

    runcmd = ' '.join(cmd)
    if args.DEBUG:
        print(runcmd)
        sys.exit(0)

    x = os.system(runcmd)
    sys.exit(x)
