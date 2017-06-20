#!/usr/bin/python
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
        elif start != 0 and check == 1:
            break
    return lines[start:stop]

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



    for vlan in vlans:
        print vlan

#lines = file_to_list("shtech.txt")
lines = file_to_list("shtech.txt")
vlans = get_vlans_from_config(lines)
vlans = convert_raw_vlans_to_list(vlans)
get_vlan_interface(vlans,lines)





