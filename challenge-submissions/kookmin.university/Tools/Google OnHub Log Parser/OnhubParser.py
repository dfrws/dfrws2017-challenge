# -*- coding: utf-8 -*-

__author__ = "DF&C"

import sys
import os
import json
import csv
import time

class ParseOnhub:
	# filename : onhubdump 도구로 파싱한 json 파일
	def __init__(self, filename, tag):
		self.fn = open(filename)
		self.tg = tag
		self.result = open(tag + '.csv', 'wb')

	def __del__(self):
		self.fn.close()
		self.result.close()

	def getCurrentTime(self):
		now = time.localtime()
		return "{0}-{1}-{2} {3}:{4}:{5}".format(str(now.tm_year), str(now.tm_mon).zfill(2), str(now.tm_mday).zfill(2), str(now.tm_hour).zfill(2), str(now.tm_min).zfill(2), str(now.tm_sec).zfill(2))

	# list = [stations, results]
	def exportCSV(self, list):
		writer = csv.writer(self.result)
		writer.writerow(["Onhub" + "(" + self.tg + ")" + "-" + self.getCurrentTime(), "UTC+" + str(list[1][1][1])])
		writer.writerow(["MAC", "IP", "dhcphostname", "mdnsname"])
		for tup in list[0]:
			writer.writerow(["=\""+ tup[0] +"\"", tup[1], tup[2], tup[3]])
		writer.writerow("")
		writer.writerow(["Time", "MAC", "State"])
		for tup in list[1]:
			writer.writerow(["=\""+ tup[0] +"\"", "=\""+ tup[2] +"\"", tup[3]])

	def parseDevcieList(self, station, wanInfo):
		ret = []       # (mac, ip, hostname)

		while (station and wanInfo):
			mac = station[0][0]
			dhcp = station[0][1]
			mdns = station[0][2]
			for i in range(0, len(wanInfo)):
				tup = wanInfo[i]
				if tup[0].find(mac) != -1:
					ret.append((tup[0], tup[1], dhcp, mdns))
					del wanInfo[i]
					del station[0]
					break
				else:
					pass

		return ret

	# string : log 리스트
	def parseKeyword(self, string):
		ret = []
		arr = string.split("\n")
		for line in arr:
			if not line:
				break
			else:
				c_ofs = line.find("Connected")
				dc_ofs = line.find("Disconnected")
				if (c_ofs != -1) or (dc_ofs != -1):
					arr = line.split(" ")

					# 시간 분석
					time = arr[0].split("+")
					utc = time[1]
					time = (time[0].replace("T", " ").split("."))[0]
					ret.append((time, utc, arr[5], arr[-1]))
				else:
					pass

		return ret

	def parseJson(self):
		st = []       # station
		wan = []
		st_wan = []
		log = []      # result
		with open("report.json") as f:
			data = f.read(os.path.getsize("report.json")).decode("utf-16")
		# json 디코딩
		dict = json.loads(data)

		# 1-1. 연결되었던 기기 목록 가져오기(MAC, Hostname)
		station = dict["infoJSON"]["_apState"]["_stations"]
		for dic in station:
			l_mdns = dic['_mdnsNames']
			if len(l_mdns) != 0:
				mdns = l_mdns[0]
			else:
				mdns = ""
			st.append((dic['_oui'], dic['_dhcpHostname'], mdns))

		# 1-2. 연결되었던 기기 목록 가져오기(MAC, IP)
		wanInfo = dict["wanInfo"]
		arr = wanInfo.split("\n")
		i = 0
		while True:
			line = arr[i]
			if line.find("mac_address") != -1:
				index = line.find("\"")
				mac = line[index+1:-1]

				line = arr[i+1]     # "ip_address"
				index = line.find("\"")
				ip = line[index+1:-1]
				wan.append((mac,ip))
				i += 3
			elif i == len(arr) - 1:
				break
			else:
				i += 1

		# 1-3. (MAC, IP, Hostname)
		st_wan = self.parseDevcieList(st, wan)

		# 2. log 분석
		files = dict["files"]
		for i in range(0, len(files)):
			dic = files[i]
			path = dic["path"]
			if (path.find("/log/messages") != -1) and ("content" in dic):
				log.append(dic["content"])
			else:
				pass
		log.reverse()
		logs = "".join(log)
		log = self.parseKeyword(logs)

		# csv 출력
		self.exportCSV([st_wan, log])

def main(*args):
	try:
		fn = sys.argv[1]
		tag = sys.argv[2]
		ParseOnhub(fn, tag).parseJson()
	except:
		print "usage:"
		print "\t" + "python Parse_Onhub.py [json File Name] [Tag]"

if __name__ == '__main__':
	main()