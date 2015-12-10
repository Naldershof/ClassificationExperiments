#!/usr/bin/env python

import pandas as pd
import numpy as np

# Here are the columns:
# PassengerId: Integer Value Key
# Survived: 0 - False, 1 - True
# Pclass: 1 - First, 2 - Second, 3 - Third
# Name: Name, no real value. Although wouldn't it be interesting if there was?
# Sex: male or female
#    --> Transform to M or F for ease of use
# Age: Integer valued age.
#       *Not always filled in, should be low priority for use*
# SibSp: Number of siblings / spouses on board
# Parch: Number of parents / Children on board
# Ticket: Ticket Number, should be trash data again.
# Fare: The amount paid for the ticket
# Cabin: Cabin Number / Letter. Very sparse as well and not very clean.
# Embarked: Port of Embarkation (C = Cherbourg; Q = Queenstown; S = Southampton)

# -------------------------
# -----Data Prep-----------
# -------------------------


def import_data(filename):
    DF = pd.read_csv(filename)
    return DF


def clean_data(DF):
    clean = DF.copy()
    clean['male'] = clean.Sex.map({"female": 0, "male": 1})

    #This seems to give some decent segmentation, but idk how reasonable it is
    clean['log_price'] = np.floor(clean.Fare.apply(lambda x: 0 if x == 0 else np.log(x)))
    return clean


# -------------------------
# -----Modelling-----------
# -------------------------


def prep_feature_df(train):
    #Add Cabin back in after doing some cleaning
    feature_df = train.drop(['PassengerId', 'Name', 'Ticket', 'Cabin', 'Fare'], axis=1)
    return feature_df


#-----------------------------
#ID3 Algorithm
#-----------------------------

# Summary (From Wikipedia)
#   Calculate the entropy of every attribute using the data set S
#   Split the set S into subsets using the attribute for which entropy is minimum
#   (or, equivalently, information gain is maximum)
#   Make a decision tree node containing that attribute
#   Recurse on subsets using remaining attributes.


# Calculate the entropy of a given feature. Input is df filtered by values, ex: DF[DF.col == n]
def entropy(feature_set, label):
    counts = feature_set[label].value_counts()
    total = counts.sum()
    prob = counts / total
    return sum(-p * np.log2(p) for p in prob)


def partition_entropy(dataset, partition, label):
    return sum(entropy(dataset[dataset[partition] == x], label)
               for x in dataset[partition].unique())


# q1 is proportion of data in set
# H = (q1)H(S1) + ... + (qm)H(Sm)

# This is pretty slow, makes me really appreciate how incredibly well-optimized sklearn is
# If we shift this to using sparse matrixes in scipy it'll probably be faster to start with.
def entropies_by_partition(dataset, label):
    entropies = {}
    feature_cols = dataset.columns.tolist()
    feature_cols.remove(label)
    for col in feature_cols:
        entropies[col] = partition_entropy(dataset, col)
    return entropies


def min_entropy_feature(feature_df, label):
    entropies = entropies_by_partition(feature_df, label)
    return min(entropies, key=entropies.get)
