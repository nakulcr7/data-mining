# Feature Normalization

A simple script that inputs data from a file, normalizes within fixed bounds, and then outputs the normalized data to the console with a specified precision.

## Usage

``` bash
./normalize.py [path_to_text_file] [lower_bound] [upper_bound] [precision]
```

***For example:*** `./normalize.py 2 in.txt -1 1 4`

## Assumptions

- The text file has one instance per line, space separating each element

- `[lower_bound]` and `[upper_bound]` above are for rach feature, such as -1 -1 or 0 -1