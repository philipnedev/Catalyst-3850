#!/usr/bin/python
'''
Prints the initial menu and takes the choice of action.
'''
import os
import devices_configuration
import hostname
import vlans
import interfaces
import formating


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

    }
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
'''

devices = devices_configuration.get_all_configs(devices)

while True:
    menu = [
        "Hostname",
        "VLAN",
        "Interfaces",
    ]

    os.system('clear')
    formating.print_menu_title("Menu - Actions")
    formating.print_menu_items(menu)

    choice = raw_input("Select Option:")
    if  choice == "q":
        break
    try:
        choice = int(choice) - 1
        if menu[choice] == "Hostname":
            hostname.menu_hostname(devices)
        if menu[choice] == "VLAN":
            vlans.menu(devices)
        if menu[choice] == "Interfaces":
            interfaces.menu(devices)
    except:
        pass