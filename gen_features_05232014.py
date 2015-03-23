	#!/usr/bin/python
#Kaggle Challenge: 
#"http://www.kaggle.com/c/acquire-valued-shoppers-challenge/" 
#'Reduce the data and generate features' by Triskelion 
#After a forum post by BreakfastPirate
#Very mediocre and hacky code, single-purpose, but pretty fast

from datetime import datetime, date
from collections import defaultdict	

loc_offers = "//home//harini//Kaggle_data//shop//offers.csv"
loc_season = "//home//harini//Kaggle_data//shop//seasonality.csv"
loc_transactions = "//home//harini//Kaggle_data//shop//reduced.csv" 
loc_train = "//home//harini//Kaggle_data//shop//trainHistory.csv"
loc_test = "//home//harini//Kaggle_data//shop//testHistory.csv"
loc_out_train = "//home//harini//Kaggle_data//shop//train_05252014.csv"
loc_out_test = "//home//harini//Kaggle_data//shop//test_05252014.csv"

def diff_days(s1,s2):
	date_format = "%Y-%m-%d"
	a = datetime.strptime(s1, date_format)
	b = datetime.strptime(s2, date_format)
	delta = b - a
	return (delta.days,b.month)
	
def get_month(s1):
	date_format = "%Y-%m-%d"
	a = datetime.strptime(s1, date_format)
	return (a.month,a.year)
	
def generate_new_dict():
	features = defaultdict(float)
	#Booleans
	features['has_bought_category'] = 0 
	features['has_bought_cb'] = 0 
	

	#Repeat all the above for 30, 60, 90, 180 days
	#Booleans
	features['has_bought_category_30'] = 0 
	features['has_bought_cb_30'] = 0 
	
	# 60
	#Booleans
	features['has_bought_category_60'] = 0 
	features['has_bought_cb_60'] = 0 

	# 90
	#Booleans
	features['has_bought_category_90'] = 0 
	features['has_bought_cb_90'] = 0 

	# 180
	#Booleans
	features['has_bought_category_180'] = 0 
	features['has_bought_cb_180'] = 0 

	#more features	
	features['label'] = 0
	features['offer_value'] = 0  #now per unit
	
	#interaction booleans
	features['has_bought_cb_category'] = 0
	
	#cross-validation will be split on category
	features['category'] = 0

	#category seasonality
	features['offer_time_from_peak'] = 0
	
	#average value of object purchased in other cb by user
	features['average_val_other_cb'] = 0
	
	#average value of object in offer cb
	features['average_val_cb'] = 0

	
	return features
	

