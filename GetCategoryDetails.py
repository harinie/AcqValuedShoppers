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
loc_out_cat = "//home//harini//Kaggle_data//shop//catDetails"


def get_month(s1):
	date_format = "%Y-%m-%d"
	a = datetime.strptime(s1, date_format)
	return (a.month, a.year)
	

def generate_category_dict(loc_offers,loc_transactions, loc_out_seasons):
	#keep a dictionary with the offer categories
	categories = {}
	
	for e, line in enumerate( open(loc_offers) ):
		if e > 0: #skip header
			row = line.strip().split(",")
			categories[ row[1] ] = row[1]
			print(categories[ row[1]])
	
	total_value = defaultdict(float)
	no_units = defaultdict(float)
	purchase_size = defaultdict(float)
	#iterate through reduced dataset 
	
	for e, line in enumerate( open(loc_transactions) ):
		if e > 0: #skip header
			#poor man's csv reader
			row = line.strip().split(",")
			#check if transaction is part of list of offer categories
			if row[3] in categories:
				category = row[3]
				company = row[4]
				brand = row[5]
				second_key = company + "_" + brand
				purchaseamount = float(row[10])
				purchasequant =  float(row[9])
				purchasesize = float(row[7])
				if (purchasequant > 0) and (purchasesize > 0):
					value_per_unit = purchaseamount/(purchasequant*purchasesize)
				else:
					value_per_unit = 0
				total_value[category,second_key] += value_per_unit
				purchase_size[category,second_key] += float(row[7])
				no_units[category,second_key] += 1.0

			if e % 100000 == 0:
				print e

	
	#get all key tuples
	all_keys = total_value.keys()
	outline = ""
	for k, v in enumerate(categories):
		#create new file for each categories
		filename= loc_out_cat+"_"+v+".csv"
		cb_keys=[]
		#get all keys for that category
		for x in all_keys:
			if x[0]==v:
				cb_keys.append(x[1])
		print(cb_keys)
		
		try:
			outfile = open(filename, "w+")
			for l, m in enumerate(cb_keys):
				if( no_units[v,m] > 0):
					final_value = total_value[v,m]/no_units[v,m]
					average_purchase_size = purchase_size[v,m]/no_units[v,m]
				else:
					final_value = 0
					print('Error'+v+m+"\n")
				outline = m+","+str(final_value) +","+str(average_purchase_size) +"\n"
				outfile.write( outline )
		finally:
			outfile.close()
		
generate_category_dict(loc_offers, loc_transactions, loc_out_cat)
