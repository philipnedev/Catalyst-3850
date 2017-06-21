#!/usr/bin/python
import os

import devices_configuration
import hostname
import vlans
'''
devices = {
    '10.24.1.131': {
        'connection':{
            'username': 'pnedev',
            'ip': '10.24.1.131',
            'device_type': 'cisco_xe',
            'password': '165779'

            },
        'building': 'Sofia',
        'floor': '2'

    },
}

'''
devices = {
    '10.24.1.128': {
        'connection':{
            'username': 'pnedev',
            'ip': '10.24.1.128',
            'device_type': 'cisco_xe',
            'password': '165779'
            },
        'building': 'Sofia',
        'floor': '2'

    },
    '10.24.1.129': {
        'connection':{
            'username': 'pnedev',
            'ip': '10.24.1.129',
            'device_type': 'cisco_xe',
            'password': '165779'
        },
        'building': 'Sofia',
        'floor': '2'
    },
    '10.24.1.131': {
        'connection':{
            'username': 'pnedev',
            'ip': '10.24.1.131',
            'device_type': 'cisco_xe',
            'password': '165779'
        },
        'building': 'Sofia',
        'floor': '1'
    }
}


devices = devices_configuration.get_all_configs(devices)

while True:
    os.system('clear')
    print 6*"-"
    print "Menu"
    print 6*"-"
    print "1.Hostname"
    print "2.VLAN"
    print "q.Quit"
    choice = raw_input("Select Option:")
    if choice == "1":
        hostname.menu_hostname(devices)
    if choice == "2":
        vlans.menu(devices)
    elif choice == "q":
        break
