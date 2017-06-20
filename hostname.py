#!/usr/bin/python
# ----------------------------------------------
from netmiko import ConnectHandler
import os
from prettytable import PrettyTable


# ----------------------------------------------

'''Finding and configuring IOS device hostname'''


def get_hostname(configuration):
    '''Returns the device hostname
       Args:
           Device configuration
       Returns:
           string:Device hostname
       '''
    hostname = None
    for line in configuration:
        if line.startswith("hostname "):
            hostname = line.split()[1]

    return hostname

def print_hostnames(configs,devices):
    os.system('clear')
    pt = PrettyTable(["Hostname", "IP Address","Building", "Floor"])
    pt.align["Hostname"] = "c"
    pt.padding_width = 1

    for ip_address in configs:
        pt.add_row([ip_address, get_hostname(configs[ip_address])])

    print pt

    a = raw_input("Press any key to continue")


def set_hostname(device, new_hostname):
    '''Configures new hostname to device
    Args:
        device:Dictionary in to form:
            sw_3850 = {
            'device_type': 'cisco_ios',
            'ip': '10.24.1.131',
            'username': 'pnedev',
            'password': '165779'
            }
        new_hostname: string: The new hostname for the device
       Returns:
           True of False
    '''
    net_connect = ConnectHandler(**device)
    command = 'hostname ' + new_hostname
    config_commands = [command]
    output = net_connect.send_config_set(config_commands)
    net_connect.disconnect()

def menu_hostname(devices, configs):
    while True:
        os.system('clear')
        print 9 * "-"
        print "Hostname"
        print 9 * "-"
        print "1.List device hostnames"
        print "2.Change device hostnames"
        print "q.Quit"

        choice = raw_input("Select Hostname Option:")

        if choice == "1":
            print_hostnames(configs,devices)
        elif choice == "2":
            print "choice 2"
            a = raw_input()
        if choice == "q":
            break
