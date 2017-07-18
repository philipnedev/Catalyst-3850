#!/usr/bin/python
'''
Prints the initial menu and takes the choice of action.
'''
import os
import formating
import hostname
from netmiko import ConnectHandler
from prettytable import PrettyTable


def get_show_command(device,command):
    if not command.startswith("show"):
        return (False, [])


    try:
        net_connect = ConnectHandler(**device)
        output = net_connect.send_command(command)
        net_connect.disconnect()

        output = output.splitlines()
        lines = []

        for line in output:  # low memory consumption iterator. even TB files can be read on a standard laptop.
            line = line.rstrip().encode('ascii','ignore')  # or some other preprocessing
            lines.append(line)

        return (True, lines)

    except:

        return (False, [])

#!/usr/bin/python
def file_to_list(file_name):
    lines = []
    with open(file_name) as file:
        for line in file: #low memory consumption iterator. even TB files can be read on a standard laptop.
            line = line.strip() #or some other preprocessing
            lines.append(line)
    return lines

def trim_show_cdp(list):
    start = 0
    stop = 0
    for index, line in enumerate(list):
        if line.startswith("Device ID"):
            start = index + 1
        if len(line) == 0 and start > 0:
            stop = index
    if stop != 0:
        return list[start:stop]
    else:
        return False

def normalize_show_cdp(list):
    list = trim_show_cdp(list)

    for index, line in enumerate(list):
        list[index] = line.split()

    count = 0
    exception = False
    new_list = []

    for line in list:
        if len(line) == 1:
            exception = True
            new_list.append(line)
            continue

        if exception == True:
            exception = False
            new_list[count] = new_list[count] + line
            count += 1
            continue

        new_list.append(line)
        count += 1

    list = []

    for line in new_list:
        list.append(line[0:3]+line[-3:])

    return list

def show_cdp(devices):
    for device in devices:
        success, output = get_show_command(devices[device]["connection"], "show cdp neighbors")
        if success:
            print " "
            print hostname.get_hostname(devices[device]['config']) + " CDP Neighbors"
            print " "
            pt = PrettyTable(["Device", "Local Interface", "Remote Interface"])
            pt.align["Device"] = "c"
            pt.padding_width = 1
            cdp_data = normalize_show_cdp(output)
            for line in cdp_data:
                pt.add_row([line[0], line[1]+line[2], line[4]+line[5]])
            print pt
            print " "




def menu(devices):
    os.system('clear')
    list = hostname.print_hostnames(devices, True)

    while True:
        menu = [
            "show running-config",
            "CDP",
            "Custom"
        ]

        formating.print_menu_title("Menu - Show Commands")
        formating.print_menu_items(menu)

        choice = raw_input("Select show commands option:")

        if choice == "q":
            break
        try:
            choice = int(choice) - 1
            if menu[choice] == "show running-config":
                question = "Which switch:"
                print len(question)*"-"
                switch = raw_input(question)
                for line in devices[list[switch]]["config"]:
                    print line
                raw_input("Press Enter to go back...")

            elif menu[choice] == "CDP":
                show_cdp(devices)
                raw_input("Press Enter to go back...")

            elif menu[choice] == "Custom":
                question = "Which switch:"
                print len(question) * "-"
                switch = raw_input(question)
                command = raw_input("Type show command:")
                success, output = get_show_command(devices[list[switch]]["connection"], command)
                if success:
                    for line in output:
                        print line
        except:
            pass