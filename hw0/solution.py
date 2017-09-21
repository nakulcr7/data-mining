#!/usr/bin/env python
# Author: Nakul Camasamudram

# Imports
import sys
import math
import csv

# Global data structues

"""Stores features from the data set in the following format:

target_class_1:
    - feature_1:
        - feature_value_1: frequency
        - feature_value_2: frequency
    - feature_2:
        - ..
target_class_2:
    - ..
..
"""
feature_data = {}

"""
Stores target class information in the following format:

target_class_1: frequency,
target_class_2: frequency
"""
target_data = {}

"""Stores feature probabilities from the data set in the following format:

target_class_1:
    - feature_1:
        - feature_value_1: probability
        - feature_value_2: probability
    - feature_2:
        - ..
target_class_2:
    - ..
..
"""
feature_prob = {}

prior_prob = {}
likelihoods = {}
discrete_features = {}


# Helper functions
def make_prediction(support):
    global likelihoods, prior_prob
    posterior_probs = []
    for target in prior_prob:
        num = likelihoods[target] * prior_prob[target]
        posterior_prob = num / support
        print("P({0})P(x|{1}) = {2}".format(target, target, num))
        print("P({0}|x) = {1}".format(target, posterior_prob))
        print("log({0}) = {1}".format(target, math.log10(num)))
        posterior_probs.append((target, posterior_prob))
    argmax = max(posterior_probs, key=lambda x: x[1])
    return argmax[0]


def compute_and_display_support(alpha):
    global likelihoods, target_prob
    p_x = 0
    for target, likelihood in likelihoods.items():
        p_x += likelihood * prior_prob[target]
    print("P(x) = {}".format(p_x))
    return p_x


def compute_and_display_likelihoods(x, alpha):
    global feature_prob, prior_prob
    for target, prob in prior_prob.items():
        print("P({0};alpha={1}) = {2}".format(target, alpha, prob))
        likelihoods[target] = 1
        for feature, feature_value in x:
            if is_discrete(feature_value):
                if 'smoothing' in feature_data[target][feature]:
                    p, p_str = additive_smoothing(feature_data.get(target).get(feature).get(feature_value, 0),
                                                  target_data[target], alpha, len(discrete_features[feature]))
                    feature_prob[target][feature][feature_value] = p
                    print("P({0}={1}|{2};alpha={3}) = {4}".format(
                        feature, feature_value, target, alpha, p_str))
                elif feature_value not in feature_data[target][feature]:
                    p, p_str = additive_smoothing(feature_data.get(target).get(feature).get(feature_value, 0),
                                                  target_data[target], alpha, len(discrete_features[feature]) + 1)
                    feature_prob[target][feature][feature_value] = p
                    print("P({0}={1}|{2};alpha={3}) = {4}".format(
                        feature, feature_value, target, alpha, p_str))
                else:
                    print("P({0}={1}|{2};alpha={3}) = {4}".format(
                        feature, feature_value, target, alpha, feature_prob[target][feature][feature_value]))
                likelihoods[target] *= feature_prob[target][feature][feature_value]
            else:
                mean = feature_prob[target][feature]['mean']
                sd = feature_prob[target][feature]['sd']
                g_mle = gaussian_mle(int(feature_value), mean, sd)
                likelihoods[target] *= g_mle
                print("P({0}={1}|{2};alpha={3}) = N(mean={4}, sd={5}) = {6}".format(
                    feature, feature_value, target, alpha, mean, sd, g_mle))
        print("P(x|{0}) = {1}".format(target, likelihoods[target]))


