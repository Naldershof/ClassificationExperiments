#!/usr/bin/env python

import pandas as pd
import numpy as np

def read_available_subs(subfile):
	#Using subtitles files from http://dl.opensubtitles.org/addons/export/
	all_subs = pd.read_csv(subfile, sep='\t', error_bad_lines=False, warn_bad_lines=False)
	en_subs = all_subs[(all_subs.MovieKind == 'movie') & (all_subs.ISO639 == 'en')].copy()
	en_subs.drop(['SubSumCD','MovieFPS','SeriesSeason','SeriesEpisode','SeriesIMDBParent','MovieKind'], axis=1, inplace=True)
	return en_subs

def read_genres(genrefile):
	#Genre File is really weirdly constructed so I'll have to write an actual parse, not just use the pandas' read_csv
	#:-(
	#

if __name__ == '__main__':
	sub_listing = read_available_subs('subtitles_all.txt') 