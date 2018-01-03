#!/usr/bin/env python
# Author: Nakul Camasamudram

# Imports
from decimal import Decimal, ROUND_UP
import sys


# Helper Functions
def process_input(in_filename):
    in_matrix = []
    for row in read_file(in_filename):
        n = [float(num) for num in row.strip().split()]
        in_matrix.append(n)
    return in_matrix


def read_file(in_filename):
    with open(in_filename, 'rU') as f:
        for line in f:
            yield line


def transpose(matrix):
    return [num for num in zip(*matrix)]


def scale_numbers(numbers, new_min, new_max, precision):
    current_min = float("inf")
    current_max = float("-inf")
    scaled_numbers = []
    for num in numbers:
        current_min = min(num, current_min)
        current_max = max(num, current_max)
    for num in numbers:
        scaled_numbers.append(scale_number(num, current_min, current_max, new_min, new_max, precision))
    return scaled_numbers


def scale_number(number, current_min, current_max, new_min, new_max, precision):
    scaled_num = ((number - current_min) / (current_max - current_min)) * (new_max - new_min) + new_min
    precision = Decimal(10) ** -precision
    return Decimal(scaled_num).quantize(precision, rounding=ROUND_UP)


# Main Function
def main():
    args = sys.argv
    in_matrix = process_input(args[1])
    in_transpose = transpose(in_matrix)
    for i, feature_row in enumerate(in_transpose):
        in_transpose[i] = scale_numbers(feature_row, int(args[2]), int(args[3]), int(args[4]))
    out_matrix = transpose(in_transpose)
    for feature_row in out_matrix:
        print(' '.join([str(val) for val in feature_row]))


if __name__ == '__main__':
    main()
