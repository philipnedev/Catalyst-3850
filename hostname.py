#!/usr/bin/python
# ----------------------------------------------
from netmiko import ConnectHandler
import formating
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
        raw_input("Press (Enter) to continue ...")
    return list

def set_hostname(devices):
    '''Configures new hostname to device
    Args:
        device:Dictionary in the form:
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
        menu = [
            "List devices hostnames",
            "Change device hostname"
        ]

        os.system('clear')
        formating.print_menu_title("Menu - Hostnames")
        formating.print_menu_items(menu)

        choice = raw_input("Select Hostname Option:")

        if choice == "q":
            break
        try:
            choice = int(choice) - 1
            if menu[choice] == "List devices hostnames":
                print_hostnames(devices)
            elif menu[choice] == "Change device hostname":
                set_hostname(devices)

        except:
            pass

