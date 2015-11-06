#!/usr/bin/env python

import pandas as pd
import numpy as np

def read_available_subs(subfile):
	# Using subtitles files from http://dl.opensubtitles.org/addons/export/
	all_subs = pd.read_csv(subfile, sep='\t', error_bad_lines=False, warn_bad_lines=False)
	print 'Filtering to only English subtitles on movies'
	en_subs = all_subs[(all_subs.MovieKind == 'movie') & (all_subs.ISO639 == 'en')].copy()
	en_subs.drop(['SubSumCD','MovieFPS','SeriesSeason','SeriesEpisode','SeriesIMDBParent','MovieKind'], axis=1, inplace=True)
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
							engine='python', header=None, names=['title','genre'])
	return genre_list


def read_ratings(ratingsfile, filter=True):
	#Get all rated movies, and then return a dataframe with only those that have been rated at least 10k times
	print 'Parsing ratings documentation block'
	with open(ratingsfile) as ratings:		
		for num, line in enumerate(ratings):
			if line == 'MOVIE RATINGS REPORT\n':
				# Blank spaces after Genre List header
				ratings_start_line = num + 3
			elif line == '------------------------------------------------------------------------------\n':
				ratings_end_line = num - 2

	with open(ratingsfile) as ratings:
		#Convert those columns which actually have ratings data into nested arrays
		#Then we can convert those nested arrays into a dataframe 
		ratings_unparsed = tuple(ratings)[ratings_start_line:ratings_end_line]
		
	ratings_arr = []

	print 'Parse ratings lines and convert to DataFrame'
	if filter is True:
		print 'Filter set to true, ignoring entries with <1000 entries'

	for i, line in enumerate(ratings_unparsed):
		entry = []
		#MAGIC NUMBERS!!! Let's make this better with some regexes and stuff
		entry.append( float(line[18:26].strip()) )
		entry.append( float(line[27:31].strip()) )
		entry.append( line[31:].strip() )
		#1000 still gives a lot of stuff no one actually cares about, it's the top <5%, but imdb is just seriously heavy 
		#on unpopular things 
		if filter is True:
			if entry[0] >= 1000:
				ratings_arr.append(entry)
		else:
			ratings_arr.append(entry)

	ratings = pd.DataFrame(ratings_arr, columns=['votes','rating','title'])
	return ratings



def merge_ratings_w_genres(ratings, genres):
	#Basically get all those which have the same names in ratings and genres
	movies = pd.merge(ratings, genres, how='inner', on='title')

	# Title strings end in ' (20XX)', however this isn't perfect
	# Sometimes they actually end in something like ' (20XX) (V)' or ' (20XX) (TV)'
	# No earthly idea why, so write a better regex for this. 
	#print 'Stripping date from variables'
	#genre_list.title = genre_list.title.str[:-7]

	pass

def match_to_subs(movie_listing, sub_listing):
	#Join genre listings to significantly rated movies
	#Get links to download the subs and associate them, don't fetch them just yet though
	pass

if __name__ == '__main__':
	sub_listing = read_available_subs('subtitles_all.txt') 
	genre_listing = read_genres('imdb/genres.list')