#!/usr/bin/env python

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
import data_prep
import re


def clean_ratings(movies):
    # Remove punctuation, split, and remove stopwords
    movies['reason_clean'] = movies.reason.astype(str).apply(
        lambda x: re.sub('[^a-zA-Z]', ' ', x))
    return movies


def split_data(movies):
    msk = np.random.rand(len(movies)) < 0.8
    train = movies[msk].copy().reset_index()
    test = movies[~msk].copy().reset_index()
    return train, test


def create_features(train):
    vectorizer = CountVectorizer(analyzer="word", stop_words='english')
    train_data_features = vectorizer.fit_transform(
        train.reason_clean.tolist())
    return vectorizer, train_data_features


def fit_forest(train, features):
    forest = RandomForestClassifier(n_estimators=100)
    forest = forest.fit(features, train['label'])
    return forest


if __name__ == '__main__':
    genre_listing = data_prep.read_genres('imdb/genres.list')
    rating_listing = data_prep.read_ratings('imdb/ratings.list')
    mpaa = data_prep.read_mpaa('imdb/mpaa-ratings-reasons.list')

    movies = data_prep.merge_all(rating_listing, genre_listing, mpaa)
