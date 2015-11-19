#!/usr/bin/env python

'''So this works ok. I guess the problem is I'm lacking significant
Indicators of how well it's  actually performing. A lot of that is
limited insights into how this actually works and an improper metric
for comparison. So start writing methods for evaluating the success
of the model in question, as well as using additional models and testing
really naive things like trying all on specific rating.'''

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
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
# Classifier testing.
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


def fit_dectree(train, features, predictor):
    trees = DecisionTreeClassifier(max_depth=None, min_samples_split=1,
                                   random_state=0)
    trees = trees.fit(features, train[predictor])
    return trees


#-----------------------------
#Evaluation
#-----------------------------

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

    forest = fit_random_forest(train, train_data_features, 'label')

    result = forest.predict(test_data_features)
    test['predictions'] = result
    #Seems about 85% accurate so far, cool.

    vocab_significance = pd.DataFrame(
        zip(vectorizer.vocabulary_, forest.feature_importances_),
        columns=['vocab', 'significance'])
