#!/usr/bin/env python

'''So this works ok. I guess the problem is I'm lacking significant
Indicators of how well it's  actually performing. A lot of that is
limited insights into how this actually works and an improper metric
for comparison. So start writing methods for evaluating the success
of the model in question, as well as using additional models and testing
really naive things like trying all on specific rating.'''

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import numpy as np
import data_prep

#-----------------------------
#Prep data for use in Different models
#-----------------------------


def split_data(movies):
    msk = np.random.rand(len(movies)) < 0.8
    train = movies[msk].copy().reset_index()
    test = movies[~msk].copy().reset_index()
    return train, test


#Additional steps we could take: Implementing a "stemmer", which strips
#similar words down to a root word. EG "nude" and "nudity"

def create_train_features(train):
    vectorizer = CountVectorizer(analyzer="word", stop_words='english')
    train_data_features = vectorizer.fit_transform(
        train.reason_clean.tolist())
    return vectorizer, train_data_features


def create_test_features(test, vectorizer):
    test_data_features = vectorizer.transform(
        test.reason_clean.tolist())
    return test_data_features

#-----------------------------
# Classifier Fitting.
#-----------------------------

# This doesn't work terribly with genres either, we just need to convert from
# annoying sets to something useful. Review how the data is stored, cause just
# trying the first one is alright so far.

# Other option is using 'multilabel classification'
# http://scikit-learn.org/stable/modules/multiclass.html#multilabel-classification-format
# I don't think this will work particularly well for the data we have in rating reasons,
# but it's going to be an excellent tool if we get sub data in here


#Random Forest
def fit_random_forest(train, features, predictor):
    forest = RandomForestClassifier(n_estimators=100)
    forest = forest.fit(features, train[predictor])
    return forest


def fit_xrandom_forest(train, features, predictor):
    xforest = ExtraTreesClassifier(n_estimators=100)
    xforest = xforest.fit(features, train[predictor])
    return xforest


def fit_dectree(train, features, predictor):
    trees = DecisionTreeClassifier(max_depth=8, min_samples_split=1,
                                   random_state=0)
    trees = trees.fit(features, train[predictor])
    return trees

# Throw in an SVM here since that supports multiclass classification

#-----------------------------
# Sklearn Classifier Predicting.
#
# Note: Now the actually return different results! The problem
# was that I was overwritting predictions in place without realizing it
# cause creating pandas columns modifies the original object unless you explicity
# make sure to copy...
#-----------------------------


def pred_random_forest(test, test_data_features, forest):
    # Otherwise we modify the original, insidious mistake that made
    # results appear the same across algorithms
    test_rf = test.copy()
    result = forest.predict(test_data_features)
    test_rf['predictions'] = result
    return test_rf


def pred_xrandom_forest(test, test_data_features, xforest):
    test_xrf = test.copy()
    result = xforest.predict(test_data_features)
    test_xrf['predictions'] = result
    return test_xrf


def pred_dectree(test, test_data_features, trees):
    test_dec = test.copy()
    result = trees.predict(test_data_features)
    test_dec['predictions'] = result
    return test_dec

#-----------------------------
#Custom Classifiers
#-----------------------------


def fit_custom_dectree(train, features, predictor):
    pass

#-----------------------------
#Evaluation
#-----------------------------

#I don't understand how things like confusion matrices work in multiple choice problems :-\


def compare_rates(tested, predictor='label'):
    rates = pd.concat([tested[predictor].value_counts(),
                       tested.predictions.value_counts()],
                      axis=1)
    #Here's where we put the scoring logic (I think)
    return rates


# Bring this all up into individual functions and change the file to use
# arguments and output some excellent graphs, reports, stats, etc
if __name__ == '__main__':
    genre_listing = data_prep.read_genres('imdb/genres.list')
    rating_listing = data_prep.read_ratings('imdb/ratings.list')
    mpaa = data_prep.read_mpaa('imdb/mpaa-ratings-reasons.list')

    movies = data_prep.merge_all(rating_listing, genre_listing, mpaa)

    train, test = split_data(movies)
    vectorizer, train_data_features = create_train_features(train)
    test_data_features = create_test_features(test, vectorizer)

    '''vocab_significance = pd.DataFrame(
                    zip(vectorizer.vocabulary_, forest.feature_importances_),
                    columns=['vocab', 'significance'])'''
