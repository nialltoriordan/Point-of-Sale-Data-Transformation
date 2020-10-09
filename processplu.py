# -*- coding: utf-8 -*-
"""
Program to extract and transform PLU sales data from a Point Of Sale terminal to .CSV format.

The program finds every file in startDir and it's subdirectories, opens any that begin with "PLU1",  
parses the text, adds it to a list of strings, checks for errors, then outputs the list to outputFile.

Program requires pricelist.csv in the same directory, containing "PLU Text" which describes items as 
they appear on the POS terminal, and "Price".

Potential errors caused by other files beginning with "PLU1" that are not in correct format.  This
program does deal with missing/incorrect entries, as are more common in these reports.  Changing 
prices between reports will cause a lot more 'Likely error' reports.

Errors - currently getting weird errors adding extra digits on some items long after the decimal 
point.  Seems to be happening at random.  Going to put a workaround in to round down to two digits
and hope no more problems are caused.

Future work :
Build in support for changing prices depending on date.
"""
#re is a text processing package
import re
import os
import pandas as pd

startDir = 'F:/backup/till/backup'
outputFile = 'daily plu.csv'




def findPLU(sstring, price):
	cLine = ''
	if(sstring in words) :
		cIndex = words.index(sstring)
		count = float(words[cIndex + 2])
		total = float(words[cIndex + 3][1:])
		cLine += words[cIndex + 2]  + ', ' 
		cLine += words[cIndex + 3][1:]  + ', ' 
		if(round((count * price), 2) != total) :  #compare expected total against actual
			print ('Likely error value found for', sstring, 'on', currentDate, '. Expected : ', (count * price ), '. Found : ', total)
	else :
			cLine += '0, 0, '
	return cLine

priceList = pd.read_csv("pricelist.csv", header=0, index_col=False) 


#create the column header row
#Date	Mushrooms Mushrooms T Mars	Mars T	Malteesers	Malteesers T	Snack	Snack T	Kit Kat	Kit Kat T	Refresher	Refresher T	Dairy Milk	Dairy Milk T
#Chew Gum	Chew Gum T	Half Bacon	Half Bacon T	Bacon 	Bacon T	Bacon Dbl Ch	Bacon Dbl Ch T	Half Curry	Half Curry T	BBQ	BBQ T	
#Curry	Curry T	Coleslaw	Coleslaw T	Cheese	Cheese T	Garlic Mayo	Garlic Mayo T	Mayo	Mayo T	Peas	Peas T	Extra Topping	
#Extra Topping T	Salsa C	Salsa T	Sweet Chilli	Sweet Chilli T	Taco	Taco T	Can	Can T	Bottle	Bottle T	Big Bottle	Big Bottle T	
#Milk	Milk T	Water	Water T	Half Dippers	Half Dippers T	Dippers	Dippers T	Breast Bun	Breast Bun T	Fillet	Fillet T	
#Half Rings	Half Rings T	Burger	Burger T	Cheese Burger	Cheese Burger T	Dbl Burger	Dbl Burger T	Dbl Ch Burger	Dbl Ch Burger T	
#Chick Burger	Chick Burger T	Veg Burger	Veg Burger T	Battered Burger	Battered Burger T	Battered Sausage	Battered Sausage T	
#Pea Fritter	Pea Fritter T	Onion Rings	Onion Rings T	Chips	Chips T	Lg Chips	Lg Chips T	Fish	Fish T	Breast	Breast T	
#Leg	Leg T	Sausage	Sausage T	Potato Pie	Potato Pie T	Nuggets	Nuggets T	Mozz Sticks	Mozz Sticks T	Sausage Burger	Sausage Burger T	
#Scoop Chips	Scoop Chips T	Half Nuggets	Half Nuggets T	Half Mozz	Half Mozz T

headerLine = "Date"

for index, row in priceList.iterrows():
    headerLine += ", " + row['PLU Text'] + ", " +  row['PLU Text'] + " T"
    
headerLine += " \n"

#create the data  row
contentLine = ''

#travese startDir and subdirectories to find appropriate files
for root, dirs, files in os.walk(startDir):
	for filename in files:
		if filename.startswith("PLU1") :
			print(filename)
			with open(os.path.join(root, filename), "r") as file :
		
				lines = file.readlines()
				#file.close()
				#create a holder for all the words we want to keep
				words=[]
				#for every line in the file we just read in
				for line in lines:
					#strip newline char from end of the line
					line = line.strip()
					#split the line into words anywhere two consecutive spaces exist
					wordList = re.split(r'  {2,}', line)
					#if there's more than one word on the line, save the words
					if len(wordList)>1:
						words = words + wordList
						
				currentDate = ''
				
				if('DATE' in words) :
					contentLine += words[(words.index('DATE'))+1] + ', '   #add Date
					currentDate = words[(words.index('DATE'))+1]
				else :
					print ('No date found - probably going to be a lot of errors!')
					
				for index, row in priceList.iterrows():
					contentLine += findPLU(row['PLU Text'], row['Price'])
                
				contentLine += '\n'	                

	


#save the header and data out to a file
outputfile = open(outputFile, 'w')
outputfile.write(headerLine)
outputfile.write(contentLine)
outputfile.close()
