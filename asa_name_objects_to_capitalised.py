#!/usr/bin/env python3

'''
-*- coding: utf-8 -*-
title           : asa_name_objects_to_capitalised.py
description     : Performs a lookup in object group and find the appropriate IP address
author          : donaldjohnson.nz@gmail.com
date            : 14/03/2018
version         : 0.1
usage           : ./asa_name_objects_to_capitalised.py --help
notes           :
python_version  : 3.5.2

Requirements: 
 - python3
 - pip install logzero argprse

simply converts all name elements to uppercase, cause I like my objects to be in caps

Usage:
python .\asa_name_objects_to_capitalised.py -i <'path/to/name-to-object.txt'> -o <'path/to/file.txt'>
=======================================================================
'''

import os
import re
import sys
from logzero import logger
import argparse

def CheckArgs(args=None):

    parser = argparse.ArgumentParser(
        description='Convert name to objects')
    parser.add_argument('-i', '--input_file', required=True,
                        help='File to convert.')
    parser.add_argument('-o', '--output_file', required=True,
                        help='File to output to.')
    parser.add_argument('-c', '--cleanup', required=False, action='store_true',
                        help='Removes output file first')
    results = parser.parse_args(args)
    return (
        results.input_file,
        results.output_file,
        results.cleanup
    )


def RemoveFile(file):

    logger.info('Cleanup requested, removing {}'.format(file))
    os.remove(file)

if __name__ == "__main__":

    INPUT_FILE, OUTPUT_FILE, cleanup_last_run = CheckArgs(sys.argv[1:])

    if cleanup_last_run:
        RemoveFile(OUTPUT_FILE)

    with open(INPUT_FILE, 'r') as imp:
        alist = [line.rstrip() for line in imp]

    with open(OUTPUT_FILE, 'a') as out:
        for line in alist:
            elements = line.split(' ')
            logger.info('processing: {}'.format(line))

            # in case the name element has a description
            if len(elements) >= 4:
                out.write('{} {} {} {}'.format(elements[0], elements[1], elements[2].upper(), ' '.join(elements[3:])))
            else:
                out.write('{} {} {}'.format(elements[0], elements[1], elements[2].upper()))
            out.write('\n')
