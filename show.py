#!/usr/bin/python
'''
Prints the initial menu and takes the choice of action.
'''
import os
import formating
import hostname
from netmiko import ConnectHandler

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

def menu(devices):
    os.system('clear')
    list = hostname.print_hostnames(devices, True)

    while True:
        menu = [
            "show running-config",
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