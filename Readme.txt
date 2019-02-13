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