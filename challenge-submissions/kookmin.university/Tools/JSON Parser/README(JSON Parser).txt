***********************JSON Parser***********************
Extracting specific variables (creationTimestamp, summary) from the scenario's JSON file
- input  : JSON file name or folder
- output : CSV file

[Source Code Building Instructions]
Program needed to build source code: 
- Python 2.x 32 or 64bit (Implemented environment : Python 2.7.14 32bit)
- IDE (ex. Visual Studio, PyCharm...)

[How To Use (Command Line Based)]
1. Type the following command on your command prompt (cmd.exe)
 - python JsonToCsv.py [arg1] [arg2]
 - arg1 is the value to select the desired filename. 
   The output filename format is 'Amazon Echo(arg1)-localtime.csv'.
 - You can put the filename or folder name in the arg2 value. 
   If you enter a file name, it analyzes one file. 
   If you put a folder name, it analyzes all the files in the folder.

2. Then you can get the result file (Amazon Echo(arg1)-localtime.csv)