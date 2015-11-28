#!/usr/bin/env python

import data_prep
import mpaa_analysis
import pandas as pd
import numpy as np

from collections import Counter
import math

#Plan: Create a custom decision tree algorithm here as well as a random
# forest implementation and compare those to the sklearn implementation

#-----------------------------
#Example implementation from
#data science from scratch
#-----------------------------

#Why log base 2? Fuck if I know. Magic. This is how we calculate entropy
# though. Blame Shannon


def entropy(class_probabilities):
    """given a list of class probabilities, compute the entropy"""
    return sum(-p * math.log(p, 2)
               for p in class_probabilities
               if p)  # ignore zero probabilities


def class_probabilities(labels):
    total_count = len(labels)
    return [count / total_count
            for count in Counter(labels).values()]


def data_entropy(labeled_data):
    labels = [label for _, label in labeled_data]
    probabilities = class_probabilities(labels)
    return entropy(probabilities)


def partition_entropy(subsets):
    """find the entropy from this partition of data into subsets
    subsets is a list of lists of labeled data"""
    total_count = sum(len(subset) for subset in subsets)
    return sum(data_entropy(subset) * len(subset) / total_count
               for subset in subsets)

#-----------------------------
#End Examples
#-----------------------------


def fit_trees():
    pass


def pred_trees():
    pass

if __name__ == '__main__':
    #Use the trees from mpaa_analysis and the fit and pred from the custom implementation
    #and compare the results
    pass
