#!/usr/bin/python
from netmiko import ConnectHandler
import os
from prettytable import PrettyTable


"""Finding the VLAN information in running-config and convert it to structured format"""


def file_to_list(file_name):
    '''Returnst file in a list format
    Args:
        File name
    Returns:
        list:Text lines are the elements of the list
    '''
    lines = []
    with open(file_name) as file:
        for line in file: #low memory consumption iterator. even TB files can be read on a standard laptop.
            line = line.strip() #or some other preprocessing
            lines.append(line)
    return lines


def get_vlans_from_config(list):
    '''Cut the VLAN part from running-config
        Args:
            list:running-config in list format
        Returns:
            list:VLAN part of the running config
    '''
    start = 0
    stop = 0
    check = 0

    for i,line in enumerate(list):
        if line.startswith("vlan") and start == 0 and len(line) < 10:
            start = i

        elif line.startswith("vlan") and start != 0:
            check = 0

        elif line == "!" and start != 0:
            check = 1
            stop = i - 1
            print line
            raw_input()
        elif start != 0 and check == 1:
            print line
            raw_input()
            break
    return list[start:stop]

def convert_raw_vlans_to_list(list):
    '''Converts VLAN part of the running-config in structured data
        Args:
            list:VLAN part of the running config
        Returns:
            list:with elent dictionary containing elements
                "number": number of the VLAN
                "name": name of the VLAN (None if there is no name)
                
    '''
    vlan = []
    vlans = []
    for line in list:
        if line == "!":
            vlans.append(vlan)
            vlan = []
        if line != "!":
            vlan.append(line)
    items = vlans

    vlan = {}
    vlans = []

    for i,item in enumerate(items):
        vlan["name"] = None
        for a in item:
            if a.startswith("vlan"):
                vlan["number"] = a.split()[1]

            if a.startswith("name"):
                vlan["name"] = a.split()[1]

        vlans.append(vlan)
        vlan = {}

    return vlans




def get_vlan_interface(vlan_list, config):
    for i, vlan in enumerate(vlan_list):
        vlan_list[i]["ip address"] = None
        vlan_list[i]["description"] = None
        try:
            position_start = config.index("interface Vlan"+vlan["number"])
            position_end = config.index("!", position_start)
            for line in config[position_start:position_end]:
                if line.startswith("ip address"):
                    vlan_list[i]["ip address"] = line.split()[2]
                elif line.startswith("description"):
                    vlan_list[i]["description"] = line[len("description") + 1:]


        except:
            pass

def get_vlans_for_switch(device):

    net_connect = ConnectHandler(**device)
    output = net_connect.send_command("show vlan brief")
    net_connect.disconnect()
    output = output.splitlines()
    lines = []
    output = [x for x in output if x]

    for line in output:  # low memory consumption iterator. even TB files can be read on a standard laptop.
        line = line.strip().encode('ascii', 'ignore')  # or some other preprocessing
        try:
            int(line.split()[0])
            if int(line.split()[0]) not in [1002,1003,1004,1005]:
                lines.append(line.split()[0])
        except:
            pass

    return lines

def vlan_to_switch_mapping(devices):
    allvlans = []
    for device in devices:
        allvlans = list(set(devices[device]["vlans"]+allvlans))
    allvlans.sort()
    allvlans.insert(0," ")
    pt = PrettyTable(allvlans)
    pt.padding_width = 1

    for device in devices:
        #pt.align["Hostname"] = "c"
        match = []
        match.append(device)
        for vlan in allvlans[1:]:
            if vlan in devices[device]['vlans']:
                match.append('YES')
            else:
                match.append('NO')
        pt.add_row(match)

    print pt
    raw_input("Press any kay to continue...")

def add_vlan(devices):
    vlan_number = raw_input("Please enter VLAN number: ")
    vlan_name = raw_input("Please enter VLAN name: ")
    for device in devices:
        net_connect = ConnectHandler(**devices[device]["connection"])
        command1 = 'vlan ' + vlan_number
        command2 = 'name ' + vlan_name
        command3 = 'exit '
        config_commands = [command1,command2, command3]

        print "Add/change VLAN ", vlan_number , " on ", device
        net_connect.send_config_set(config_commands)
        net_connect.disconnect()

def menu(devices):
    print "Collecting VLAN information ..."
    for device in devices:
        print "Collecting from ", device
        devices[device]['vlans'] = get_vlans_for_switch(devices[device]["connection"])

    while True:
        os.system('clear')
        print 9 * "-"
        print "VLANs"
        print 9 * "-"
        print "1.VLAN to switches mapping"
        print "2.Add VLAN"
        print "q.Quit"

        choice = raw_input("Select VLAN Option:")

        if choice == "1":
            vlan_to_switch_mapping(devices)

        elif choice == "2":
            add_vlan(devices)

        elif choice == "q":
            break






