#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
A simple script to query LDAP and print emails. With export possibility to
CSV format, e.g. for importing into Thunderbird Mail

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
    conn.unbind()
    return mail_list


def print_list(mail_list):
    print(', '.join(map(str, mail_list)))


def print_csv(mail_list):
    row = ["First Name", " Last Name", " Display Name", " Nickname", " Primary Email", " Secondary Email", " Work Phone", " Home Phone", " Fax Number", " Pager Number", " Mobile Number", " Home Address", " Home Address2", " Home City", " Home State", " Home Zipcode", " Home Country",
           " Work Address", " Work Address2", " Work City", " Work State", " Work Zip", " Work Country", " Job Title", " Department", " Organization", " Web Page 1", " Web Page 2", " Birth Year", " Birth Month", " Birth Day", " Custom 1", " Custom 2", " Custom 3", " Custom 4", " Notes"]
    print(', '.join(map(str, row)))
    for item in mail_list:
        print(',' * 4 + item + ',' * 31)


# ----
if __name__ == '__main__':
    passwd = getpass('Password for {} @ {} :'.format(username, server_address))
    for arg in sys.argv[1:]:
        mail_list = main(arg, passwd)

    if sys.argv[1] == '--csv':
        print_csv(mail_list)
    elif sys.argv[1] == '--list':
        print_list(mail_list)
    else:
        print('Please provide either --csv or --list')
