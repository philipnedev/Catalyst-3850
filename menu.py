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
import show

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


devices = devices_configuration.get_all_configs(devices)

while True:
    menu = [
        "Hostnames",
        "VLAN",
        "Interfaces",
        "Show Commands"
    ]

    os.system('clear')
    formating.print_menu_title("Menu - Actions")
    formating.print_menu_items(menu)

    choice = raw_input("Select Option:")
    if  choice == "q":
        break
    try:
        choice = int(choice) - 1
        if menu[choice] == "Hostnames":
            hostname.menu(devices)
        elif menu[choice] == "VLAN":
            vlans.menu(devices)
        elif menu[choice] == "Interfaces":
            interfaces.menu(devices)
        elif menu[choice] == "Show Commands":
            show.menu(devices)

    except:
        pass