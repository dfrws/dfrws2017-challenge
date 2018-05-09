# -*- coding: utf-8 -*-

__author__ = "DF&C"

import datetime
import os
import sys

Time = "creationTimestamp"
Context = '"summary"'


def unixTimeConvert(utime):
	return datetime.datetime.fromtimestamp(int(utime[0:10])).strftime('%Y-%m-%d %H:%M:%S')

def CSVsave(filename, time, contents,Endfile):
	f = open(Endfile,"a")
	f.write(time + "," + filename + "," + contents)
	f.write("\n")
	f.close()

class JsonToText:
	def FileBased(self, filename, basename, endfile):
		with open(filename) as f:
			data = f.read()
			size = len(data)
			UnixTimeStamp = "None"
			Contents = "None"
			for i in range(0, len(data)):
				try:
					if (Time == data[i:i + 17]):
						UnixTimeStamp = data[i + 19:i + 32]
						UnixTimeStamp = unixTimeConvert(UnixTimeStamp)
						break
				except:
					UnixTimeStamp = 0
			for i in range(0, len(data)):
				if (Context == data[i:i + 9]):
					for j in range(0, len(data)):
						try:
							if (data[i + 11 + j] == '"'):
								Contents = data[i + 11:i + 11 + j]
								break
						except:
							Contents = None
				elif (Contents != "None"):
					break

			CSVsave(basename, "=\""+ UnixTimeStamp +"\"", Contents, endfile)

	def DirectoryBased(self, path, endfile):
		for (path, dir, files) in os.walk(path):
			for filename in files:
				ext = os.path.splitext(filename)[-1]
				basename = os.path.basename(filename)
				if ext == '.json':
					filename = path+"\\"+filename
					parse = JsonToText()
					parse.FileBased(filename, basename, endfile)


def main(*args):
	localtime = datetime.datetime.now()
	utctime = datetime.datetime.utcnow()
	UTC = localtime - utctime
	UTC = str(UTC)

	if UTC[0:2] == "-1":
		value = "-"
	else:
		value = "+"

	inputname = sys.argv[1]

	localtime = str(localtime)
	localtime = localtime[0:-7]
	endfile = "JasonToCsv(%s)-%s.csv"%(inputname,localtime[0:10])

	f = open(endfile, "w")
	f.write("Amazon Echo(%s)-%s,UTC%s%s\n" % (inputname, localtime, value, UTC[-8:-3].zfill(5)))
	f.write("Time,Filename,Content\n")
	f.close()

	try:
		filename = sys.argv[2]
		if filename[-5:] == ".json":
			FileParse = JsonToText()
			FileParse.FileBased(filename, endfile)
		else:
			path = filename
			DirParse = JsonToText()
			DirParse.DirectoryBased(path, endfile)
	except:
		path = os.path.dirname(os.path.realpath(__file__))
		DirParse = JsonToText()
		DirParse.DirectoryBased(path, endfile)

if __name__ == '__main__':
	main()