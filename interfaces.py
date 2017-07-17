#!/usr/bin/python
import re
import hostname
import os
from netmiko import ConnectHandler
import devices_configuration



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
    interface["shutdown"] = "No"

    for line in interface_cfg:
        line = line.strip()

        if line.startswith("interface"):
            interface["type"] = re.findall('[a-zA-Z]+', line.split()[1])[0].split("Ethernet")[0]
            interface["number"] = re.findall('[0-9].+', line.split()[1])[0]

        if line.startswith("description"):
            interface["description"] = line[len("description") + 1:]

        if line == "switchport mode access":
            interface["mode"] = "Access"

        if line == "switchport mode trunk":
            interface["mode"] = "Trunk"

        if line.startswith("switchport access vlan"):
            interface["access_vlan"] = line[len("switchport access vlan") + 1:]

        if line.startswith("switchport voice vlan"):
            interface["voice_vlan"] = line[len("switchport voice vlan") + 1:]

        if line.startswith("spanning-tree portfast"):
            interface["stp_portfast"] = "Yes"

        if line.startswith("spanning-tree bpduguard enable"):
            interface["stp_bpdug"] = "Yes"

        if line.startswith("shutdown"):
            interface["shutdown"] = "Yes"


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

    pt = PrettyTable(["Type", "Number", "Description", "Mode", "VLAN", "Voice", "STP_PF", "BPDU Guard","Shutdown"])
    pt.align["Type"] = "c"
    pt.padding_width = 1

    for i in device["interfaces"]:
        pt.add_row(
            [i["type"], i["number"], i["description"], i["mode"], i["access_vlan"], i["voice_vlan"], i["stp_portfast"], i["stp_bpdug"], i["shutdown"]])


    print pt
    raw_input("Press Enter to continue ...")

def interface_configuration(device,interface):
    pt = PrettyTable(["Type", "Number", "Description", "Mode", "VLAN", "Voice", "STP_PF", "BPDU Guard", "Shutdown"])
    pt.align["Type"] = "c"
    pt.padding_width = 1
    existance = False
    for i in device["interfaces"]:
        if i["number"] == interface:
            existance = True
            pt.add_row(
                [i["type"], i["number"], i["description"], i["mode"], i["access_vlan"], i["voice_vlan"], i["stp_portfast"],
                 i["stp_bpdug"], i["shutdown"]])
    if existance == True:
        print pt
        description = raw_input("Interface description:")
        data_vlan = raw_input("Data VLAN number:")
        voice_vlan = raw_input("Voice VLAN number (or n):")
        port_fast = raw_input("PortFast y-yes/n-any other:")
        bpdu_guard = raw_input("BPDUGuard y-yes/n-any other:")

        net_connect = ConnectHandler(**device["connection"])

        for i in device["interfaces"]:
            if i["number"] == interface:
                command1 = 'interface ' + i["type"] + i["number"]
                command2 = 'description ' + description
                command3 = 'switchport mode access'
                command4 = 'switchport access vlan ' + data_vlan
                if voice_vlan != 'n':
                    command5 = 'switchport voice vlan ' + voice_vlan
                else:
                    command5 = 'no switchport voice vlan '
                if port_fast == 'y':
                    command6 = 'spanning-tree portfast'
                else:
                    command6 = 'no spanning-tree portfast'
                if bpdu_guard == 'y':
                    command7 = 'spanning-tree bpduguard enable'
                else:
                    command7 = 'no spanning-tree bpduguard'

        config_commands = [command1, command2, command3, command4, command5, command6, command7]


        net_connect.send_config_set(config_commands)
        net_connect.disconnect()

    else:
        print "There is no such Swich/Interface combination"
    print "Finished configuration. Collecting result ..."

def interface_shutdown(device, interface, action):
    pt = PrettyTable(["Type", "Number", "Description", "Mode", "VLAN", "Voice", "STP_PF", "BPDU Guard", "Shutdown"])
    pt.align["Type"] = "c"
    pt.padding_width = 1
    existance = False
    for i in device["interfaces"]:
        if i["number"] == interface:
            existance = True
            pt.add_row(
                [i["type"], i["number"], i["description"], i["mode"], i["access_vlan"], i["voice_vlan"], i["stp_portfast"],
                 i["stp_bpdug"], i["shutdown"]])
    if existance == True:
        print pt

        net_connect = ConnectHandler(**device["connection"])

        for i in device["interfaces"]:
            if i["number"] == interface and action == 's':
                command1 = 'interface ' + i["type"] + i["number"]
                command2 = 'shutdown'
                config_commands = [command1, command2]

            elif i["number"] == interface and action == 'sn':
                command1 = 'interface ' + i["type"] + i["number"]
                command2 = 'shutdown'
                command3 = "no shutdown"
                config_commands = [command1, command2, command3]

        net_connect.send_config_set(config_commands)
        net_connect.disconnect()

    else:
        print "There is no such Swich/Interface combination"
    print "Finished configuration. Collecting result ..."

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
        print "2.Configure Access Interface"
        print "3.Configure Trunk Interface"
        print "4.Shutdown Interface"
        print "q.Quit"

        choice = raw_input("Select an Option:")
        print "-"*10

        if choice == "1":
            switch = raw_input("Which switch:")
            print_switch_interfaces(devices[list[switch]])
        elif choice == "2":
            switch = raw_input("Which switch:")
            interface = raw_input("Which interface [x/x/x]:")
            interface_configuration(devices[list[switch]],interface)
            devices[list[switch]]["config"] = devices_configuration.get_device_config(devices[list[switch]]["connection"])
            devices[list[switch]]["interfaces"] = get_interfaces_from_config(devices[list[switch]]['config'])
        elif choice == "4":
            switch = raw_input("Which switch:")
            interface = raw_input("Which interface [x/x/x]:")
            action = raw_input("s:shutdown | sn:shut/no shut:")

            interface_shutdown(devices[list[switch]], interface, action)
            devices[list[switch]]["config"] = devices_configuration.get_device_config(devices[list[switch]]["connection"])
            devices[list[switch]]["interfaces"] = get_interfaces_from_config(devices[list[switch]]['config'])


        elif choice == "q":
            break




