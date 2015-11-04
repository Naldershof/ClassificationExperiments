#!/usr/bin/env python

import pandas as pd
import numpy as np

def read_available_subs(subfile):
	# Using subtitles files from http://dl.opensubtitles.org/addons/export/
	all_subs = pd.read_csv(subfile, sep='\t', error_bad_lines=False, warn_bad_lines=False)
	en_subs = all_subs[(all_subs.MovieKind == 'movie') & (all_subs.ISO639 == 'en')].copy()
	en_subs.drop(['SubSumCD','MovieFPS','SeriesSeason','SeriesEpisode','SeriesIMDBParent','MovieKind'], axis=1, inplace=True)
	return en_subs

# Has this entire process been done by like 15 million other people who have their code on github? Yes, yes it has.
# BUT I'M BUILDING CHARACTER DAMNIT
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
	# Title strings end in ' (20XX)', however this isn't perfect
	# Sometimes they actually end in something like ' (20XX) (V)' or ' (20XX) (TV)'
	# No earthly idea why, so write a better regex for this. 
	print 'Stripping date from variables'
	genre_list.title = genre_list.title.str[:-7]
	return genre_list

#Stubbing
def read_ratings(ratingsfile):
	#Get all rated movies, and then return a dataframe with only those that have been rated at least 10k times
	pass

def match_to_subs(genre_listing, sub_listing, rating_listing):
	#Join genre listings to significantly rated movies
	#Get links to download the subs and associate them, don't fetch them just yet though   
	pass

if __name__ == '__main__':
	sub_listing = read_available_subs('subtitles_all.txt') 
	genre_listing = read_genres('imdb/genres.list')