#!/usr/bin/env python

import data_prep
import pandas as pd
import numpy as np

#Plan: Create a custom decision tree algorithm here as well as a random
# forest implementation and compare those to the sklearn implementation


def prep_feature_df(train, train_data_features):
    feature_df = pd.DataFrame(train_data_features.todense())
    feature_columns = feature_df.columns.tolist()

    train_df = pd.concat([feature_df, train], axis=1)
    feature_df = train_df[feature_columns + ["label"]]
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


def partition_entropy(dataset, partition):
    return sum(entropy(dataset[dataset[partition] == x], 'label')
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


def fit_trees(train, label):
    pass


def pred_trees(test):
    pass

if __name__ == '__main__':
    #Use the trees from mpaa_analysis and the fit and pred from the custom implementation
    #and compare the results

    genre_listing = data_prep.read_genres('imdb/genres.list')
    rating_listing = data_prep.read_ratings('imdb/ratings.list')
    mpaa = data_prep.read_mpaa('imdb/mpaa-ratings-reasons.list')

    movies = data_prep.merge_all(rating_listing, genre_listing, mpaa)
    pass
