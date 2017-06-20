#!/usr/bin/python
import re
from prettytable import PrettyTable

def file_to_list(file_name):
    lines = []
    with open(file_name) as file:
        for line in file: #low memory consumption iterator. even TB files can be read on a standard laptop.
            line = line.strip() #or some other preprocessing
            lines.append(line)
    return lines

def split_same_elemets(list):

    interface = []
    interfaces = []
    count = 0
    for line in lines:
        if line == "!":
            interfaces.append(interface)
            count = count + 1
            interface = []
        if line != "!":
            interface.append(line)

    return interfaces


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


lines = file_to_list("interfaces.txt")
interfaces = split_same_elemets(lines)

for i,item in enumerate(interfaces):
    interfaces[i] = raw_list_to_dictionary(item)


x = PrettyTable(["Type", "Number", "Description", "Mode", "VLAN","Voice","STP_PF","BPDU Guard"])
x.align["Type"] = "c"
x.padding_width = 1

for i in interfaces:
    x.add_row([i["type"],i["number"],i["description"],i["mode"],i["access_vlan"],i["voice_vlan"],i["stp_portfast"],i["stp_bpdug"]])

print
print x
print




