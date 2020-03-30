UPDATE :

I've updated some files since initially uploading this project.  This is pretty much a final version for the 
'data transformation' project; it's likely what the data is used for will be uploaded as seperate projects
 (e.g. : Sales by Time Project data visualisation).

I'm uploading three files :

genfinreports.py
gentimereports.py
genplureports.py

All assume you have one week's worth of data in the working directory or subdirectories thereof.  An 'x' report 
is generated Monday to Saturday and accumulates data for the week, so the Thursday financial report for example 
contains financial data for Monday, Tuesday, Wednesday, and Thursday combined.  A 'z' report is generated on 
Sunday giving the total for the week and resetting the counts.

The programs read .txt report files from subdirectories and generate two CSV files :

dailyfin.csv (or similar) is the relevant data from the seven text files in CSV form.

dailyfinrep.csv (or similar) provides daily numbers by subtracting previous days from the current, 
with the week's total in the 8th row.



processfin :

Program to extract and transform sales data from a Point Of Sale terminal to .CSV format.

The program finds every file in startDir and it's subdirectories, opens any that begin with "FIN1",  
parses the text, adds it to a list of strings, then outputs the list to outputFile.


processtime :

Program to extract and transform sales time data from a Point Of Sale terminal to .CSV format.

The program finds every file in startDir and it's subdirectories, opens any that begin with "TIME1", 
parses the text, adds it to a dataframe, then outputs the list to outputFile.

Note : transactions logged after lunchtime / evening hours are added to the previous valid hour.


processplu :

Program to extract and transform PLU sales data from a Point Of Sale terminal to .CSV format.

The program finds every file in startDir and it's subdirectories, opens any that begin with "PLU1",  
parses the text, adds it to a list of strings, checks for errors, then outputs the list to outputFile.

Future work :
Read in PLU descriptions and prices from a .CSV file.  Build in support for changing prices depending
on date.