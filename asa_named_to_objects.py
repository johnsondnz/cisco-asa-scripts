#!/usr/bin/env python3

'''
-*- coding: utf-8 -*-
title           : asa_named_to_objects.py
description     : Converts pre 8.3 name entries to objects for use is access-lists
author          : donaldjohnson.nz@gmail.com
date            : 14/03/2018
version         : 0.1
usage           : ./asa_named_to_objects.py --help
notes           :
python_version  : 3.5.2

Requirements: 
 - python3
 - pip install logzero argprse


converts:

name 1.1.1.1 Test
name 2.2.2.2 test-2
name 3.3.3.3 test3 description some text here
name 192.168.5.50 test2-nat

to 

object network TEST
 host 1.1.1.1
!
object network TEST_2
 host 2.2.2.2
!
object network TEST3
 host 2.2.2.2
 description some text here
!
object network MAPPED_TEST2-192.168.5
 host 192.168.5.50
!

Usage:
python asa_named_to_objects.py -i <'path/to/name-to-object.txt'> -o <'path/to/file.txt'>
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

            try:
                elements = line.split()
                logger.info('processing: {}'.format(line))

                # make the object name case insensitve for search and replace operations
                object_name = elements[2].lower()
                object_name = object_name.replace('-', '_')

                # look for nat name objects
                if re.search('^.+([-_])nat', object_name):
                    logger.info('"nat" found in: {}'.format(object_name))

                    # get IP octets
                    ip_octets = elements[1].split('.')

                    # remove nat from object_name
                    object_name = object_name.replace('_nat', '')
                    object_name = object_name.replace('-nat', '')
                    logger.info('Object created: MAPPED_{}-{}.{}.{}\n'.format(
                        object_name.upper(), ip_octets[0], ip_octets[1], ip_octets[2]))

                    out.write('object network MAPPED_{}-{}.{}.{}\n'.format(
                        object_name.upper(), ip_octets[0], ip_octets[1], ip_octets[2]))

                # all other name objects will be real addresses
                else:
                    logger.info('Object created: {}\n'.format(
                        object_name.upper()))
                    out.write('object network {}\n'.format(
                        object_name.upper()))

                out.write(' host {}\n'.format(elements[1]))

                # check for a description and migrate to object
                if len(elements) >= 4:
                    out.write(' {}\n'.format(' '.join(elements[3:])))

                out.write('!\n')

            except:
                logger.error('{}: {}'.format(
                    sys.exc_info()[0], sys.exc_info()[1]))
