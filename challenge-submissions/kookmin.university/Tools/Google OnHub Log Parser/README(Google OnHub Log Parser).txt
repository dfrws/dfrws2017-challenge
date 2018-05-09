***********************Google OnHub Log Parser***********************
OnHub Diagnostic Report analysis tool
- input	 : [diagnostic report name].json (output of the 'onhubdump' from Github)
- output : Exporting the data for connected/disconnected devices in CSV format

[Source Code Building Instructions]
Program needed to build source code: 
- Python 2.x 32 or 64bit (Implemented environment : Python 2.7.14 32bit)
- IDE (ex. Visual Studio, PyCharm...)

[How To Use]
1. Convert your diagnostic report to the JSON file format using onhubdump.
 - Source code of onhubdump and installation method is specified in Github (https://github.com/benmanns/onhub/tree/master/cmd/onhubdump).
 - Command format example:
	onhubdump.exe	[raw diagnostic-report path] > [output file name you choose].json

2. Type the following command on your command prompt (cmd.exe).
 - python OnhubParser.py [JSON file path] [output file (csv) name]

3. Then you can get the result file ([output file name].csv)