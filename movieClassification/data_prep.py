#!/usr/bin/env python

import pandas as pd
import re


def read_available_subs(subfile):
    # Using subtitles files from http://dl.opensubtitles.org/addons/export/
    # Not using this right now.
    print 'Parsing subtitle listings'
    all_subs = pd.read_csv(subfile, sep='\t', error_bad_lines=False, warn_bad_lines=False)

    print 'Filtering to only English subtitles on movies'
    en_subs = all_subs[(all_subs.MovieKind == 'movie') & (all_subs.ISO639 == 'en')].copy()
    en_subs.drop(['SubSumCD', 'MovieFPS', 'SeriesSeason', 'SeriesEpisode', 'SeriesIMDBParent', 'MovieKind'],
                 axis=1, inplace=True)

    # Alphanumberic to upper
    en_subs['title_clean'] = en_subs.MovieName.apply(lambda x: re.sub('\W+', '', str(x)).upper())
    return en_subs


def read_genres(genrefile):
    # Genre File is really weirdly constructed so I'll have to write an actual parser, not just use the pandas' read_csv
    print 'Parsing genre list documentation block'
    with open(genrefile) as genres:
        for num, line in enumerate(genres):
            if line == '8: THE GENRES LIST\n':
                # Blank spaces after Genre List header
                genre_start_line = num + 2
                break

    print 'Reading genre list into memory'
    genre_list = pd.read_csv(genrefile, sep=r'\t*', skipinitialspace=True, skiprows=genre_start_line,
                             engine='python', header=None, names=['title', 'genre'])

    return genre_list


def read_ratings(ratingsfile, filter=True):
    # Get all rated movies, and then return a dataframe with only those that have been rated at least 10k times
    print 'Parsing ratings documentation block'
    with open(ratingsfile) as ratings:
        for num, line in enumerate(ratings):
            if line == 'MOVIE RATINGS REPORT\n':
                # Blank spaces after Genre List header
                ratings_start_line = num + 3
            elif line == '------------------------------------------------------------------------------\n':
                ratings_end_line = num - 2

    with open(ratingsfile) as ratings:
        # Convert those columns which actually have ratings data into nested arrays
        # Then we can convert those nested arrays into a dataframe
        ratings_unparsed = tuple(ratings)[ratings_start_line:ratings_end_line]

    ratings_arr = []

    print 'Parse ratings lines and convert to DataFrame'
    if filter is True:
        print 'Filter set to true, ignoring entries with <1000 entries'

    for i, line in enumerate(ratings_unparsed):
        entry = []
        # MAGIC NUMBERS!!! Let's make this better with some regexes and stuff
        entry.append(float(line[18:26].strip()))
        entry.append(float(line[27:31].strip()))
        entry.append(line[31:].strip())
        # 1000 still gives a lot of stuff no one actually cares about, it's the top <5%, but imdb is just seriously heavy
        # on unpopular things
        if filter is True:
            if entry[0] >= 1000:
                ratings_arr.append(entry)
        else:
            ratings_arr.append(entry)

    ratings = pd.DataFrame(ratings_arr, columns=['votes', 'rating', 'title'])
    print '%s movies returned' % ratings.shape[0]
    return ratings


def read_mpaa(mpaafile):
    print 'Opening mpaa files'
    with open(mpaafile) as mpaa_r:
        mpaa = tuple(mpaa_r)

    print 'Cleaning mpaa data'
    mpaa_dict = {}
    for line, item in enumerate(mpaa):
        if item[0:3] == 'MV:':
            movie = item[3:]
            mpaa_dict[movie] = []
        if item[0:3] == 'RE:':
            mpaa_dict[movie].append(item[3:])

    mpaa_arr = []
    for key, value in mpaa_dict.iteritems():
        clean_key = key.strip()
        # Join two line ratings into one and replace multiple spaces with one
        temp_value = ' '.join(value).strip().replace('\n', '')
        clean_value = re.sub(' +', ' ', temp_value)

        # Get rating and reason by splitting on possible ratings
        # Some come in as "PG -13" or "PG - 13", stupid messy data
        value_split = re.split('( G | PG |\s*PG\s*-\s*13 | R |NC\s*-\s*17)', clean_value)
        mpaa_arr.append([clean_key] + value_split[1:])

    mpaa_frame = pd.DataFrame(mpaa_arr, columns=['title', 'label', 'reason'])
    # The regex brings them in with spaces, I should do this before here but it works
    #mpaa_frame.label = mpaa_frame.label.str.strip()
    mpaa_frame.label = mpaa_frame.label.astype(str).apply(
        lambda x: re.sub('[\s]', '', x))

    mpaa_frame['reason_clean'] = mpaa_frame.reason.astype(str).apply(
        lambda x: re.sub('[^a-zA-Z]', ' ', x))

    return mpaa_frame


def merge_all(ratings, genres, mpaa):
    print 'Performing initial merge'
    # Basically get all those which have the same names in ratings and genres
    movie_data = pd.merge(ratings, genres, how='inner', on='title')
    # The main problem is that this duplicates genres, the problem is whether we do compound genres, or just select the first
    movie_data = movie_data.groupby(['title', 'votes', 'rating']).apply(lambda x: set(x.genre))
    movies = movie_data.reset_index()
    movies.rename(columns={0: 'genres'}, inplace=True)

    movies_full = movies.merge(mpaa, how='inner', on='title')

    print 'Cleaning title'
    # Since movies are usually 'title (year)', split title to get rid of year, regex matches '(####)'
    # Note, this wouldn't work if there was a movie called "(1234) Blah", but it seems there's not
    movies['title_clean'] = movies.title.apply(lambda x: re.split('(\(\d{4}\))', x)[0])
    movies['title_clean'] = movies.title_clean.apply(
        lambda x: re.sub('\W+', '', x).upper())  # only alpha numeric to upper
    return movies_full


def match_to_subs(movie_listing, sub_listing):
    # Join genre listings to significantly rated movies
    # Get links to download the subs and associate them, don't fetch them just yet though
    movies_subs = pd.merge(movie_listing, sub_listing, how='inner', on='title_clean')
    movies_srts = movies_subs[movies_subs.SubFormat == 'srt'].copy()
    # Problems here since you can't do more than 200 requests per day, site indicates openness to bulk requests
    # Will be doing that
    pass