def generate_features(loc_train, loc_test, loc_transactions, loc_out_train, loc_out_test):
	#keep a dictionary with the offerdata
	offers = {}
	for e, line in enumerate( open(loc_offers) ):
		row = line.strip().split(",")
		offers[ row[0] ] = row
		
	#keep a dictionary with the seasonality
	seasonality = {}
	for e, line in enumerate( open(loc_season) ):
		row = line.strip().split(",")
		seasonality[ row[0] ] = row[37]
		
	#load all category details
	catDetails = {}
	for cats in seasonality.keys():
		category_file = "//home//harini//Kaggle_data//shop//catDetails"+"_"+cats+".csv"
		for e, line in enumerate( open(category_file) ):
			row = line.strip().split(",")
			catDetails[cats,row[0],"average_price"] = row[1]
			catDetails[cats,row[0],"average_size"] = row[2]
		
	#keep two dictionaries with the shopper id's from test and train
	train_ids = {}
	test_ids = {}
	for e, line in enumerate( open(loc_train) ):
		if e > 0:
			row = line.strip().split(",")
			train_ids[row[0]] = row
	for e, line in enumerate( open(loc_test) ):
		if e > 0:
			row = line.strip().split(",")
			test_ids[row[0]] = row
			
	#open two output files
	out_train = open(loc_out_train, "w+")
	out_test = open(loc_out_test, "w+")
	try:
		#iterate through reduced dataset 
		last_id = 0
		features = generate_new_dict()
		no_times_other_cb = 0
		headerflag = True
		for e, line in enumerate( open(loc_transactions) ):
			if e > 0: #skip header
				#poor man's csv reader
				row = line.strip().split(",")
				#write away the features when we get to a new shopper id
				
				if last_id != row[0] and e != 1:
					#generate interaction features
					if features['has_bought_cb'] > 0 and features['has_bought_category'] > 0:
						features['has_bought_cb_category'] = 1
					
					#convert total into average, reset count
					if no_times_other_cb>0:
						features['average_val_other_cb'] = features['average_val_other_cb']/no_times_other_cb
						no_times_other_cb = 0
					
					if features['average_val_other_cb'] == 0:
						features['average_val_other_cb'] = features['average_val_cb'] 
					
					# write header for train and test csv files
					if headerflag :
						outline = "id,"
						for k, v in sorted(features.items()):
							outline += k+","
						outline += "\n"
						out_test.write( outline )
						out_train.write( outline )
						headerflag = False
			
					outline = last_id + ","
					test = False
					for k, v in sorted(features.items()):
						if k == "label" and v == 0.5:
							#test
							test = True
						outline += str(v)+","
					outline += "\n"
					if test:
						out_test.write( outline )
					else:
						out_train.write( outline )
					
					if last_id == "457362299" or last_id == "4274569163":
						print features['has_bought_cb']
						print features['has_bought_category']
						print features['has_bought_cb_30']
						print features['has_bought_cb_category']
						print outline
						for k, v in features.items():
							print k,v 
							print "\n"

					
					#print "Writing features or storing them in an array"
					#reset features
					features = generate_new_dict()
					
				#generate features from transaction record
				#check if we have a test sample or train sample
				if row[0] in train_ids or row[0] in test_ids:
					#generate label and history
					if row[0] in train_ids:
						history = train_ids[row[0]]
						if train_ids[row[0]][5] == "t":
							features['label'] = 1
						else:
							features['label'] = 0
					else:
						history = test_ids[row[0]]
						features['label'] = 0.5
						
				
					
					offervalue = offers[ history[2] ][4]
					offer_category = offers[ history[2] ][1]
					offer_company = offers[ history[2] ][3]
					offer_brand = offers[ history[2] ][5]
					offer_key = offer_company + "_" + offer_brand
					
					trans_category = row[3]
					trans_company = row[4]
					trans_brand = row[5]
					trans_cb_key = trans_company+"_"+trans_brand
					
					features['average_val_cb'] = float(catDetails[offer_category,offer_key,"average_price"])
					features['category'] =  offer_category
					features['offer_value'] = float(offervalue)/float(catDetails[offer_category,offer_key,"average_size"])				
					
					
					date_diff_days, offer_month = diff_days(row[6],history[-1])						
					# if customer has shopped for company and brand before
					if offer_key == trans_cb_key:
						features['has_bought_cb'] = 1.0
						if date_diff_days < 30:
							features['has_bought_cb_30'] = 1.0
						if date_diff_days < 60:
							features['has_bought_cb_60'] = 1.0
						if date_diff_days < 90:
							features['has_bought_cb_90'] = 1.0
						if date_diff_days < 180:
							features['has_bought_cb_180'] = 1.0
							
					# if customer has shopped for category before	
					if offer_category == trans_category:
						features['has_bought_category'] = 1.0
						if date_diff_days < 30:
							features['has_bought_category_30'] = 1.0
						if date_diff_days < 60:
							features['has_bought_category_60'] = 1.0
						if date_diff_days < 90:
							features['has_bought_category_90'] = 1.0
						if date_diff_days < 180:
							features['has_bought_category_180'] = 1.0
						if trans_cb_key != offer_key:
							features['average_val_other_cb'] += float(catDetails[trans_category,trans_cb_key,"average_price"])
							no_times_other_cb += 1
																	
					# if the customer was made the offer in peak time		
					features['offer_time_from_peak'] = min(abs(offer_month - float(seasonality[ offer_category])),abs(float(seasonality[ offer_category ]) - offer_month))
												
				last_id = row[0]
				if e % 100000 == 0:
					print e
	finally:
		out_train.close()
		out_test.close()
		
generate_features(loc_train, loc_test, loc_transactions, loc_out_train, loc_out_test)
