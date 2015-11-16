
# movieClassification
Experimenting in classifying movies by genre using imdb data and python

Data from imdb:
http://www.imdb.com/interfaces
Acquired via ftp.

For now using three main data sources, genres.list, mpaa-ratings-reasons.list, and ratings.list. Some additional sources may make for interesting analysis as well though.

Current approach uses Random Forest classifier to match mpaa rating reasons up against mpaa ratings. Initial run using an 80 / 20 train / test split shows approximately 85% accuracy. However, this is not all that great a metric since we're not determining what percentage of movies are normally in a given rating. 

Fix this by using something like multiclass log loss
https://www.kaggle.com/wiki/MultiClassLogLoss

General goal: Experimenting in the use of classification algorithms, both implemented using sklearn and coded from scratch for experience.