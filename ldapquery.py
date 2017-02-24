#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
A simple script to query LDAP and print emails

2017

Xaratustrah

"""

from ldap3 import Server, Connection, ALL, NTLM
from getpass import getpass
import sys

username = 'domain\\user'
server_address = 'server:port'
org_name = '@example.net'
options = 'cn=users,dc=example,dc=net'


def main(pattern, passwd):
    server = Server(server_address, get_info=ALL)
    conn = Connection(server, 'uid={},cn=users,dc=gsi,dc=de'.format(username), passwd, auto_bind=True,
                      authentication=NTLM)
    conn.search(options, '(|(cn=*{}*)(givenName=*{}*))'.format(pattern, pattern))
    mail_list = []
    for ent in conn.entries:
        tx = ent.entry_dn
        mail = (tx.split(',')[0].split('=')[1])
        if '@' not in tx:
            mail += org_name
        mail_list.append(mail)
    print(', '.join(map(str, mail_list)))
    conn.unbind()


# ----
if __name__ == '__main__':
    passwd = getpass('Password for {} @ {} :'.format(username, server_address))
    for arg in sys.argv:
        main(arg, passwd)
