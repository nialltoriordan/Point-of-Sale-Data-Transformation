# -*- coding: utf-8 -*-
"""
Program to extract and transform PLU sales data from a Point Of Sale terminal to .CSV format.

The program finds every file in startDir and it's subdirectories, opens any that begin with "PLU1",  
parses the text, adds it to a list of strings, checks for errors, then outputs the list to outputFile.

Potential errors caused by other files beginning with "PLU1" that are not in correct format.  This
program does deal with missing/incorrect entries, as are more common in these reports.  Changing 
prices between reports will cause a lot more 'Likely error' reports.

Errors - currently getting weird errors adding extra digits on some items long after the decimal 
point.  Seems to be happening at random.  Going to put a workaround in to round down to two digits
and hope no more problems are caused.

Similar to genfinreports I'm going to expand this to process the data and give daily numbers followed by the weekly total.

Future work :
Read in PLU descriptions and prices from a .CSV file.  Build in support for changing prices depending
on date.
"""
#re is a text processing package
import re
import os
import pandas as pd

startDir = 'F:/backup/till/backup'
outputFile = 'dailyplu.csv'
outputFile2 = 'dailyplurep.csv'


#create the column header row
#Date	Mars	Mars T	Malteesers	Malteesers T	Snack	Snack T	Kit Kat	Kit Kat T	Refresher	Refresher T	Dairy Milk	Dairy Milk T
#Chew Gum	Chew Gum T	Half Bacon	Half Bacon T	Bacon 	Bacon T	Bacon Dbl Ch	Bacon Dbl Ch T	Half Curry	Half Curry T	BBQ	BBQ T	
#Curry	Curry T	Coleslaw	Coleslaw T	Cheese	Cheese T	Garlic Mayo	Garlic Mayo T	Mayo	Mayo T	Peas	Peas T	Extra Topping	
#Extra Topping T	Salsa C	Salsa T	Sweet Chilli	Sweet Chilli T	Taco	Taco T	Can	Can T	Bottle	Bottle T	Big Bottle	Big Bottle T	
#Milk	Milk T	Water	Water T	Half Dippers	Half Dippers T	Dippers	Dippers T	Breast Bun	Breast Bun T	Fillet	Fillet T	
#Half Rings	Half Rings T	Burger	Burger T	Cheese Burger	Cheese Burger T	Dbl Burger	Dbl Burger T	Dbl Ch Burger	Dbl Ch Burger T	
#Chick Burger	Chick Burger T	Veg Burger	Veg Burger T	Battered Burger	Battered Burger T	Battered Sausage	Battered Sausage T	
#Pea Fritter	Pea Fritter T	Onion Rings	Onion Rings T	Chips	Chips T	Lg Chips	Lg Chips T	Fish	Fish T	Breast	Breast T	
#Leg	Leg T	Sausage	Sausage T	Potato Pie	Potato Pie T	Nuggets	Nuggets T	Mozz Sticks	Mozz Sticks T	Sausage Burger	Sausage Burger T	
#Scoop Chips	Scoop Chips T	Half Nuggets	Half Nuggets T	Half Mozz	Half Mozz T

headerLine = 'Date, Mars, Mars T, Malteesers, Malteesers T, Snack, Snack T, Kit Kat, Kit Kat T, Refresher, Refresher T, Dairy Milk, Dairy Milk T, ' 
headerLine += 'Chew Gum, Chew Gum T, Half Bacon, Half Bacon T, Bacon, Bacon T, Bacon Dbl Ch, Bacon Dbl Ch T, Half Curry, Half Curry T, BBQ, BBQ T, ' 
headerLine += 'Pink Sauce, Pink Sauce T, Ketchup, Ketchup, ' 
headerLine += 'Curry, Curry T, Coleslaw, Coleslaw T, Cheese, Cheese T, Garlic Mayo, Garlic Mayo T, Mayo, Mayo T, Peas, Peas T, Extra Topping, ' 
headerLine += 'Extra Topping T, Salsa C, Salsa T, Sweet Chilli, Sweet Chilli T, Taco, Taco T, Can, Can T, Bottle, Bottle T, Big Bottle, Big Bottle T, ' 
headerLine += 'Milk, Milk T, Water, Water T, Half Dippers, Half Dippers T, Dippers, Dippers T, Breast Bun, Breast Bun T, Fillet, Fillet T, ' 
headerLine += 'Half Rings, Half Rings T, Burger, Burger T, Cheese Burger, Cheese Burger T, Dbl Burger, Dbl Burger T, Dbl Ch Burger, Dbl Ch Burger T, ' 
headerLine += 'Chick Burger, Chick Burger T, Veg Burger, Veg Burger T, Battered Burger, Battered Burger T, Battered Sausage, Battered Sausage T, ' 
headerLine += 'Pea Fritter, Pea Fritter T, Onion Rings, Onion Rings T, Chips, Chips T, Lg Chips, Lg Chips T, Fish, Fish T, Breast, Breast T, ' 
headerLine += 'Leg, Leg T, Sausage, Sausage T, Potato Pie, Potato Pie T, Nuggets, Nuggets T, Mozz Sticks, Mozz Sticks T, Sausage Burger, Sausage Burger T, ' 
headerLine += 'Scoop Chips, Scoop Chips T, Half Nuggets, Half Nuggets T, Half Mozz, Half Mozz T' + ' \n' 

#create the data  row
contentLine = ''

