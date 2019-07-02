#   Diverse tools to work with supernovae
#
# This is my MAIN code file.
#--------------------------------------------------------60
code_created_by = 'Arturo_Avelino'
# On date: 2019.06.29 (yyyy.mm.dd)
code_name = 'mytoolsSNe.py'
version_code = '0.1.0'
last_update = '2019.06.29'
#--------------------------------------------------------60

import numpy as np
import datetime # Get the current date and time

#-----------------------------------------------------------------------------80
#       Function to convert between index and phase (days) in my
#       Gaussian-Processes light-curve files

shiftNum = 70

#- Function to convert from numpy index to days (phase).
def index2day(index):
    day = (index-shiftNum)/2.
    return day

#- Function to convert from days (phase) to numpy index.
def day2index(day):
    index = 2*day + shiftNum
    return int(index)

# print(index2day(70))
# print(day2index(0))

#-----------------------------------------------------------------------------80
#       Function to identify string or number

# Function to identify if a string is an integer number or a letter.
# This will be used in the dictionary construction to properly read some SN names.

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# Tests
# print(is_number('5'), is_number('e'))
# True False

#-----------------------------------------------------------------------------80
#   Function to define correctly the name of a supernova

def sn_name(sn_filename):

    # To read correctly, e.g., "sn2011B":
    if sn_filename[7] == '_': sn_name = sn_filename[:7]

    elif sn_filename[7] != '_':

        # To read correctly, e.g., "snf20080514-002":
        if is_number(sn_filename[7]): sn_name = sn_filename[:15]

        # To read correctly, e.g., "sn1998bu"
        else: sn_name = sn_filename[:8]

    return sn_name

#-----------------------------------------------------------------------------80