def compute_and_display_input_probabilities(alpha):
    global feature_data, target_data, feature_prob, discrete_features
    for target in target_data:
        num = target_data[target]
        denom = dict_vals_sum(target_data)
        p = round(num / denom, 3)
        prior_prob[target] = p
        print("P({0};alpha={1}) = {2} / {3} = {4}".format(target, alpha, num, denom, p))
        for feature in feature_data.get(target):
            if feature not in discrete_features:
                m = mean(feature_data[target][feature])
                std = sd(feature_data[target][feature])
                feature_prob[target][feature] = {'mean': m, 'sd': std}
                print("P({0}|{1};alpha={2}) = N(mean={3}, sd={4})".format(
                    feature, target, alpha, m, std))
            else:
                for feature_value in discrete_features[feature]:
                    initialize_feature_prob(target, feature, feature_value)
                    if 'smoothing' in feature_data[target][feature]:
                        p, p_str = additive_smoothing(feature_data.get(target).get(feature).get(feature_value, 0),
                                                      target_data[target], alpha, len(discrete_features[feature]))
                        feature_prob[target][feature][feature_value] = p
                        print("P({0}={1}|{2};alpha={3}) = {4}".format(
                            feature, feature_value, target, alpha, p_str))
                    else:
                        num = feature_data.get(target).get(feature).get(feature_value, 0)
                        denom = target_data[target]
                        p = round(num / denom, 3)
                        feature_prob[target][feature][feature_value] = p
                        print("P({0}={1}|{2};alpha={3}) = {4} / {5} = {6}".format(
                            feature, feature_value, target, alpha, num, denom, p))


def additive_smoothing(x, N, alpha, d):
    p = (x + alpha) / float((N + alpha * d))
    p_str = ("({0} + {1}) / ({2} + {3}*{4}) = {5}".format(
        x, alpha, N, alpha, d, p))
    return p, p_str


def gaussian_mle(x, mean, stdev):
    exponent = math.exp(-(math.pow(x - mean, 2) / (2 * math.pow(stdev, 2))))
    return (1 / (math.sqrt(2 * math.pi) * stdev)) * exponent


def mean(numbers):
    return sum(numbers) / float(len(numbers))


def sd(numbers):
    avg = mean(numbers)
    variance = sum([pow(x - avg, 2) for x in numbers]) / float(len(numbers) - 1)
    return math.sqrt(variance)


def process_input(in_file):
    global feature_data, target_data
    with open(in_file, newline='') as f:
        reader = csv.reader(f)
        headers = next(reader)
        for row in reader:
            target = row[-1]
            initialize_target_data(target)
            target_data[target] += 1
            for (feature, feature_value) in zip(headers[:-1], row[:-1]):
                target_data[target]
                if is_discrete(feature_value):
                    initialize_feature_data(target, feature, feature_value)
                    discrete_features[feature].add(feature_value)
                    feature_data[target][feature][feature_value] += 1
                else:
                    initialize_feature_data(target, feature, feature_value)
                    feature_data[target][feature].append(int(feature_value))
    return headers


def dict_vals_sum(d):
    return sum([v for k, v in d.items()])


def initialize_target_data(target_value):
    global target_data
    target_data.setdefault(target_value, 0)


def initialize_feature_prob(target_value, feature, feature_value):
    global feature_prob
    if is_discrete(feature_value):
        feature_prob.setdefault(target_value, {}).setdefault(feature, {}).setdefault(feature_value, 0)
    else:
        feature_prob.setdefault(target_value, {}).setdefault(feature, [])


def initialize_feature_data(target_value, feature, feature_value):
    global feature_data, discrete_features
    if is_discrete(feature_value):
        discrete_features.setdefault(feature, set([]))
        feature_data.setdefault(target_value, {}).setdefault(feature, {}).setdefault(feature_value, 0)
    else:
        feature_data.setdefault(target_value, {}).setdefault(feature, [])


def is_discrete(value):
    return not(str(value).isdigit())


def analyze_data_to_be_smoothed():
    global feature_data, discrete_features
    for target in feature_data:
        for d_feature in discrete_features:
            for d_feature_value in discrete_features[d_feature]:
                if d_feature_value not in feature_data[target][d_feature]:
                    feature_data[target][d_feature]['smoothing'] = True


# Main Function
def main():
    args = sys.argv
    in_file = args[1]
    alpha = int(args[3])
    x = args[4:]
    headers = process_input(in_file)
    analyze_data_to_be_smoothed()
    compute_and_display_input_probabilities(alpha)
    print("Input: {}".format(x))
    compute_and_display_likelihoods(list(zip(headers, x)), alpha)
    support = compute_and_display_support(alpha)
    argmax = make_prediction(support)
    print("argmax_Ck = {}".format(argmax))


if __name__ == "__main__":
    main()
