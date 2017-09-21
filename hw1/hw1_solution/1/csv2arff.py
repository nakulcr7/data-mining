#!/usr/bin/env python
# Author: Nakul Camasamudram

# Imports
from collections import OrderedDict
import csv
import sys

# Data Structures
FEATURE_DATA = OrderedDict()


# Helper functions
def display_arff(in_filename):
    display_relation(in_filename)
    display_attributes()
    display_data(in_filename)


def display_data(in_filename):
    print('@data')
    for row in read_data_iter(in_filename):
        out_str = ','.join(map(lambda x: '?' if x == '' else x, row.values()))
        print(out_str)


def display_attributes():
    global FEATURE_DATA
    for feature in FEATURE_DATA:
        values = FEATURE_DATA[feature]['values']
        if FEATURE_DATA[feature]['type'] == 'discrete':
            values = '{' + ','.join(sorted(values)) + '}'
        out_str = '@attribute {} {}'.format(feature, values)
        print(out_str)


def display_relation(outfile_name):
    out_str = '@relation {}'.format(outfile_name)
    print(out_str)


def populate_feature_data(filename):
    global FEATURE_DATA
    for row in read_data_iter(filename):
        for feature, feature_value in row.items():
            if is_discrete(feature_value):
                FEATURE_DATA.setdefault(feature, {})['type'] = 'discrete'
                FEATURE_DATA.setdefault(feature, {}).setdefault('values', set()).add(feature_value)
            else:
                FEATURE_DATA.setdefault(feature, {})['type'] = 'numeric'
                FEATURE_DATA.setdefault(feature, {})['values'] = 'numeric'


def is_discrete(value):
    return not(str(value).isdigit())


def read_data_iter(filename):
    with open(filename, 'rU') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


# Main Function
def main():
    global FEATURE_DATA
    args = sys.argv
    populate_feature_data(args[1])
    display_arff(args[1])


if __name__ == "__main__":
    main()
