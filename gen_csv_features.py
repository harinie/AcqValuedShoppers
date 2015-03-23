#!/usr/bin/python
#Kaggle Challenge: 
#"http://www.kaggle.com/c/acquire-valued-shoppers-challenge/" 
#'Reduce the data and generate features' by Triskelion 
#After a forum post by BreakfastPirate
#Very mediocre and hacky code, single-purpose, but pretty fast

from datetime import datetime, date
from collections import defaultdict

loc_offers = "kaggle_shop//offers.csv"

def diff_days(s1,s2):
	date_format = "%Y-%m-%d"
	a = datetime.strptime(s1, date_format)
	b = datetime.strptime(s2, date_format)
	delta = b - a
	return delta.days


loc_train = "kaggle_shop//trainHistory.csv"
loc_test = "kaggle_shop//testHistory.csv"
loc_transactions = "kaggle_shop//reduced2.csv"
loc_out_train = "kaggle_shop//train.csv"
loc_out_test = "kaggle_shop//test.csv"
def generate_features(loc_train, loc_test, loc_transactions, loc_out_train, loc_out_test):
	#keep a dictionary with the offerdata
	offers = {}
	for e, line in enumerate( open(loc_offers) ):
		row = line.strip().split(",")
		offers[ row[0] ] = row

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
		features = defaultdict(float)
		features['has_bought_company'] = 0 
		features['has_bought_company_q'] = 0
		features['has_bought_company_a'] = 0
		features['has_bought_company_30'] = 0
		features['has_bought_company_q_30'] = 0
		features['has_bought_company_a_30'] = 0
		features['has_bought_company_60'] = 0
		features['has_bought_company_q_60'] = 0
		features['has_bought_company_a_60'] = 0
		features['has_bought_company_90'] = 0
		features['has_bought_company_q_90'] = 0
		features['has_bought_company_a_90'] = 0						
		features['has_bought_company_180'] = 0
		features['has_bought_company_q_180'] = 0
		features['has_bought_company_a_180'] = 0	
		features['has_bought_category'] = 0
		features['has_bought_category_q'] = 0
		features['has_bought_category_a'] = 0
		features['has_bought_category_30'] = 0
		features['has_bought_category_q_30'] = 0
		features['has_bought_category_a_30'] = 0
		features['has_bought_category_60'] = 0
		features['has_bought_category_q_60'] = 0
		features['has_bought_category_a_60'] = 0
		features['has_bought_category_90'] = 0
		features['has_bought_category_q_90'] = 0
		features['has_bought_category_a_90'] = 0		
		features['has_bought_category_180'] = 0
		features['has_bought_category_q_180'] = 0
		features['has_bought_category_a_180'] = 0
		features['has_bought_brand'] = 0
		features['has_bought_brand_q'] = 0
		features['has_bought_brand_a'] = 0
		features['has_bought_brand_30'] = 0
		features['has_bought_brand_q_30'] = 0
		features['has_bought_brand_a_30'] = 0	
		features['has_bought_brand_60'] = 0
		features['has_bought_brand_q_60'] = 0
		features['has_bought_brand_a_60'] = 0			
		features['has_bought_brand_90'] = 0
		features['has_bought_brand_q_90'] = 0
		features['has_bought_brand_a_90'] = 0			
		features['has_bought_brand_180'] = 0
		features['has_bought_brand_q_180'] = 0
		features['has_bought_brand_a_180'] = 0						
		features['label'] = 0
		features['offer_value'] = 0
		features['offer_quantity'] = 0
		features['total_spend'] = 0
		features['has_bought_brand_company_category'] = 0
		features['has_bought_brand_category'] = 0
		features['has_bought_brand_company'] = 0
		
		headerflag = True
		for e, line in enumerate( open(loc_transactions) ):
			if e > 0: #skip header
				#poor man's csv reader
				row = line.strip().split(",")
				#write away the features when we get to a new shopper id
				
				if last_id != row[0] and e != 1:
					#generate negative features
					if features['has_bought_brand'] > 0 and features['has_bought_category'] > 0 and features['has_bought_company'] > 0:
						features['has_bought_brand_company_category'] = 1

				
					if features['has_bought_brand'] > 0 and features['has_bought_category'] > 0:
						features['has_bought_brand_category'] = 1
			
						
					if features['has_bought_brand'] > 0 and features['has_bought_company'] > 0:
						features['has_bought_brand_company'] = 1
					
					if 	features['has_bought_brand'] > 0:
						features['never_bought_brand'] = 0
					else:
						features['never_bought_brand'] = 1

					if 	features['has_bought_category'] > 0:
						features['never_bought_category'] = 0
					else:
						features['never_bought_category'] = 1
						
					if 	features['has_bought_company'] > 0:
						features['never_bought_company'] = 0	
					else:
						features['never_bought_company'] = 1
					
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
						print features['has_bought_brand']
						print features['has_bought_category']
						print features['has_bought_company']
						print features['has_bought_brand_company_category']
						print outline
						for k, v in features.items():
							print k,v 
							print "\n"

					
					#print "Writing features or storing them in an array"
					#reset features
					features = defaultdict(float)
					features['has_bought_company'] = 0 
					features['has_bought_company_q'] = 0
					features['has_bought_company_a'] = 0
					features['has_bought_company_30'] = 0
					features['has_bought_company_q_30'] = 0
					features['has_bought_company_a_30'] = 0
					features['has_bought_company_60'] = 0
					features['has_bought_company_q_60'] = 0
					features['has_bought_company_a_60'] = 0
					features['has_bought_company_90'] = 0
					features['has_bought_company_q_90'] = 0
					features['has_bought_company_a_90'] = 0						
					features['has_bought_company_180'] = 0
					features['has_bought_company_q_180'] = 0
					features['has_bought_company_a_180'] = 0	
					features['has_bought_category'] = 0
					features['has_bought_category_q'] = 0
					features['has_bought_category_a'] = 0
					features['has_bought_category_30'] = 0
					features['has_bought_category_q_30'] = 0
					features['has_bought_category_a_30'] = 0
					features['has_bought_category_60'] = 0
					features['has_bought_category_q_60'] = 0
					features['has_bought_category_a_60'] = 0
					features['has_bought_category_90'] = 0
					features['has_bought_category_q_90'] = 0
					features['has_bought_category_a_90'] = 0		
					features['has_bought_category_180'] = 0
					features['has_bought_category_q_180'] = 0
					features['has_bought_category_a_180'] = 0
					features['has_bought_brand'] = 0
					features['has_bought_brand_q'] = 0
					features['has_bought_brand_a'] = 0
					features['has_bought_brand_30'] = 0
					features['has_bought_brand_q_30'] = 0
					features['has_bought_brand_a_30'] = 0	
					features['has_bought_brand_60'] = 0
					features['has_bought_brand_q_60'] = 0
					features['has_bought_brand_a_60'] = 0			
					features['has_bought_brand_90'] = 0
					features['has_bought_brand_q_90'] = 0
					features['has_bought_brand_a_90'] = 0			
					features['has_bought_brand_180'] = 0
					features['has_bought_brand_q_180'] = 0
					features['has_bought_brand_a_180'] = 0						
					features['label'] = 0
					features['offer_value'] = 0
					features['offer_quantity'] = 0
					features['total_spend'] = 0
					features['has_bought_brand_company_category'] = 0
					features['has_bought_brand_category'] = 0
					features['has_bought_brand_company'] = 0
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
						
				
					features['offer_value'] = offers[ history[2] ][4]
					features['offer_quantity'] = offers[ history[2] ][2]
					offervalue = offers[ history[2] ][4]
					
					features['total_spend'] += float( row[10] )
					
					if offers[ history[2] ][3] == row[4]:
						features['has_bought_company'] += 1.0
						features['has_bought_company_q'] += float( row[9] )
						features['has_bought_company_a'] += float( row[10] )
						
						date_diff_days = diff_days(row[6],history[-1])
						if date_diff_days < 30:
							features['has_bought_company_30'] += 1.0
							features['has_bought_company_q_30'] += float( row[9] )
							features['has_bought_company_a_30'] += float( row[10] )
						if date_diff_days < 60:
							features['has_bought_company_60'] += 1.0
							features['has_bought_company_q_60'] += float( row[9] )
							features['has_bought_company_a_60'] += float( row[10] )
						if date_diff_days < 90:
							features['has_bought_company_90'] += 1.0
							features['has_bought_company_q_90'] += float( row[9] )
							features['has_bought_company_a_90'] += float( row[10] )
						if date_diff_days < 180:
							features['has_bought_company_180'] += 1.0
							features['has_bought_company_q_180'] += float( row[9] )
							features['has_bought_company_a_180'] += float( row[10] )
						
					if offers[ history[2] ][1] == row[3]:
						
						features['has_bought_category'] += 1.0
						features['has_bought_category_q'] += float( row[9] )
						features['has_bought_category_a'] += float( row[10] )
						date_diff_days = diff_days(row[6],history[-1])
						if date_diff_days < 30:
							features['has_bought_category_30'] += 1.0
							features['has_bought_category_q_30'] += float( row[9] )
							features['has_bought_category_a_30'] += float( row[10] )
						if date_diff_days < 60:
							features['has_bought_category_60'] += 1.0
							features['has_bought_category_q_60'] += float( row[9] )
							features['has_bought_category_a_60'] += float( row[10] )
						if date_diff_days < 90:
							features['has_bought_category_90'] += 1.0
							features['has_bought_category_q_90'] += float( row[9] )
							features['has_bought_category_a_90'] += float( row[10] )						
						if date_diff_days < 180:
							features['has_bought_category_180'] += 1.0
							features['has_bought_category_q_180'] += float( row[9] )
							features['has_bought_category_a_180'] += float( row[10] )
							
					if offers[ history[2] ][5] == row[5]:
						features['has_bought_brand'] += 1.0
						features['has_bought_brand_q'] += float( row[9] )
						features['has_bought_brand_a'] += float( row[10] )
						date_diff_days = diff_days(row[6],history[-1])
						if date_diff_days < 30:
							features['has_bought_brand_30'] += 1.0
							features['has_bought_brand_q_30'] += float( row[9] )
							features['has_bought_brand_a_30'] += float( row[10] )
						if date_diff_days < 60:
							features['has_bought_brand_60'] += 1.0
							features['has_bought_brand_q_60'] += float( row[9] )
							features['has_bought_brand_a_60'] += float( row[10] )
						if date_diff_days < 90:
							features['has_bought_brand_90'] += 1.0
							features['has_bought_brand_q_90'] += float( row[9] )
							features['has_bought_brand_a_90'] += float( row[10] )						
						if date_diff_days < 180:
							features['has_bought_brand_180'] += 1.0
							features['has_bought_brand_q_180'] += float( row[9] )
							features['has_bought_brand_a_180'] += float( row[10] )	
						
				last_id = row[0]
				if e % 100000 == 0:
					print e
	finally:
		out_train.close()
		out_test.close()
		
generate_features(loc_train, loc_test, loc_transactions, loc_out_train, loc_out_test)

