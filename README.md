
# Classification Experiments

A repository for storing implementation of some various machine learning algorithms I'm experimenting with for classification and analysis.

Each folder contains different datasets and general approaches

## Move Classification

Experimenting in classifying movies by genre using imdb data and python

Data from imdb:
http://www.imdb.com/interfaces
Acquired via ftp.

For now using three main data sources, genres.list, mpaa-ratings-reasons.list, and ratings.list. Some additional sources may make for interesting analysis as well though.

Current approach uses Random Forest classifier to match mpaa rating reasons up against mpaa ratings. Initial run using an 80 / 20 train / test split shows approximately 85% accuracy. However, this is not all that great a metric since we're not determining what percentage of movies are normally in a given rating. 

Fix this by using something like multiclass log loss
https://www.kaggle.com/wiki/MultiClassLogLoss

## Titanic Survivor Predictions

Using data from one of Kaggle's traditional training examples located here:
https://www.kaggle.com/c/titanic

While this is a relatively easy problem to solve by just doing a quick SKlearn classifier, I'll be implementing decision trees from scratch in python in order to better understand the workings of the algorithms and develop a greater understanding of the techniques and methods necessary to classify data based on different features