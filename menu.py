#!/usr/bin/python
import os

import devices_configuration
import hostname

sw_3850_1 = {
        'device_type': 'cisco_ios',
        'ip': '10.24.1.131',
        'username': 'pnedev',
        'password': '165779',
        'building': 'Sofia',
        'floor': '2'
}

sw_3850_2 = {
        'device_type': 'cisco_ios',
        'ip': '10.24.1.128',
        'username': 'pnedev',
        'password': '165779',
        'building': 'Sofia',
        'floor': '2'
}

sw_3850_3 = {
        'device_type': 'cisco_ios',
        'ip': '10.24.1.129',
        'username': 'pnedev',
        'password': '165779',
        'building': 'Sofia',
        'floor': '3'
}
devices = [sw_3850_1, sw_3850_2, sw_3850_3]

configurations = devices_configuration.get_all_configs(devices)


while True:
    os.system('clear')
    print 6*"-"
    print "Menu"
    print 6*"-"
    print "1.Hostname"
    print "q.Quit"
    choice = raw_input("Select Option:")
    if choice == "1":
        hostname.menu_hostname(devices, configurations)
    elif choice == "q":
        break
