# movieClassification
Experimenting in classifying movies by genre using imdb data and python

Data from imdb:
http://www.imdb.com/interfaces
Acquired via ftp.

For now using two main data sources, genres.list, and ratings.list. Some additional sources may make for interesting analysis as well though

OpenSubtitles Database
Link dump here:
http://dl.opensubtitles.org/addons/export/
These dumps have imdb ids for matching up against! It's like they're promoting analysis, awesome.

General goal: Experimenting in the use of classification algorithms, both implemented using sklearn and coded from scratch for experience.
imbd data should theoretically be great because it's sizable and well-labelled.

Initial approach is likely going to filter to only movies above a certain budget / revenue / number or ratings since there are so many tiny terrible movies.
Although there are probably interesting things that can be done without restricting based on size. For instance, if a movie has a porn star, it's probably porn.

There is no set goal here, really just practice.
