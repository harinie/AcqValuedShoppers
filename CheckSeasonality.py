#!/usr/bin/python
#Kaggle Challenge: 
#"http://www.kaggle.com/c/acquire-valued-shoppers-challenge/" 
#'Reduce the data and generate features' by Triskelion 
#After a forum post by BreakfastPirate
#Very mediocre and hacky code, single-purpose, but pretty fast

from datetime import datetime, date
from collections import defaultdict
import numpy as np
from pylab import plot, show

loc_offers = "//home//harini//Kaggle_data//shop//offers.csv"
loc_transactions = "//home//harini//Kaggle_data//shop//reduced.csv" 
loc_out_seasons = "//home//harini//Kaggle_data//shop//seasonality.csv"


def get_month(s1):
	date_format = "%Y-%m-%d"
	a = datetime.strptime(s1, date_format)
	return (a.month, a.year)
	

def generate_season_transactions(loc_offers,loc_transactions, loc_out_seasons):
	#keep a dictionary with the offer categories
	categories = {}
	for e, line in enumerate( open(loc_offers) ):
		if e > 0: #skip header
			row = line.strip().split(",")
			categories[ row[1] ] = row[1]
			print(categories[ row[1]])
			
	#open output file
	season_data={}
	for e, line in enumerate(categories):
		season_data[line] = [0]*36
		print(line)
	out_season = open(loc_out_seasons, "w+")
	try:
		#iterate through reduced dataset 
		for e, line in enumerate( open(loc_transactions) ):
			if e > 0: #skip header
				#poor man's csv reader
				row = line.strip().split(",")
				#check if transaction is part of list of offer categories
				if row[3] in categories:
					month_val, year_val = get_month(row[6])
					# only consider transactions between 1st march 2012 to 28th feb 2013
					# we have transactions upto end of july 2013 in the data
					if year_val == 2013 and month_val > 2:
						continue
					season_data[row[3]][3*(month_val-1)] += 1
					season_data[row[3]][3*(month_val-1)+1] += float(row[9])
					season_data[row[3]][3*(month_val-1)+2] += float(row[10])
					
				if e % 100000 == 0:
					print e
		
		for e, v in enumerate(categories):
			outline = v + ","
			temp = season_data[v]
			peak = np.argmax(temp[1:36:3])
			print(peak)
			for e2, v2 in enumerate(temp):
				outline += str(v2)+","
			outline += str(peak)+","
			outline += "\n"	
			print(outline)
			out_season.write( outline )
	finally:
		out_season.close()
		
#generate_season_transactions(loc_offers, loc_transactions, loc_out_seasons)

data = np.genfromtxt(loc_out_seasons, delimiter = ',') 
[N,m] = data.shape
print(data.shape)

for e in range(N):
	plot(np.arange(1,12+1,1),data[e,np.arange(1,m-2,3)])
	plot(np.arange(1,12+1,1),data[e,np.arange(2,m-2,3)])
	plot(np.arange(1,12+1,1),data[e,np.arange(3,m-2,3)])
	show()
## Aha! all categories seem to peak either in march(most), june(two) or dec(one)
