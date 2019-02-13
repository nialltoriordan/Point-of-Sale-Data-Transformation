# -*- coding: utf-8 -*-
"""
Program to extract and transform sales time data from a Point Of Sale terminal to .CSV format.

The program finds every file in startDir and it's subdirectories, opens any that begin with "TIME1",  
parses the text, adds it to a dataframe, then outputs the list to outputFile.

Note : transactions logged after lunchtime / evening hours are added to the previous valid hour.

Potential errors caused by other files beginning with "TIME1" that are not in correct format.  Aslo 
by missing values but won't worry about these unless it happens.  Extra values are dealt with.
"""
#re is a text processing package
import re
import os
import pandas as pd

startDir = 'F:/backup/till/backup'
outputFile = 'timetest.csv'



#create the column header row
#Date	12:00 – 12:59 C	12:00 – 12:59 T	13:00 – 13:59 C	13:00 – 13:59 T	14:00 – 14:59 C	14:00 – 14:59 T	Total Lunchtime	17:00 – 17:59 C	17:00 – 17:59 T	18:00 – 18:59 C	18:00 – 18:59 T	19:00 – 19:59 C	19:00 – 19:59 T	
#20:00 – 20:59 C	20:00 – 20:59 T	21:00 – 21:59 C	21:00 – 21:59 T	22:00 – 22:59 C	22:00 – 22:59 T	Total Evening
headerLine = ['Date', '12:00 : 12:59 C', '12:00 : 12:59 T', '13:00 : 13:59 C', '13:00 : 13:59 T', '14:00 : 14:59 C', '14:00 : 14:59 T', 'Total Lunchtime','17:00 : 17:59 C', '17:00 : 17:59 T', '18:00 : 18:59 C', '18:00 : 18:59 T', '19:00 : 19:59 C', '19:00 : 19:59 T', '20:00 : 20:59 C', '20:00 : 20:59 T', '21:00 : 21:59 C', '21:00 : 21:59 T', '22:00 : 22:59 C', '22:00 : 22:59 T', 'Total Evening']


times = pd.DataFrame(columns=headerLine)

