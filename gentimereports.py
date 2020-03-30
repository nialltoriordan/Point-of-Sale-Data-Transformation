# -*- coding: utf-8 -*-
"""
Program to extract and transform sales time data from a Point Of Sale terminal to .CSV format.

The program finds every file in startDir and it's subdirectories, opens any that begin with "TIME1",  
parses the text, adds it to a dataframe, then outputs the list to outputFile.

Note : transactions logged after lunchtime / evening hours are added to the previous valid hour if
possible, or else just printed to screen.

Potential errors caused by other files beginning with "TIME1" that are not in correct format.  

Similar to genfinreports I'm going to expand this to process the data and give daily numbers followed by the weekly total.
"""
#re is a text processing package
import re
import os
import pandas as pd

startDir = 'F:/backup/till/backup'
outputfile = 'dailytime.csv'
outputFile2 = 'dailytimerep.csv'


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
				overflowEve = 0
				overflowEvet = 0.0

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
				#not very efficient but short array to work through
				if ('DATE' in words) :
					cIndex = words.index('DATE')
					currentRow.append(words[cIndex + 1]) #add Date


					
				if ('00:00 - 00:59' in words) : #shouldn't get these so keep count
					cIndex = words.index('00:00 - 00:59')
					overflowEve += float(words[cIndex + 1])
					overflowEvet += float(words[cIndex + 2][1:]) #cut off euro symbol

				if ('01:00 - 01:59' in words) :
					cIndex = words.index('01:00 - 01:59')
					overflowEve += float(words[cIndex + 1])
					overflowEvet += float(words[cIndex + 2][1:])
					
				if ('02:00 - 02:59' in words) :
					cIndex = words.index('02:00 - 02:59')
					overflowEve += float(words[cIndex + 1])
					overflowEvet += float(words[cIndex + 2][1:])

				if ('03:00 - 03:59' in words) :
					cIndex = words.index('03:00 - 03:59')
					overflowEve += float(words[cIndex + 1])
					overflowEvet += float(words[cIndex + 2][1:])

				if ('04:00 - 04:59' in words) :
					cIndex = words.index('04:00 - 04:59')
					overflowEve += float(words[cIndex + 1])
					overflowEvet += float(words[cIndex + 2][1:])

				if ('05:00 - 05:59' in words) :
					cIndex = words.index('05:00 - 05:59')
					overflowEve += float(words[cIndex + 1])
					overflowEvet += float(words[cIndex + 2][1:])		

				if ('06:00 - 06:59' in words) : 
					cIndex = words.index('06:00 - 06:59')
					overflowEve += float(words[cIndex + 1])
					overflowEvet += float(words[cIndex + 2][1:])

				if ('07:00 - 07:59' in words) : 
					cIndex = words.index('07:00 - 07:59')
					overflowEve += float(words[cIndex + 1])
					overflowEvet += float(words[cIndex + 2][1:])
					
				if ('08:00 - 08:59' in words) : 
					cIndex = words.index('08:00 - 08:59')
					overflowEve += float(words[cIndex + 1])
					overflowEvet += float(words[cIndex + 2][1:])

				if ('09:00 - 09:59' in words) : 
					cIndex = words.index('09:00 - 09:59')
					overflowEve += float(words[cIndex + 1])
					overflowEvet += float(words[cIndex + 2][1:])		

				if ('10:00 - 10:59' in words) :
					cIndex = words.index('10:00 - 10:59')
					overflowEve += float(words[cIndex + 1])
					overflowEvet += float(words[cIndex + 2][1:])

				if ('11:00 - 11:59' in words) : 
					cIndex = words.index('11:00 - 11:59')
					overflowEve += float(words[cIndex + 1])
					overflowEvet += float(words[cIndex + 2][1:])


					
				if ('12:00 - 12:59' in words) :   #start lunchtime hours
					cIndex = words.index('12:00 - 12:59')
					currentRow.append(float(words[cIndex + 1]))
					currentRow.append(float(words[cIndex + 2][1:]))		
				else :
					currentRow.append(0)
					currentRow.append(0.0)		

				if ('13:00 - 13:59' in words) :   
					cIndex = words.index('13:00 - 13:59')
					currentRow.append(float(words[cIndex + 1]))
					currentRow.append(float(words[cIndex + 2][1:]))		
				else :
					currentRow.append(0)
					currentRow.append(0.0)		
					
				if ('14:00 - 14:59' in words) :   #end lunchtime hours
					cIndex = words.index('14:00 - 14:59')
					currentRow.append(float(words[cIndex + 1]))
					currentRow.append(float(words[cIndex + 2][1:]))		
				else :
					currentRow.append(0)
					currentRow.append(0.0)							

					
				currentRow.append(currentRow[2] + currentRow[4] + currentRow[6])   #produce 'lunchtime total'

				
				if ('15:00 - 15:59' in words) : #shouldn't get these but roll into lunchtime
					cIndex = words.index('15:00 - 15:59')
					currentRow[5] += float(words[cIndex+1])
					currentRow[6] += float(words[cIndex+2][1:])
					currentRow[7] += float(words[cIndex+2][1:])

				if ('16:00 - 16:59' in words) : #shouldn't get these but roll into lunchtime
					cIndex = words.index('16:00 - 16:59')
					currentRow[5] += float(words[cIndex+1])
					currentRow[6] += float(words[cIndex+2][1:])
					currentRow[7] += float(words[cIndex+2][1:])					


				if ('17:00 - 17:59' in words) :   #start eveing hours
					cIndex = words.index('17:00 - 17:59')
					currentRow.append(float(words[cIndex + 1]))
					currentRow.append(float(words[cIndex + 2][1:]))		
				else :
					currentRow.append(0)
					currentRow.append(0.0)		

				if ('18:00 - 18:59' in words) :   
					cIndex = words.index('18:00 - 18:59')
					currentRow.append(float(words[cIndex + 1]))
					currentRow.append(float(words[cIndex + 2][1:]))		
				else :
					currentRow.append(0)
					currentRow.append(0.0)		
					
				if ('19:00 - 19:59' in words) :   
					cIndex = words.index('19:00 - 19:59')
					currentRow.append(float(words[cIndex + 1]))
					currentRow.append(float(words[cIndex + 2][1:]))		
				else :
					currentRow.append(0)
					currentRow.append(0.0)	
					
				if ('20:00 - 20:59' in words) :   
					cIndex = words.index('20:00 - 20:59')
					currentRow.append(float(words[cIndex + 1]))
					currentRow.append(float(words[cIndex + 2][1:]))		
				else :
					currentRow.append(0)
					currentRow.append(0.0)		

				if ('21:00 - 21:59' in words) :   
					cIndex = words.index('21:00 - 21:59')
					currentRow.append(float(words[cIndex + 1]))
					currentRow.append(float(words[cIndex + 2][1:]))		
				else :
					currentRow.append(0)
					currentRow.append(0.0)	
					
				if ('22:00 - 22:59' in words) :   #end evening hours
					cIndex = words.index('22:00 - 22:59')
					currentRow.append(float(words[cIndex + 1]))
					currentRow.append(float(words[cIndex + 2][1:]))		
				else :
					currentRow.append(0)
					currentRow.append(0.0)							
					
	
				currentRow.append(currentRow[9] + currentRow[11] + currentRow[13] + currentRow[15] + currentRow[17] + currentRow[19])  #produce 'evening total'
	

				if ('23:00 - 23:59' in words) : #shouldn't get this but roll into evening
					cIndex = words.index('23:00 - 23:59')
					currentRow[18] += float(words[cIndex+1])
					currentRow[19] += float(words[cIndex+2][1:])
					currentRow[20] += float(words[cIndex+2][1:])		

					
				if(overflowEve > 0) :  
					if times.empty:  #if no previous row, just print
						print ('Overflow found on', currentRow[0], '. Sales Count : ', overflowEve, '.  Sales Value : ', overflowEvet)		
					else :    #else, add to previous row.
						lastrow = times.index[-1]
						times.at[lastrow, '22:00 : 22:59 C'] += overflowEve
						times.at[lastrow, '22:00 : 22:59 T'] += overflowEvet
						times.at[lastrow, 'Total Evening'] += overflowEvet

				times.loc[len(times)] = currentRow
				

				
				
	


#save the header and data out to a file

times.to_csv(outputfile, index=False)




time_data = pd.read_csv(outputfile, header=0, index_col=False) 
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

