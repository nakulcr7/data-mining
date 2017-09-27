#!/usr/bin/env python3
# Author: Nakul Camasamudram

# Imports
from collections import defaultdict
import sys


# Helper functions
def display_arff(in_filename, max_number):
    display_relation(in_filename)
    display_attributes(max_number)
    display_data(in_filename)


def display_relation(outfile_name):
    out_str = '@RELATION {}'.format(outfile_name.strip().split('.')[0])
    print(out_str)


def display_attributes(max_number):
	for i in range(1, max_number + 1):
		value_string = '{0, 1}'
		print('@ATTRIBUTE i{} {}'.format(i, value_string))


def display_data(in_filename):
    print('@DATA')
    for line in read_file_iter(in_filename):
    	nums = [int(n) for n in line.strip().split()]
    	output_dict = defaultdict(int)
    	for num in nums:
    		output_dict[num] += 1
    	output_pairs = []
    	for num in sorted(output_dict):
    		# output_str += '{' + '{} {} '.format(num - 1, output_dict[num]) + '}'
    		output_pairs.append('{} {}'.format(num - 1, output_dict[num]))
    	print('{' + ', '.join(output_pairs) + '}')


def find_max_number(in_filename):
	maximum = float("-inf")
	for line in read_file_iter(in_filename):
		for num_str in line.strip().split():
			num = int(num_str)
			if num > maximum:
				maximum = num
	return maximum


def read_file_iter(in_filename):
	with open(in_filename, 'rU') as f:
		for line in f:
			yield line


# Main function
def main():
	args = sys.argv
	display_arff(args[1], find_max_number(args[1]))


if __name__ ==  "__main__":
	main()