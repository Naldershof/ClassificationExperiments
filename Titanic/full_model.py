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
    clean['log_price'] = np.floor(clean.Fare.apply(lambda x: 0 if x == 0 else np.log(x))).fillna(0)

    clean['Age'] = clean.Age.fillna(clean.Age.median())
    clean['Embarked'] = clean.Embarked.fillna(clean.Embarked.mode().iloc[0])
    clean['decade'] = np.floor(clean.Age / 10)
    return clean


# -------------------------
# -----Modelling-----------
# -------------------------


def prep_feature_df(train):
    #Add Cabin back in after doing some cleaning
    feature_df = train.drop(['PassengerId', 'Name', 'Ticket', 'Cabin', 'Fare', 'Age', 'Sex'], axis=1)
    feature_df.Embarked = feature_df.Embarked.map({'S': 0, 'C': 1, 'Q': 2})
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


# We have the math! Let's do the iteration parts now!

# So the most effective way is going to be:
#       - Write a split function where given a feature splits by that feature
#       splits by a then returns an array of dataframes split by each possibility
#       - Then run the min entropy on that split and move onto the next.
#       - Hard part is going to be book keeping in a way that opens itself up for use as a
#       predictor, not just a used for fitting

# Note: This isn't a super effective method for actually getting result sets, a regression
# would be much better, but this is for experimenting with writing my own, not for actually doing
# high quality analytics

def split_df(DF, feature):
    df_split = {}
    for x in DF[feature].unique():
        df_split[x] = DF[DF[feature] == x].drop(feature, axis=1).copy()
    return df_split

# So what I really need to do is write a simple tree structure class since otherwise we won't be
# able to effectively store the data, nested dicts / lists is technically possible, but gets very
# very messy and no fun.

#http://www.patricklamle.com/Tutorials/Decision%20tree%20python/tuto_decision%20tree.html


class tree_node:
    def __init__(self, col=-1, value=None, results=None,
                 t_branch=None, f_branch=None, depth=0):
        self.col = col
        self.value = value
        self.results = results
        self.t_branch = t_branch
        self.f_branch = f_branch
        self.depth = depth

#Liberally cribbed code, max it work for our functions and adjusted split_df 
'''def fit_dec_tree(DF, label, max_depth):
    split_val = min_entropy_feature(DF, label)
      # Create the sub branches   
    if best_gain>0:
        trueBranch=buildtree(best_sets[0])
        falseBranch=buildtree(best_sets[1])
        return decisionnode(col=best_criteria[0],value=best_criteria[1],
                            tb=trueBranch,fb=falseBranch)
    else:
        return decisionnode(results=uniquecounts(rows))
'''