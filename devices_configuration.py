#!/usr/bin/python
'''
Collecting and saving single or multiple device configurations
'''

from netmiko import ConnectHandler

def get_device_config(device):
    '''Connects to device via SSH and collects the configuration.

        Args:
            device - dictionary with the connection parameters - netmiko format
            {
            'username': '<USERNAME>',
            'ip': '<IP ADDRESS>',
            'device_type': '<TYPE OS>',
            'password': '<PASSWORD>'
            }

        Returns:
            (True/False, lines) - tuple
                True/False - if the configuration was collected
                lines - list - running-config in list format
    '''
    try:
        net_connect = ConnectHandler(**device)
        output = net_connect.send_command("show running-config")
        net_connect.disconnect()

        output = output.splitlines()
        lines = []

        for line in output:  # low memory consumption iterator. even TB files can be read on a standard laptop.
            line = line.rstrip().encode('ascii','ignore')  # or some other preprocessing
            lines.append(line)

        return (True, lines)

    except:

        return (False, [])

def get_all_configs(devices):
    '''Goes throught list of devices, connects to them, collects the running-config and adds it to the device

            Args:
                devices - list of devices in the format:
                '<IP ADDRESS>': {
                    'connection':{
                        'username': '<USERNAME>',
                        'ip': '<IP ADDRESS>',
                        'device_type': '<OS TYPE>',
                        'password': '<PASSWORD>'

                    },
                    'building': '<BUILDING LOCATION>',
                    'floor': '<FLOOR NUMBER>'

                }

            Returns:
                devices - returns all devices with added configuration to them under key "config"
                if devices was unsuccessfully connected it is removed from the list
        '''
    print "Start configurations collection:"
    failed_device = []
    for device in devices:
        result, devices[device]["config"] = get_device_config(devices[device]["connection"])
        if result:
            print "Collecting ", devices[device]["connection"]["ip"], "...","OK"
        else:
            print "Collecting ", devices[device]["connection"]["ip"], "...","FAILED"
            failed_device.append(device)

    for item in failed_device:
        del devices[item]

    return devices

