# -*- coding: utf-8 -*-
"""
Program to extract and transform sales data from a Point Of Sale terminal to .CSV format. 

The program finds every file in startDir and it's subdirectories, opens any that begin with "FIN1",  
parses the text, adds it to a list of strings, then outputs the list to outputFile.

Data is then processed to seperate data by day, then add the weekly total to the end.  To 
save development time I'm going to just add new code to the end of the old program.  This
will be inefficient, but these programs don't take long to run anyway.

NB - Program intended to be used to process one week's worth of X/Z reports.

Potential errors caused by other files beginning with "FIN1" that are not in correct format. 
"""
#re is a text processing package
import re
import os
import pandas as pd
import numpy as np

startDir = 'F:/backup/till/backup'
outputFile = 'dailyfin.csv'
outputFile2 = 'dailyfinrep.csv'


#create the column header row
#Date	PLU Count	PLU Total	Net Sales	Prev Void	Cash Sales	No Sales	Total
headerLine = 'Date, PLU Count, PLU Total, Net Sales, Prev Void, Cash Sales, No Sales, Total' + '\n'

#create the data  row
contentLine = ''

#travese startDir and subdirectories to find appropriate files
for root, dirs, files in os.walk(startDir):
	for filename in files:
		if filename.startswith("FIN1") :
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
		
				
				#not very efficient but short array to loop through
				
				if ('DATE' in words) :
					cIndex = words.index('DATE')
					contentLine +=words[cIndex + 1] + ', ' #add Date
				else :
					contentLine += '0, '  #add null			

				if ('+PLU LVL1 TTL' in words) :
					cIndex = words.index('+PLU LVL1 TTL')
					contentLine += words[cIndex+1] + ', '  #add PLU Count
					contentLine += words[cIndex+2][1:] + ', '  #add PLU Total
				else :
					contentLine += '0, '  #add null	
					contentLine += '0, '  #add null	
					
				if ('NET SALES' in words) :
					cIndex = words.index('NET SALES')
					contentLine += words[cIndex+1] + ', '  #add net sales
				else :
					contentLine += '0, '  #add null	
				
				if ('PREVIOUS VOID' in words) :
					cIndex = words.index('PREVIOUS VOID')
					contentLine += words[cIndex+1] + ', '  #add Prev Void
				else :
					contentLine += '0' ', '  #add null						

				if ('CASH SALES' in words) :
					cIndex = words.index('CASH SALES')
					contentLine += words[cIndex+1] + ', '  #add Cash Sales
				else :
					contentLine += '0, '  #add null	
					
				if ('NO SALE/NON-ADD#' in words) :
					cIndex = words.index('NO SALE/NON-ADD#')
					contentLine += words[cIndex+1] + ', '  #add no sales
				else :
					contentLine += '0, '  #add null	

				if ('DRAWER1 TOTAL' in words) :
					cIndex = words.index('DRAWER1 TOTAL')
					contentLine += words[cIndex+1][1:] + ', '  #add total
				else :
					contentLine += '0, '  #add null						
		
				contentLine += '\n'	
				



#save the header and data out to a file
outputfile = open(outputFile, 'w')
outputfile.write(headerLine)
outputfile.write(contentLine)
outputfile.close()


col_names = ['Date', 'PLU Count', 'PLU Total', 'Net Sales', 'Prev Void', 'Cash Sales', 'No Sales', 'Total']
fin_data = pd.read_csv(outputFile, header=0, index_col=False) 


fin_data.columns = col_names

weekly_total = pd.DataFrame(fin_data[-1:].values, columns=fin_data.columns)

date_col = fin_data['Date']
fin_data = fin_data.drop('Date', axis=1)  


new_data = pd.DataFrame(fin_data[:1].values, columns=fin_data.columns)


for index, row in fin_data.iterrows():
	if(index != 0) :
		new_row = fin_data.loc[index] - fin_data.loc[index-1]
		new_data = new_data.append(new_row, ignore_index=True)
		
new_data['Date'] = date_col 


new_data = new_data.append(weekly_total)
new_data = new_data[col_names]




new_data.to_csv(outputFile2, index=False)


