# -*- coding: utf-8 -*-
"""
Program to extract and transform sales data from a Point Of Sale terminal to .CSV format.  An 
example of typical content is below.

The program finds every file in startDir and it's subdirectories, opens any that begin with "FIN1",  
parses the text, adds it to a list of strings, then outputs the list to outputFile.

Potential errors caused by other files beginning with "FIN1" that are not in correct format.  Also 
by missing entries, but not going to worry about these unless they happen.

***Update***
I moticed a bug when trying to use this program to process daily entries : not every file contains  
a 'PREVIOUS VOID' entry.  Also, this isn't always directly after 'NET SALES'.  I'm going to add a 
work around rather than rewrite the entire program - I should rewrite to a style similar to 
processplu.py, but I'm going to leave as is to demonstrate this style of parsing text. 

Similar bug work around implemented for 'NO SALE/NON-ADD#'.

***Notice***
This file now superceeded by processfindaily.py.  New program is more error tolerant, but I'm 
leaving this as is to demonstrate this style of parsing.


DATE           26/08/2018            SUN
FINANCIAL REPORT                        
Z1 REPORT                           0841
                                        
DESCRIPTOR            COUNT        TOTAL
________________________________________
+PLU LVL1 TTL          1966     €4243.85
ADJST TTL              1966     €4243.85
----------------------------------------
NON-TAX                         €4243.85
                                        
NET SALES               399     €4243.85
PREVIOUS VOID            25       -84.80
CANCEL                    1        €4.30
                                        
GROSS SALES                     €4243.85
----------------------------------------
CASH SALES              399     €4243.85
NO SALE/NON-ADD#         36            0
----------------------------------------
CASH-IN-DRAWER                  €4243.85
                                        
DRAWER1 TOTAL                   €4243.85
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
						if('PREVIOUS VOID' in words) :
							cIndex = words.index(sstring)
							contentLine += words[cIndex+1] + ', '  #add Prev Void
							i += 1
						else :
							contentLine += '0' ', '  #add Prev Void
							i += 1
					elif words[i] == 'CASH SALES' :
						contentLine += words[i+1] + ', '  #add Cash Sales
						i += 1
						if('NO SALE/NON-ADD#' in words) :
							cIndex = words.index(sstring)
							contentLine += words[cIndex+1] + ', '  #add Prev Void
							i += 1
						else :
							contentLine += '0' ', '  #add Prev Void
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
