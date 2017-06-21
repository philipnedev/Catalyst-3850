#!/usr/bin/python
from netmiko import ConnectHandler

def get_device_config(device):
    net_connect = ConnectHandler(**device)
    output = net_connect.send_command("show running-config")
    net_connect.disconnect()

    output = output.splitlines()
    lines = []

    for line in output:  # low memory consumption iterator. even TB files can be read on a standard laptop.
        line = line.rstrip().encode('ascii','ignore')  # or some other preprocessing
        lines.append(line)

    return lines

def get_all_configs(devices):
    print "Start configurations collection:"
    configurations = {}
    for device in devices:
        devices[device]["config"] = get_device_config(devices[device]["connection"])
        if devices[device]["config"][0] == "Building configuration...":
            print "Collecting ", devices[device]["connection"]["ip"], "...","OK"
        else:
            print "Collecting ", devices[device]["connection"]["ip"], "...","FAIL"

    return devices

