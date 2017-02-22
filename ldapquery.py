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
server_name = 'server:port'
org_name = '@example.net'


def main(pattern, passwd):
    server = Server(server_name, get_info=ALL)
    conn = Connection(server)
    conn.bind()
    conn = Connection(server, 'uid={},cn=users,dc=gsi,dc=de'.format(username), passwd, auto_bind=True,
                      authentication=NTLM)
    # print(conn)
    # print(server.info)
    conn.search('cn=users,dc=gsi,dc=de', '(|(cn=*{}*)(givenName=*{}*))'.format(pattern, pattern))
    for entry in conn.entries:
        tx = entry.entry_dn
        mail = tx.split(',')[0].split('=')[1]
        if '@' not in tx:
            mail += org_name
        print(mail)
    conn.unbind()


# ----
if __name__ == '__main__':
    passwd = getpass('Password for {} @ {} :'.format(username, server_name))
    for arg in sys.argv:
        main(arg, passwd)