def findPLU(sstring, price):
	cLine = ''
	if(sstring in words) :
		cIndex = words.index(sstring)
		count = float(words[cIndex + 2])
		total = float(words[cIndex + 3][1:])
		#cLine += words[cIndex + 2]  + ', ' 
		#cLine += words[cIndex + 3][1:]  + ', ' 
		'''
		Sometimes the total doesn't seem to be what it should be.  It's rare and might be due to a buffer over run on the POS system or something.
		Going to change this to put in what I believe is the correct value.
		'''
		if(round((count * price), 2) != total) :  #compare expected total against actual 
			print ('Likely error value found for', sstring, 'on', currentDate, '. Expected : ', (count * price ), '. Found : ', total)
			cLine += str(count)  + ', ' 
			cLine += str(count * price)  + ', ' 
		else :
			cLine += str(count)  + ', ' 
			cLine += str(total)	 + ', ' 
	else :
			cLine += '0, 0, '
	return cLine

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
				#this is going to be long winded but should be quick to program and easy to read
				if('DATE' in words) :
					contentLine += words[(words.index('DATE'))+1] + ', '   #add Date
					currentDate = words[(words.index('DATE'))+1]
				else :
					print ('No date found - probably going to be a lot of errors!')
					
				contentLine += findPLU('MARS', 1.0)
				contentLine += findPLU('MALTESERS', 0.9)

				contentLine += findPLU('SNACK', 0.55)
				contentLine += findPLU('KIT KAT', 0.9)
				contentLine += findPLU('REFRESHERS', 0.15)
				contentLine += findPLU('DAIRY MILK', 0.9)
				contentLine += findPLU('CHEWING GUM', 0.6)
				
				contentLine += findPLU('HALF BACON', 0.50)
				contentLine += findPLU('BACON', 1.0)
				contentLine += findPLU('BACON DBL CHEESE', 4.5)
				contentLine += findPLU('HALF CURRY', 0.5)
				contentLine += findPLU('BBQ', 1.0)

				contentLine += findPLU('PINK', 1.0)
				contentLine += findPLU('KETCHUP', 1.0)
				
				contentLine += findPLU('TUB CURRY', 1.0)
				contentLine += findPLU('TUB COLESLAW', 1.0)
				contentLine += findPLU('TUB CHEESE', 1.0)
				contentLine += findPLU('TUB GARLIC MAYO', 1.0)
				contentLine += findPLU('TUB MAYO', 1.0)
				
				contentLine += findPLU('TUB PEAS', 1.0)
				contentLine += findPLU('XTRA TOP', 0.5)
				contentLine += findPLU('SALSA', 1.0)
				contentLine += findPLU('SWEET CHILLI', 1.0)
				contentLine += findPLU('TACO', 1.0)
				
				contentLine += findPLU('CAN', 1.25)
				contentLine += findPLU('BOTTLE', 1.8)
				contentLine += findPLU('1.25 LITRE', 2.5)
				contentLine += findPLU('MILK', 0.85)
				contentLine += findPLU('WATER', 1.8)
				
				contentLine += findPLU('HALF DIPPERS', 1.5)
				contentLine += findPLU('DIPPERS', 3.0)
				contentLine += findPLU('BREAST IN BUN', 4.25)
				contentLine += findPLU('SFC FILLET', 3.5)
				contentLine += findPLU('HALF RINGS', 1.25)

				contentLine += findPLU('BEEF BURGER', 2.0)
				contentLine += findPLU('CHEESE BURGER', 2.5)
				contentLine += findPLU('DBL BURGER', 3.0)
				contentLine += findPLU('DBL CH BURGER', 3.5)
				contentLine += findPLU('CHICKEN BURGER', 3.8)
				
				contentLine += findPLU('VEGGIE BURGER', 3.5)
				contentLine += findPLU('BATT BURGER', 1.3)
				contentLine += findPLU('BATT SAUSAGE', 0.7)
				contentLine += findPLU('PEA FRITTER', 1.2)
				contentLine += findPLU('ONION RINGS', 2.5)
				
				contentLine += findPLU('SMALL CHIP', 2.5)
				contentLine += findPLU('LARGE CHIP', 3.5)
				contentLine += findPLU('FISH', 3.5)
				contentLine += findPLU('CHICKEN BREAST', 4.0)
				contentLine += findPLU('CHICKEN LEG', 2.5)
				
				contentLine += findPLU('SAUSAGE', 0.5)
				contentLine += findPLU('POTATO PIE', 1.8)
				contentLine += findPLU('CHK NUGGETS', 2.5)
				contentLine += findPLU('MOZZARELLA STICKS', 3.0)
				contentLine += findPLU('SAUSAGE BURGER', 2.5)
				
				contentLine += findPLU('SCOOP CHIPS', 1.0)
				contentLine += findPLU('HALF NUGGETS', 1.25)
				contentLine += findPLU('HALF MOZZARELLA', 1.5)						
					
					
					
				contentLine += '\n'	
				
	


#save the header and data out to a file
outputfile = open(outputFile, 'w')
outputfile.write(headerLine)
outputfile.write(contentLine)
outputfile.close()

time_data = pd.read_csv(outputFile, header=0, index_col=False) 
col_names = time_data.columns.values

#time_data.columns = col_names

weekly_total = pd.DataFrame(time_data[-1:].values, columns=time_data.columns)

#drop the date column
date_col = time_data['Date']
time_data = time_data.drop('Date', axis=1)  

#get the first line
new_data = pd.DataFrame(time_data[:1].values, columns=time_data.columns)

#for all other lines, new row = current row - previous row
for index, row in time_data.iterrows():
	if(index != 0) :
		new_row = time_data.loc[index] - time_data.loc[index-1]
		new_data = new_data.append(new_row, ignore_index=True)

#add back in the date column		
new_data['Date'] = date_col 

#add in weekly total
new_data = new_data.append(weekly_total)

#sort the data back to original column order
new_data = new_data[col_names]




new_data.to_csv(outputFile2, index=False)