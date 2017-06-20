#!/usr/bin/python
# ----------------------------------------------
from netmiko import ConnectHandler
import os
from prettytable import PrettyTable
from devices_configuration import get_device_config

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

def print_hostnames(devices, skip=False):
    os.system('clear')
    pt = PrettyTable(["N", "Hostname", "IP Address","Building", "Floor"])
    pt.align["Hostname"] = "c"
    pt.padding_width = 1
    i = 1
    list = {}
    for device in devices:
        pt.add_row([i, device, get_hostname(devices[device]['config']),devices[device]['building'],devices[device]['floor']])
        list[str(i)] = device
        i+=1

    print pt
    if skip == False:
        raw_input("Press any key to continue")
    return list

def set_hostname(devices):
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
    list = print_hostnames(devices, True)
    switch_number = raw_input("Please enter switch number: ")
    new_hostname = raw_input("Please enter new name: ")

    net_connect = ConnectHandler(**devices[list[switch_number]]["connection"])
    command = 'hostname ' + new_hostname
    config_commands = [command]
    try:
        print "Changing hostname ...(it takes some time)"
        net_connect.send_config_set(config_commands)
        net_connect.disconnect()
    except:
        net_connect.disconnect()
    devices[list[switch_number]]["config"] = get_device_config(devices[list[switch_number]]["connection"])

def menu_hostname(devices):
    while True:
        os.system('clear')
        print 9 * "-"
        print "Hostname"
        print 9 * "-"
        print "1.List device hostnames"
        print "2.Change device hostname"
        print "q.Quit"

        choice = raw_input("Select Hostname Option:")

        if choice == "1":
            print_hostnames(devices)

        elif choice == "2":
            set_hostname(devices)

        elif choice == "q":
            break
