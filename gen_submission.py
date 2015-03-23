#!/usr/bin/python
#Kaggle Challenge: 
#"http://www.kaggle.com/c/acquire-valued-shoppers-challenge/" 
#'Reduce the data and generate features' by Triskelion 
#After a forum post by BreakfastPirate
#Very mediocre and hacky code, single-purpose, but pretty fast

from datetime import datetime, date

loc_preds = "testsubmission_average_05182014.csv"
loc_test = "//home//harini//Kaggle_data//shop//testHistory.csv"
loc_submission = "submission.csv"

def generate_submission(loc_preds, loc_test, loc_submission):
	preds = {}
	for e, line in enumerate( open(loc_preds) ):
		row = line.strip().split(",")
#		if e > 0: #ignore header
		preds[ row[0] ] = row[1]
		
	outfile = open(loc_submission, "w+")
	try:
		for e, line in enumerate( open(loc_test) ):
			if e == 0:
				outfile.write( "id,repeatProbability\n" )
			else:
				row = line.strip().split(",")
				if row[0] not in preds:
					outfile.write(row[0]+",0\n")
				else:
					outfile.write(row[0]+","+preds[row[0]]+"\n")
	finally:
		outfile.close()
generate_submission(loc_preds, loc_test, loc_submission)
