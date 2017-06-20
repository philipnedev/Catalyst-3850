#!/usr/bin/python
from netmiko import ConnectHandler

def get_device_config(device):
    print "Collecting ", device["ip"], "..."
    net_connect = ConnectHandler(**device)
    output = net_connect.send_command("show running-config")
    net_connect.disconnect()

    output = output.splitlines()
    lines = []

    for line in output:  # low memory consumption iterator. even TB files can be read on a standard laptop.
        line = line.strip().encode('ascii','ignore')  # or some other preprocessing
        lines.append(line)

    return lines

def get_all_configs(devices):
    print "Start configurations collection:"
    configurations = {}
    for device in devices:
        configurations[device["ip"]] = get_device_config(device)

    return configurations