#travese startDir and subdirectories to find appropriate files
for root, dirs, files in os.walk(startDir):
	for filename in files:
		if filename.startswith("TIME1") :
			print(filename)
			with open(os.path.join(root, filename), "r") as file :
			
				lines = file.readlines()
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
						
						
				
				#init variables for this file
				i = 0
				currentRow = []
				overflowc = 0
				overflowt = 0.0
				'''
				currentRow[0]   Date
				currentRow[1]   12:00 - 12:59 C
				currentRow[2]   12:00 - 12:59 T
				currentRow[3]   13:00 - 13:59 C
				currentRow[4]   13:00 - 13:59 T
				currentRow[5]   14:00 - 14:59 C
				currentRow[6]   14:00 - 14:59 T
				currentRow[7]  - lunchtime total
				currentRow[8]   17:00 - 17:59 C
				currentRow[9]   17:00 - 17:59 T
				currentRow[10]   18:00 - 18:59 C
				currentRow[11]   18:00 - 18:59 T
				currentRow[12]   19:00 - 19:59 C
				currentRow[13]   19:00 - 19:59 T
				currentRow[14]   20:00 - 20:59 C
				currentRow[15]   20:00 - 20:59 T
				currentRow[16]   21:00 - 21:59 C
				currentRow[17]   21:00 - 21:59 T
				currentRow[18]   22:00 - 22:59 C
				currentRow[19]   22:00 - 22:59 T				
				currentRow[20]  - evening total				
				'''
				#not very efficient but short array to loop through
				while i < len(words):
					if words[i] == 'DATE' :
						currentRow.append(words[i+1]) #add Date
						i += 1
					elif words[i] == '00:00 - 00:59' :   #shouldn't get these but roll into evening
						overflowc += float(words[i+1])
						overflowt += float(words[i+2][1:])
						i += 2
					elif words[i] == '01:00 - 01:59' :   #shouldn't get these but roll into evening
						overflowc += float(words[i+1])
						overflowt += float(words[i+2][1:])
						i += 2
					elif words[i] == '02:00 - 02:59' :   #shouldn't get these but roll into evening
						overflowc += float(words[i+1])
						overflowt += float(words[i+2][1:])
						i += 2
					elif words[i] == '03:00 - 03:59' :   #shouldn't get these but roll into evening
						overflowc += float(words[i+1])
						overflowt += float(words[i+2][1:])
						i += 2
					elif words[i] == '04:00 - 04:59' :   #shouldn't get these but roll into evening
						overflowc += float(words[i+1])
						overflowt += float(words[i+2][1:])
						i += 2
					elif words[i] == '05:00 - 05:59' :   #shouldn't get these but roll into evening
						overflowc += float(words[i+1])
						overflowt += float(words[i+2][1:])
						i += 2		
					elif words[i] == '06:00 - 06:59' :   #shouldn't get these but roll into evening
						overflowc += float(words[i+1])
						overflowt += float(words[i+2][1:])
						i += 2
					elif words[i] == '07:00 - 07:59' :   #shouldn't get these but roll into evening
						overflowc += float(words[i+1])
						overflowt += float(words[i+2][1:])
						i += 2
					elif words[i] == '08:00 - 08:59' :   #shouldn't get these but roll into evening
						overflowc += float(words[i+1])
						overflowt += float(words[i+2][1:])
						i += 2		
					elif words[i] == '09:00 - 09:59' :   #shouldn't get these but roll into evening
						overflowc += float(words[i+1])
						overflowt += float(words[i+2][1:])
						i += 2
					elif words[i] == '10:00 - 10:59' :   #shouldn't get these but roll into evening
						overflowc += float(words[i+1])
						overflowt += float(words[i+2][1:])
						i += 2	
					elif words[i] == '11:00 - 11:59' :   #shouldn't get these but roll into evening
						overflowc += float(words[i+1])
						overflowt += float(words[i+2][1:])
						i += 2	
					elif words[i] == '12:00 - 12:59' :     #start lunchtime hours
						currentRow.append(float(words[i+1]))
						currentRow.append(float(words[i+2][1:]))
						i += 2
					elif words[i] == '13:00 - 13:59' :
						currentRow.append(float(words[i+1]))
						currentRow.append(float(words[i+2][1:]))
						i += 2
					elif words[i] == '14:00 - 14:59' :    #end of lunchtime hours
						currentRow.append(float(words[i+1]))
						currentRow.append(float(words[i+2][1:]))
						currentRow.append(currentRow[2] + currentRow[4] + currentRow[6])
						i += 2
					elif words[i] == '15:00 - 15:59' :   #shouldn't get these but roll into lunchtime
						currentRow[5] += float(words[i+1])
						currentRow[6] += float(words[i+2][1:])
						currentRow[7] += float(words[i+2][1:])
						i += 2
					elif words[i] == '16:00 - 16:59' :   #shouldn't get these but roll into lunchtime
						currentRow[5] += float(words[i+1])
						currentRow[6] += float(words[i+2][1:])
						currentRow[7] += float(words[i+2][1:])
						i += 1
					elif words[i] == '17:00 - 17:59' :   #start evening hours
						currentRow.append(float(words[i+1]))
						currentRow.append(float(words[i+2][1:]))
						i += 2
					elif words[i] == '18:00 - 18:59' :
						currentRow.append(float(words[i+1]))
						currentRow.append(float(words[i+2][1:]))
						i += 2
					elif words[i] == '19:00 - 19:59' :
						currentRow.append(float(words[i+1]))
						currentRow.append(float(words[i+2][1:]))
						i += 2
					elif words[i] == '20:00 - 20:59' :   #
						currentRow.append(float(words[i+1]))
						currentRow.append(float(words[i+2][1:]))
						i += 2
					elif words[i] == '21:00 - 21:59' :
						currentRow.append(float(words[i+1]))
						currentRow.append(float(words[i+2][1:]))
						i += 2
					elif words[i] == '22:00 - 22:59' :   #end evening hours
						currentRow.append(float(words[i+1]))
						currentRow.append(float(words[i+2][1:]))
						currentRow.append(currentRow[9] + currentRow[11] + currentRow[13] + currentRow[15] + currentRow[17] + currentRow[19] + overflowt)
						i += 2
					elif words[i] == '23:00 - 23:59' :   #shouldn't get these but roll into evening
						currentRow[18] += float(words[i+1])
						currentRow[19] += float(words[i+2][1:])
						currentRow[20] += float(words[i+2][1:])
						i += 2
		
					i += 1
		

				times.loc[len(times)] = currentRow
				

				
				
	


#save the header and data out to a file

times.to_csv(outputFile, index=False)

