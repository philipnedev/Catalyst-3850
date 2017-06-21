#!/usr/bin/python
import re
import hostname
import os

from prettytable import PrettyTable


def file_to_list(file_name):
    lines = []
    with open(file_name) as file:
        for line in file: #low memory consumption iterator. even TB files can be read on a standard laptop.
            line = line.strip() #or some other preprocessing
            lines.append(line)
    return lines

def get_interfaces_from_config(config):
    '''Cut the interface part from running-config
        Args:
            list:running-config in list format
        Returns:
            list:interface part of the running config
    '''
    start = 0
    stop = 0


    for i,line in enumerate(config):
        if line.startswith("interface GigabitEthernet") and start == 0:
            start = i

        elif line.startswith("interface Vlan1") and start != 0:
            stop = i-1
            break

    return split_same_elemets(config[start:stop])

def raw_list_to_dictionary(interface_cfg):

    interface = {}

    interface["type"] = None
    interface["number"] = None
    interface["description"] = None
    interface["mode"] = None
    interface["access_vlan"] = None
    interface["voice_vlan"] = None
    interface["stp_portfast"] = "No"
    interface["stp_bpdug"] = "No"

    for line in interface_cfg:
        line = line.strip()

        if line.startswith("interface"):
            interface["type"] = re.findall('[a-zA-Z]+', line.split()[1])[0].split("Ethernet")[0]
            interface["number"] = re.findall('[0-9].+', line.split()[1])[0]

        if line.startswith("description"):
            interface["description"] = line[len("description") + 1:]

        if line == "switchport mode access":
            interface["mode"] = "Access"

        if line.startswith("switchport access vlan"):
            interface["access_vlan"] = line[len("switchport access vlan") + 1:]

        if line.startswith("switchport voice vlan"):
            interface["voice_vlan"] = line[len("switchport voice vlan") + 1:]

        if line.startswith("spanning-tree portfast"):
            interface["stp_portfast"] = "Yes"

        if line.startswith("spanning-tree bpduguard enable"):
            interface["stp_bpdug"] = "Yes"

    return interface

def split_same_elemets(config):

    interface = []
    interfaces = []
    count = 0
    for line in config:
        if line == "!":
            interfaces.append(interface)
            count = count + 1
            interface = []
        if line != "!":
            interface.append(line)

    for i, interface in enumerate(interfaces):
        interfaces[i]=raw_list_to_dictionary(interface)

    return interfaces

def print_switch_interfaces(device):

    pt = PrettyTable(["Type", "Number", "Description", "Mode", "VLAN", "Voice", "STP_PF", "BPDU Guard"])
    pt.align["Type"] = "c"
    pt.padding_width = 1

    for i in device["interfaces"]:
        pt.add_row(
            [i["type"], i["number"], i["description"], i["mode"], i["access_vlan"], i["voice_vlan"], i["stp_portfast"], i["stp_bpdug"]])

    print pt
    raw_input("Press Enter to continue ...")



def menu(devices):
    os.system('clear')
    list = hostname.print_hostnames(devices, True)
    for device in devices:
        devices[device]["interfaces"] = get_interfaces_from_config(devices[device]['config'])

    while True:
        print 11 * "-"
        print "Interfaces"
        print 11 * "-"
        print "1.Get switch interface information in"
        print "2.---"
        print "3.---"
        print "q.Quit"

        choice = raw_input("Select VLAN Option:")

        if choice == "1":
            switch = raw_input("Which switch:")
            print_switch_interfaces(devices[list[switch]])
        elif choice == "2":
            raw_input()
        elif choice == "3":
            raw_input()

        elif choice == "q":
            break

'''

x = PrettyTable(["Type", "Number", "Description", "Mode", "VLAN","Voice","STP_PF","BPDU Guard"])
x.align["Type"] = "c"
x.padding_width = 1

for i in interfaces:
    x.add_row([i["type"],i["number"],i["description"],i["mode"],i["access_vlan"],i["voice_vlan"],i["stp_portfast"],i["stp_bpdug"]])

print
print x
print

'''


