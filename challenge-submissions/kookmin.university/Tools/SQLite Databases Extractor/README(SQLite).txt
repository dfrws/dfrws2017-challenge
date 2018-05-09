***********************SQLite Databases Extractor***********************
Database extract tool from the EXT4-based device image
- input  : EXT4-based device image file(s)
- output : CSV, DB file(s)

[Source Code Building Instructions]
1. Install Anaconda 2.7
- Installation Type : Install for All Users 
- Advanced Options 
  Add Anaconda to my PATH environment variable
  Register Anaconda as my default Python 2.7
- Install Microsoft VScode

2. Execute VScode
- Install python in MarketPlace

3. Enter the following commands in terminal
pip install tabulate
pip install datetime

4. Now you can compile the main code; '_DB_View.py'

[How To Use]
1. If the image is splitted in to many files, it needs to be merged.
   Using 'File - File-Merge' option.
2. Open the merged file or single file with 'File - Open File'.
3. Extract databases with 'Make_File' toggle button.
   Display database contents with 'DB_VIEW' toggle button.
4. You can also get the result file in CSV format.