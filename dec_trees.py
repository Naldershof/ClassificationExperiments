#!/usr/bin/env python

import data_prep
import pandas as pd
import numpy as np

#Plan: Create a custom decision tree algorithm here as well as a random
# forest implementation and compare those to the sklearn implementation

#-----------------------------
#ID3 Algorithm
#-----------------------------

# Summary (From Wikipedia)
#   Calculate the entropy of every attribute using the data set S
#   Split the set S into subsets using the attribute for which entropy is minimum (or, equivalently, information gain is maximum)
#   Make a decision tree node containing that attribute
#   Recurse on subsets using remaining attributes.


def entropy(dataset, column):
    counts = dataset[column].value_counts()
    total = counts.sum()
    prob = counts / total
    return sum(-p * np.log2(p) for p in prob)


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
