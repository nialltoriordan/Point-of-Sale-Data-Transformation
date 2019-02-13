# -*- coding: utf-8 -*-
"""
Program to extract and transform sales data from a Point Of Sale terminal to .CSV format.

The program finds every file in startDir and it's subdirectories, opens any that begin with "FIN1",  
parses the text, adds it to a list of strings, then outputs the list to outputFile.

Potential errors caused by other files beginning with "FIN1" that are not in correct format.  Also 
by missing entries, but not going to worry about these unless they happen.
"""
#re is a text processing package
import re
import os

startDir = 'F:/backup/till/backup'
outputFile = 'test.csv'



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
		
				i = 0
				#not very efficient but short array to loop through
				while i < len(words):
					if words[i] == 'DATE' :
						contentLine += words[i+1] + ', ' #add Date
						i += 1
					elif words[i] == '+PLU LVL1 TTL' :
						contentLine += words[i+1] + ', '  #add PLU Count
						contentLine += words[i+2] + ', '  #add PLU Total
						i += 2
					elif words[i] == 'NET SALES' :
						contentLine += words[i+1] + ', '  #add Net Sales
						i += 1
					elif words[i] == 'PREVIOUS VOID' :
						contentLine += words[i+1] + ', '  #add Prev Void
						i += 1
					elif words[i] == 'CASH SALES' :
						contentLine += words[i+1] + ', '  #add Cash Sales
						i += 1
					elif words[i] == 'NO SALE/NON-ADD#' :
						contentLine += words[i+1] + ', '  #add No Sales
						i += 1
					elif words[i] == 'DRAWER1 TOTAL' :
						contentLine += words[i+1] + ', '  #add Total
						i += 1
		
					i += 1
		
				contentLine += '\n'	
				
	


#save the header and data out to a file
outputfile = open(outputFile, 'w')
outputfile.write(headerLine)
outputfile.write(contentLine)
outputfile.close()
