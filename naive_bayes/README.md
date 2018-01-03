# Verbose Naive Bayes Classifier

## Implementation details

- The goal was to write the code from scratch, without making use of modules (aside from basic sqrt/pow/log functions available via math, and command-line arguments/exit in sys).

- Additive smoothing only when necessary (i.e to avoid P(x) = 0) for discrete features. Discrete features were assumed to be Gaussian.

Below are sample runs to show what I expect as outputs (parameters are [data file] [target feature name] [alpha] [test feature 1] [test feature 2] ...[test feature n]). Notice that NB model is first provided (all priors and likelihoods), then pertinent values to the test input (smoothed as appropriate), and then finally a classification. The first dataset is the classic weather example, and the shapes for the second are actually in the NB slides from class (in case a visualization helps).

``` python
$ ./naive_bayes.py data1.csv play 1 overcast 83 86 FALSE
P(yes;alpha=1) = 9 / 14 = 0.643
P(no;alpha=1) = 5 / 14 = 0.357
P(outlook=rainy|yes;alpha=1) = 3 / 9 = 0.333
P(outlook=overcast|yes;alpha=1) = 4 / 9 = 0.444
P(outlook=sunny|yes;alpha=1) = 2 / 9 = 0.222
P(outlook=rainy|no;alpha=1) = (2 + 1) / (5 + 1*3) = 0.375
P(outlook=overcast|no;alpha=1) = (0 + 1) / (5 + 1*3) = 0.125
P(outlook=sunny|no;alpha=1) = (3 + 1) / (5 + 1*3) = 0.500
P(temp|yes;alpha=1) = N(mean=73.000, sd=6.164)
P(temp|no;alpha=1) = N(mean=74.600, sd=7.893)
P(humidity|yes;alpha=1) = N(mean=79.111, sd=10.216)
P(humidity|no;alpha=1) = N(mean=86.200, sd=9.731)
P(windy=FALSE|yes;alpha=1) = 6 / 9 = 0.667
P(windy=TRUE|yes;alpha=1) = 3 / 9 = 0.333
P(windy=FALSE|no;alpha=1) = 2 / 5 = 0.400
P(windy=TRUE|no;alpha=1) = 3 / 5 = 0.600
Input: [’overcast’, ’83’, ’86’, ’FALSE’]
P(yes;alpha=1) = 9 / 14 = 0.643
P(outlook=overcast|yes;alpha=1) = 4 / 9 = 0.444
P(temp=83.000|yes;alpha=1) = N(mean=73.000, sd=6.164) = 1.736e-02
P(humidity=86.000|yes;alpha=1) = N(mean=79.111, sd=10.216) = 3.111e-02
P(windy=FALSE|yes;alpha=1) = 6 / 9 = 0.667
P(x|yes) = 1.600e-04
P(no;alpha=1) = 5 / 14 = 0.357
P(outlook=overcast|no;alpha=1) = (0 + 1) / (5 + 1*3) = 0.125
P(temp=83.000|no;alpha=1) = N(mean=74.600, sd=7.893) = 2.869e-02
P(humidity=86.000|no;alpha=1) = N(mean=86.200, sd=9.731) = 4.099e-02
P(windy=FALSE|no;alpha=1) = 2 / 5 = 0.400
P(x|no) = 5.880e-05
P(x) = 1.239e-04
P(yes|x) = 0.830
P(no|x) = 0.170
P(yes)P(x|yes) = 1.029e-04
P(no)P(x|no) = 2.100e-05
log(yes) = -3.988
log(no) = -4.678
argmax_Ck = yes

$ ./naive_bayes.py data2.csv sign 1 blue square
P(minus;alpha=1) = 5 / 12 = 0.417
P(plus;alpha=1) = 7 / 12 = 0.583
P(color=blue|minus;alpha=1) = 3 / 5 = 0.600
P(color=black|minus;alpha=1) = 1 / 5 = 0.200
P(color=red|minus;alpha=1) = 1 / 5 = 0.200
P(color=blue|plus;alpha=1) = 3 / 7 = 0.429
P(color=black|plus;alpha=1) = 2 / 7 = 0.286
P(color=red|plus;alpha=1) = 2 / 7 = 0.286
P(shape=circle|minus;alpha=1) = 2 / 5 = 0.400
P(shape=square|minus;alpha=1) = 3 / 5 = 0.600
P(shape=circle|plus;alpha=1) = 2 / 7 = 0.286
P(shape=square|plus;alpha=1) = 5 / 7 = 0.714
Input: [’blue’, ’square’]
P(minus;alpha=1) = 5 / 12 = 0.417
P(color=blue|minus;alpha=1) = 3 / 5 = 0.600
P(shape=square|minus;alpha=1) = 3 / 5 = 0.600
P(x|minus) = 3.600e-01
P(plus;alpha=1) = 7 / 12 = 0.583
P(color=blue|plus;alpha=1) = 3 / 7 = 0.429
P(shape=square|plus;alpha=1) = 5 / 7 = 0.714
P(x|plus) = 3.061e-01
P(x) = 3.286e-01
P(minus|x) = 0.457
P(plus|x) = 0.543
P(minus)P(x|minus) = 1.500e-01
P(plus)P(x|plus) = 1.786e-01
log(minus) = -0.824
log(plus) = -0.748
argmax_Ck = plus

$ ./naive_bayes.py data2.csv sign 1 orange square
P(minus;alpha=1) = 5 / 12 = 0.417
P(plus;alpha=1) = 7 / 12 = 0.583
P(color=red|minus;alpha=1) = 1 / 5 = 0.200
P(color=black|minus;alpha=1) = 1 / 5 = 0.200
P(color=blue|minus;alpha=1) = 3 / 5 = 0.600
P(color=red|plus;alpha=1) = 2 / 7 = 0.286
P(color=black|plus;alpha=1) = 2 / 7 = 0.286
P(color=blue|plus;alpha=1) = 3 / 7 = 0.429
P(shape=square|minus;alpha=1) = 3 / 5 = 0.600
P(shape=circle|minus;alpha=1) = 2 / 5 = 0.400
P(shape=square|plus;alpha=1) = 5 / 7 = 0.714
P(shape=circle|plus;alpha=1) = 2 / 7 = 0.286
Input: [’orange’, ’square’]
P(minus;alpha=1) = 5 / 12 = 0.417
P(color=orange|minus;alpha=1) = (0 + 1) / (5 + 1*4) = 0.111
P(shape=square|minus;alpha=1) = 3 / 5 = 0.600
P(x|minus) = 6.667e-02
P(plus;alpha=1) = 7 / 12 = 0.583
P(color=orange|plus;alpha=1) = (0 + 1) / (7 + 1*4) = 0.091
P(shape=square|plus;alpha=1) = 5 / 7 = 0.714
P(x|plus) = 6.494e-02
P(x) = 6.566e-02
P(minus|x) = 0.423
P(plus|x) = 0.577
P(minus)P(x|minus) = 2.778e-02
P(plus)P(x|plus) = 3.788e-02
log(minus) = -1.556
log(plus) = -1.422
argmax_Ck = plus
```