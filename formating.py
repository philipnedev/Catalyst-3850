#!/usr/bin/python
'''
Formating the output for improve appearance and usability
'''

def print_menu_title(text):
    '''Print the given text with line of dashes above and bellow.
    Size of dashed line in related to the lenght of the text

    Args:
        text - string - that we want to print

    Returns:
        Nothing
    '''
    print (len(text) + 2) * "-"
    print " " + text
    print (len(text) + 2) * "-"


def print_menu_items(menu_list):
    '''Print the given list of items as a menu with number infront of every item

        Args:
            menu_list - list - items that we want to print

        Returns:
            Nothing
        '''
    lenght = 0

    for index,item in enumerate(menu_list):
        print "{0}. {1}".format(index+1, item)
        if len(item) > lenght:
            lenght = len(item)

    print"q. Quit"

    print (lenght+4) * "-"


