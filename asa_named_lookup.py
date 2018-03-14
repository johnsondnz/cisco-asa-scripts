#!/usr/bin/env python3

'''
-*- coding: utf-8 -*-
title           : asa_named_lookup.py
description     : Performs a lookup in object group and find the appropriate IP address
author          : donaldjohnson.nz@gmail.com
date            : 14/03/2018
version         : 0.1
usage           : ./asa_named_lookup.py --help
notes           :
python_version  : 3.5.2

Requirements: 
 - python3
 - pip install logzero argprse

lookup file is Cisco ASA name hostlist
name 192.168.6.22 <name> 
name 192.168.6.21 <name> 
name 192.168.6.23 <name> 
name 192.168.6.7 <name> description some words here

lookup is case insensitive

Usage:
python .\asa_named_lookup.py -l <'path/to/name-to-object.txt'> -v <named-host>

[I 180314 13:59:31 asa_named_lookup:65] Found: name 192.168.6.7 <named-host>, on line 4
[I 180314 13:59:31 asa_named_lookup:71] Object: <named-host>, IP: 192.168.6.7
=======================================================================
'''

import os
import sys
import re
from logzero import logger
import argparse

def CheckArgs(args=None):

    parser = argparse.ArgumentParser(
        description='Convert name to objects')
    parser.add_argument('-v', '--value', required=True,
                        help='File to convert.')
    parser.add_argument('-l', '--lookup_file', required=True,
                        help='File to convert.')
    results = parser.parse_args(args)
    return (
        results.value,
        results.lookup_file
    )

if __name__ == "__main__":

    VALUE, LOOKUP_FILE = CheckArgs(sys.argv[1:])

    with open(LOOKUP_FILE, 'r') as lookup:
        alist = [line.rstrip() for line in lookup]

    try:

        os.system('cls' if os.name == 'nt' else 'clear')
        elements = line.split()

        # make the object name case insensitve for search and replace operations
        object_name = elements[2].lower()

        # search for the object
        for index, lookup_line in enumerate(alist):

            look_elements = lookup_line.split(' ')
            lookup_object = look_elements[2].lower()

            if str(VALUE.lower()) == str(lookup_object.lower()):
                b_elembers = lookup_line.split(' ')
                object_ip = b_elembers[1]
                object_ip_found = True
                logger.info('Found: {}, on line {}'.format(lookup_line, index + 1))
                break
            else:
                object_ip_found = False
        
        if object_ip_found:
            logger.info('Object: {}, IP: {}'.format(VALUE, object_ip))
        else:
            logger.error('Object: {}, IP: not found'.format(VALUE))

    except:
        logger.error('{}: {}'.format(
        sys.exc_info()[0], sys.exc_info()[1]))
