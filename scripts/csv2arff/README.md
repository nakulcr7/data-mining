# CSV to ARFF conversion script for Weka

Simple script to convert .CSV to .ARFF

## Usage:

``` bash
./csv2arff.py [*.csv] > [*.arff]
```

## Assumptions

- The first row of the file will contain attribute names – the ARFF attribute list should mirror this order

- All data will be either numeric or nominal – assume numeric if possible

- The output relation name should be the name of the file, without any path/extension information

- The set of values for nominal attributes should be listed in sorted order, irrespective of the order in which they appear in the CSV

- The data rows in the ARFF should appear in the same order as in the CSV