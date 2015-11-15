#!/usr/bin/env python

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
import data_prep


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


def fit_forest(train, features):
    forest = RandomForestClassifier(n_estimators=100)
    forest = forest.fit(features, train['label'])
    return forest


if __name__ == '__main__':
    genre_listing = data_prep.read_genres('imdb/genres.list')
    rating_listing = data_prep.read_ratings('imdb/ratings.list')
    mpaa = data_prep.read_mpaa('imdb/mpaa-ratings-reasons.list')

    movies = data_prep.merge_all(rating_listing, genre_listing, mpaa)

    train, test = split_data(movies)
    vectorizer, train_data_features = create_train_features(train)

    forest = fit_forest(train, train_data_features)

    test_data_features = create_test_features(test, vectorizer)

    result = forest.predict(test_data_features)
    test['predictions'] = result
    #Seems about 85% accurate so far, cool.
