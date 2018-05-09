# -*- coding: utf-8 -*-

__author__ = "DF&C"

from PyQt4 import QtCore, QtGui
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import csv
import numpy as np
import os
from datetime import timedelta, datetime

out_data = {
	"onhub_connect": "", \
	"onhub_disconnect": "", \
	"Database": "", \
	"amazon_echo": ""}

utc_timezone_dic = {}
Date = {"year": "", "month": "", "day": ""}

device_list = []
time_list = []
onhub_connect_annot = {}
onhub_disconnect_annot = {}
Database_annot={}
echo_annot = {}

utc_timezone = 0

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtGui.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName(_fromUtf8("MainWindow"))
		MainWindow.resize(1150, 655)
		MainWindow.setMinimumSize(QtCore.QSize(1500, 250))
		self.centralwidget = QtGui.QWidget(MainWindow)
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
		self.gridLayout = QtGui.QGridLayout(self.centralwidget)
		self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
		self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
		self.pushButton_2.setMinimumSize(QtCore.QSize(0, 30))
		self.pushButton_2.setMaximumSize(QtCore.QSize(70, 16777215))
		font = QtGui.QFont()
		font.setBold(True)
		font.setWeight(75)
		self.pushButton_2.setFont(font)
		self.pushButton_2.setLayoutDirection(QtCore.Qt.RightToLeft)
		self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
		self.pushButton_2.clicked.connect(self.zoom)  ########### zoom 함수 연결
		self.gridLayout.addWidget(self.pushButton_2, 2, 1, 1, 1)
		self.pushButton = QtGui.QPushButton(self.centralwidget)
		self.pushButton.setMinimumSize(QtCore.QSize(0, 30))
		self.pushButton.setMaximumSize(QtCore.QSize(70, 16777215))
		font = QtGui.QFont()
		font.setBold(True)
		font.setWeight(75)
		self.pushButton.setFont(font)
		self.pushButton.setLayoutDirection(QtCore.Qt.RightToLeft)
		self.pushButton.setObjectName(_fromUtf8("pushButton"))
		self.pushButton.clicked.connect(self.pan)  ###########pan 함수 연결
		self.gridLayout.addWidget(self.pushButton, 2, 2, 1, 1)
		self.pushButton_3 = QtGui.QPushButton(self.centralwidget)
		self.pushButton_3.setMinimumSize(QtCore.QSize(0, 30))
		self.pushButton_3.setMaximumSize(QtCore.QSize(70, 16777215))
		font = QtGui.QFont()
		font.setBold(True)
		font.setWeight(75)
		self.pushButton_3.setFont(font)
		self.pushButton_3.setLayoutDirection(QtCore.Qt.RightToLeft)
		self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
		self.pushButton_3.clicked.connect(self.home)  ##########home 함수 연결
		self.gridLayout.addWidget(self.pushButton_3, 2, 3, 1, 1)
		self.frame_4 = QtGui.QFrame(self.centralwidget)
		self.frame_4.setMinimumSize(QtCore.QSize(150, 0))
		self.frame_4.setMaximumSize(QtCore.QSize(16777215, 40))
		self.frame_4.setFrameShape(QtGui.QFrame.StyledPanel)
		self.frame_4.setFrameShadow(QtGui.QFrame.Plain)
		self.frame_4.setLineWidth(1)
		self.frame_4.setObjectName(_fromUtf8("frame_4"))
		self.horizontalLayout = QtGui.QHBoxLayout(self.frame_4)
		self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
		self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
		self.label = QtGui.QLabel(self.frame_4)
		self.label.setMinimumSize(QtCore.QSize(0, 35))
		self.label.setMaximumSize(QtCore.QSize(40, 30))
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setBold(True)
		font.setWeight(75)
		self.label.setFont(font)
		self.label.setAlignment(QtCore.Qt.AlignCenter)
		self.label.setObjectName(_fromUtf8("label"))
		self.horizontalLayout.addWidget(self.label)
		self.dateEdit = QtGui.QDateEdit(self.frame_4)
		self.dateEdit.setMinimumSize(QtCore.QSize(0, 30))
		self.dateEdit.setMaximumSize(QtCore.QSize(121, 20))
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setBold(True)
		font.setWeight(75)
		self.dateEdit.setFont(font)
		self.dateEdit.setAlignment(QtCore.Qt.AlignCenter)
		self.dateEdit.setObjectName(_fromUtf8("dateEdit"))
		self.dateEdit.setDateTime(QtCore.QDateTime.currentDateTime())  ########## 현재 날짜로 업데이트
		self.dateEdit.setCalendarPopup(True)  ########## 캘린더 팝업
		self.dateEdit.dateChanged.connect(self.ShowDate)  ########## 선택한 날짜로 데이터 업데이트
		self.horizontalLayout.addWidget(self.dateEdit)
		self.label_2 = QtGui.QLabel(self.frame_4)
		self.label_2.setMinimumSize(QtCore.QSize(0, 35))
		self.label_2.setMaximumSize(QtCore.QSize(81, 30))
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setBold(True)
		font.setWeight(75)
		self.label_2.setFont(font)
		self.label_2.setAlignment(QtCore.Qt.AlignCenter)
		self.label_2.setObjectName(_fromUtf8("label_2"))
		self.horizontalLayout.addWidget(self.label_2)
		self.textEdit = QtGui.QTextEdit(self.frame_4)
		self.textEdit.setMinimumSize(QtCore.QSize(600, 30))
		self.textEdit.setMaximumSize(QtCore.QSize(16777215, 20))
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setBold(True)
		font.setWeight(75)
		self.textEdit.setFont(font)
		self.textEdit.setFrameShape(QtGui.QFrame.StyledPanel)
		self.textEdit.setObjectName(_fromUtf8("textEdit"))
		self.horizontalLayout.addWidget(self.textEdit)
		self.comboBox = QtGui.QComboBox(self.frame_4)
		self.comboBox.setMinimumSize(QtCore.QSize(0, 30))
		self.comboBox.setMaximumSize(QtCore.QSize(16777215, 20))
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setBold(True)
		font.setWeight(75)
		self.comboBox.setFont(font)
		self.comboBox.setObjectName(_fromUtf8("comboBox"))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.activated.connect(self.convert_utc)
		self.horizontalLayout.addWidget(self.comboBox)
		self.gridLayout.addWidget(self.frame_4, 0, 0, 1, 4)
		self.verticalLayout = QtGui.QVBoxLayout()
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
		self.fig = plt.figure()  ########## figure 만들기
		self.canvas = FigureCanvas(self.fig)  ########## canvas 만들기
		self.verticalLayout.addWidget(self.canvas)  ########## figure 삽입
		self.toolbar = NavigationToolbar(self.canvas, MainWindow)  ##########툴바 생성
		self.toolbar.hide()  ##########툴바 숨김
		self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 4)
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtGui.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 1150, 21))
		self.menubar.setObjectName(_fromUtf8("menubar"))
		self.menuOpen = QtGui.QMenu(self.menubar)
		self.menuOpen.setObjectName(_fromUtf8("menuOpen"))
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtGui.QStatusBar(MainWindow)
		self.statusbar.setObjectName(_fromUtf8("statusbar"))
		MainWindow.setStatusBar(self.statusbar)
		self.actionFile = QtGui.QAction(MainWindow)
		self.actionFile.setObjectName(_fromUtf8("actionFile"))
		self.actionFile.triggered.connect(self.OpenFile)  ########## OpenFile 연결
		self.actionDirectory = QtGui.QAction(MainWindow)
		self.actionDirectory.setObjectName(_fromUtf8("actionDirectory"))
		self.actionDirectory.triggered.connect(self.OpenDirectory)  ########## OpenDirectory 연결
		self.menuOpen.addAction(self.actionFile)
		self.menuOpen.addAction(self.actionDirectory)
		self.menubar.addAction(self.menuOpen.menuAction())

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
		self.pushButton_2.setText(_translate("MainWindow", "ZOOM", None))
		self.pushButton.setText(_translate("MainWindow", "PAN", None))
		self.pushButton_3.setText(_translate("MainWindow", "HOME", None))
		self.label.setText(_translate("MainWindow", "Date", None))
		self.label_2.setText(_translate("MainWindow", "Duration", None))
		self.comboBox.setCurrentIndex(14)
		self.comboBox.setItemText(0, _translate("MainWindow", "UTC -12:00", None))
		self.comboBox.setItemText(1, _translate("MainWindow", "UTC -11:00", None))
		self.comboBox.setItemText(2, _translate("MainWindow", "UTC -10:00", None))
		self.comboBox.setItemText(3, _translate("MainWindow", "UTC -09:30", None))
		self.comboBox.setItemText(4, _translate("MainWindow", "UTC -09:00", None))
		self.comboBox.setItemText(5, _translate("MainWindow", "UTC -08:00", None))
		self.comboBox.setItemText(6, _translate("MainWindow", "UTC -07:00", None))
		self.comboBox.setItemText(7, _translate("MainWindow", "UTC -06:00", None))
		self.comboBox.setItemText(8, _translate("MainWindow", "UTC -05:00", None))
		self.comboBox.setItemText(9, _translate("MainWindow", "UTC -04:00", None))
		self.comboBox.setItemText(10, _translate("MainWindow", "UTC -03:30", None))
		self.comboBox.setItemText(11, _translate("MainWindow", "UTC -03:00", None))
		self.comboBox.setItemText(12, _translate("MainWindow", "UTC -02:00", None))
		self.comboBox.setItemText(13, _translate("MainWindow", "UTC -01:00", None))
		self.comboBox.setItemText(14, _translate("MainWindow", "UTC +00:00", None))
		self.comboBox.setItemText(15, _translate("MainWindow", "UTC +01:00", None))
		self.comboBox.setItemText(16, _translate("MainWindow", "UTC +02:00", None))
		self.comboBox.setItemText(17, _translate("MainWindow", "UTC +03:00", None))
		self.comboBox.setItemText(18, _translate("MainWindow", "UTC +03:30", None))
		self.comboBox.setItemText(19, _translate("MainWindow", "UTC +04:00", None))
		self.comboBox.setItemText(20, _translate("MainWindow", "UTC +04:30", None))
		self.comboBox.setItemText(21, _translate("MainWindow", "UTC +05:00", None))
		self.comboBox.setItemText(22, _translate("MainWindow", "UTC +05:30", None))
		self.comboBox.setItemText(23, _translate("MainWindow", "UTC +05:45", None))
		self.comboBox.setItemText(24, _translate("MainWindow", "UTC +06:00", None))
		self.comboBox.setItemText(25, _translate("MainWindow", "UTC +06:30", None))
		self.comboBox.setItemText(26, _translate("MainWindow", "UTC +07:00", None))
		self.comboBox.setItemText(27, _translate("MainWindow", "UTC +08:00", None))
		self.comboBox.setItemText(28, _translate("MainWindow", "UTC +08:30", None))
		self.comboBox.setItemText(29, _translate("MainWindow", "UTC +08:45", None))
		self.comboBox.setItemText(30, _translate("MainWindow", "UTC +09:00", None))
		self.comboBox.setItemText(31, _translate("MainWindow", "UTC +09:30", None))
		self.comboBox.setItemText(32, _translate("MainWindow", "UTC +10:00", None))
		self.comboBox.setItemText(33, _translate("MainWindow", "UTC +10:30", None))
		self.comboBox.setItemText(34, _translate("MainWindow", "UTC +11:00", None))
		self.comboBox.setItemText(35, _translate("MainWindow", "UTC +12:00", None))
		self.comboBox.setItemText(36, _translate("MainWindow", "UTC +12:45", None))
		self.comboBox.setItemText(37, _translate("MainWindow", "UTC +13:00", None))
		self.comboBox.setItemText(38, _translate("MainWindow", "UTC +14:00", None))
		self.menuOpen.setTitle(_translate("MainWindow", "Open", None))
		self.actionFile.setText(_translate("MainWindow", "File", None))
		self.actionDirectory.setText(_translate("MainWindow", "Directory", None))

	def convert_utc(self):
		global utc_timezone
		temp = self.comboBox.currentText().split(" ")[1]
		if temp[0] == '-':
			utc_timezone = float(temp[0:3])-float(temp[4:6])/60
		else:
			utc_timezone = float(temp[0:3]) + float(temp[4:6]) / 60

		if time_list is not None:
			int_time_list = []
			del int_time_list[:]
			for i in time_list:
				convert_time = self.convert_utc_timezone(i,utc_timezone)
				if convert_time.find('-') >= 0:
					temp = convert_time.split('-')[0] + convert_time.split('-')[1] + convert_time.split('-')[2]
					int_time_list.append(temp)

			min_time = min(int_time_list)[0:4] + '/' + min(int_time_list)[4:6] + '/' + min(int_time_list)[6:8]
			max_time = max(int_time_list)[0:4] + '/' + max(int_time_list)[4:6] + '/' + max(int_time_list)[6:8]
			self.textEdit.setText(min_time + ' ~ ' + max_time)  ###duration 설정
		else:
			pass

		self.View()

	def convert_utc_timezone(self, get_time, gap):
		get_time = get_time.replace("-"," ")
		get_time = get_time.replace(":"," ")
		temp = datetime(int(get_time.split(' ')[0]), int(get_time.split(' ')[1]), int(get_time.split(' ')[2]), int(get_time.split(' ')[3]), int(get_time.split(' ')[4]), int(get_time.split(' ')[5]), 0)
		convert_time = temp + timedelta(hours=gap)

		return str(convert_time)

	def zoom(self):
		self.toolbar.zoom()

	def pan(self):
		self.toolbar.pan()

	def home(self):
		self.toolbar.home()

	def ShowDate(self):
		date = self.dateEdit.date()
		string_date = str(date.toPyDate())
		Date["year"] = string_date.split('-')[0]
		Date["month"] = string_date.split('-')[1]
		Date["day"] = string_date.split('-')[2]

		self.View()

	def OpenFile(self):
		find=['Onhub', 'Database', 'Amazon Echo']
		file_list = []
		del file_list[:] #리스트 초기화
		del device_list[:]
		device_list.append('') # y축 한 줄 띄려고 추가

		reload(sys)
		sys.setdefaultencoding('utf-8')

		FilePath = QtGui.QFileDialog.getOpenFileName()

		if FilePath:
			if FilePath[-4:] == '.csv':  # 확장자로 csv 파일만 필터링
				f = open(FilePath, 'r')
				first = f.readline().split(',')[0].split('-')[0]

				if first.split('(')[0] in find:  # 분석 대상 파일 필터링
					file_list.append(FilePath)
					device_list.append(first)
				f.close()

			self.Analyze_Data(file_list)
		else:
			pass

		self.init_view()

	def OpenDirectory(self):
		reload(sys)
		sys.setdefaultencoding('utf-8')

		DirPath = str(QtGui.QFileDialog.getExistingDirectory())

		if DirPath:
			self.Directory_Search(DirPath)
		else:
			pass

		self.init_view()

	def Directory_Search(self,DirPath):
		find=['Onhub', 'Database', 'Amazon Echo']
		file_list = []
		del file_list[:] #리스트 초기화
		del device_list[:]

		device_list.append('') # y축 한 줄 띄려고 추가
		for (path, dir, files) in os.walk(unicode(DirPath)): #unicode(DirPath): 한글 경로 가능하게
			for filename in files:
				if filename[-4:] == '.csv': #확장자로 csv 파일만 필터링
					f = open(os.path.join(path,filename),'r')
					first = f.readline()
					if first[0:5] == 'Onhub': #분석 대상 파일 필터링
						file_list.append(os.path.join(path, filename))
						device_list.append(first.split(',')[0].split('-')[0])
					elif first[0:8] == 'Database':
						file_list.append(os.path.join(path, filename))
						device_list.append(first.split('_')[0] + '('+first.split('(')[1].split('-')[0])
					elif first[0:11] == 'Amazon Echo':
						file_list.append(os.path.join(path, filename))
						device_list.append(first.split(',')[0].split('-')[0])
					f.close()

		self.Analyze_Data(file_list)

	def Analyze_Data(self,file_list):
		empty_list = []
		out_data["onhub_disconnect"] = empty_list
		out_data["onhub_connect"] = empty_list
		out_data["amazon_echo"] = empty_list
		out_data["Database"] = empty_list
		in_data = {} #기기별 모든 데이터가 포함되어 있는 딕셔너리
		del time_list[:]
		index = 1
		for i in range(1,len(device_list)):
			data = self.Read_Data(file_list[i-1],time_list,index) #모든 데이터
			if in_data is None:
				in_data[device_list[i]] = data
			else:
				if device_list[i] in in_data:
					in_data[device_list[i]] = data
				else:
					in_data[device_list[i]]=data
			index += 1

		int_time_list=[]
		del int_time_list[:]
		for i in time_list:
			if i.find('-')>=0:
				temp = i.split('-')[0]+i.split('-')[1]+i.split('-')[2]
				int_time_list.append(temp)

		min_time = min(int_time_list)[0:4]+'/'+min(int_time_list)[4:6]+'/'+min(int_time_list)[6:8]
		max_time = max(int_time_list)[0:4]+'/'+max(int_time_list)[4:6]+'/'+max(int_time_list)[6:8]
		self.textEdit.setText(min_time+' ~ '+max_time) ###duration 설정

		connect = []
		disconnect = []
		database = []
		echo=[]

		for key in in_data:
			if key[0:5] == 'Onhub':
				temp1 = in_data[key] #temp1은 각 기기별 데이터 리스트들
				for temp2 in temp1: #temp2는 temp1의 리스트 하나
					if temp2[2] =='Connected':
						connect.append(temp2[0]+' '+temp2[1]+' '+temp2[3]+ ' ' +temp2[4])
					elif temp2[2] =='Disconnected':
						disconnect.append(temp2[0] + ' ' + temp2[1]+' '+temp2[3]+' ' +temp2[4])
					else:
						continue
				out_data["onhub_connect"] = connect
				out_data["onhub_disconnect"] = disconnect
			elif key[0:11] == 'Amazon Echo':
				temp1 = in_data[key]  # temp1은 각 기기별 데이터 리스트들
				for temp2 in temp1:  # temp2는 temp1의 리스트 하나
					echo.append(temp2)
				out_data["amazon_echo"] = echo
			elif key[0:8] == 'Database':
				temp1 = in_data[key]  # temp1은 각 기기별 데이터 리스트들
				for temp2 in temp1:  # temp2는 temp1의 리스트 하나
					database.append(temp2)
				out_data["Database"]=database

		###View 함수로 이동

	def Read_Data(self,Filepath, time_list,index):
		global utc_timezone

		f = open(Filepath,'r')

		data_a = csv.reader(f)
		count = 0
		list = []
		device_name=0

		for data in data_a:
			if not data:
				pass
			else:
				if count == 0:
					if data[0][0:5] == 'Onhub':
						device_name = data[0].split('-')[0]
					elif data[0][0:11] == 'Amazon Echo':
						device_name = data[0].split('-')[0]
					elif data[0][0:8] == 'Database':
						device_name = data[0].split('_')[0] + '(' + data[0].split('(')[1].split('-')[0]
					temp=QtCore.QString(data[1].split("UTC")[1])
					if temp[0] == '-':
						utc_timezone_temp = float(temp[0:3])-float(temp[4:6])/60
					else:
						utc_timezone_temp =  float(temp[0:3])+float(temp[4:6])/60
					utc_timezone_dic[device_name]=utc_timezone_temp
					count = 1
				elif data[0].find('Time')>=0:
					count = 2
				elif count == 2:
					if data[0] == '="None"':
						pass
					else:
						data.append(device_name)  # 기기정보 추가(날짜, 맥주소, 연결/연결해제, 기기정보)
						data.append(str(index))
						list.append(data)
						if utc_timezone_dic[device_name] == utc_timezone:
							time_list.append(data[0].split('"')[1].split('"')[0])  # time_list는 시간정보
						else:
							time_temp = data[0].split('"')[1].split('"')[0]
							time_temp = self.convert_utc_timezone(time_temp,utc_timezone-utc_timezone_dic[device_name])
							time_list.append(time_temp)  # time_list는 시간정보
		f.close()
		return list

	def init_view(self):
		plt.clf()
		plt.ylim(0, len(device_list))  # y축 최소,최대값 설정
		plt.yticks(np.arange(0, len(device_list)), device_list)  # y축 눈금
		plt.xlim(0, 24)  # x축 최소,최대값 설정
		plt.xticks(np.arange(0, 25))  # x축 눈금
		plt.xlabel('time(hours)')
		plt.ylabel('devices')
		plt.title('Result')

	def View(self):
		self.init_view()
		global utc_timezone
		sc_onhub_connect = []
		del sc_onhub_connect[:]
		sc_onhub_connect_index= []
		del sc_onhub_connect_index[:]
		sc_onhub_disconnect= []
		del sc_onhub_disconnect[:]
		sc_onhub_disconnect_index= []
		del sc_onhub_disconnect_index[:]
		onhub_disconnect_annot.clear
		onhub_connect_annot.clear
		sc_Database= []
		del sc_Database[:]
		sc_Database_index= []
		del sc_Database_index[:]
		Database_annot.clear
		sc_amazon_echo= []
		del sc_amazon_echo[:]
		sc_amazon_echo_index = []
		del sc_amazon_echo_index[:]
		echo_annot.clear

		if (out_data["onhub_connect"] is '') & (out_data["onhub_disconnect"] is '') & (out_data["Database"] is '') & (out_data["amazon_echo"] is ''):
			self.canvas.draw()
			self.clear_view()
		else:
			self.annot = plt.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points", bbox=dict(boxstyle="round", fc="w"), arrowprops=dict(arrowstyle="->"))
			if out_data["onhub_connect"]:
				sc_onhub_connect_temp = out_data["onhub_connect"]
				if utc_timezone_dic[sc_onhub_connect_temp[0].split(' ')[3]] == utc_timezone:
					for i in range(len(sc_onhub_connect_temp)):
						time = sc_onhub_connect_temp[i].split(' ')[0].split('"')[1]
						if (Date["year"] == time.split('-')[0]) & (Date["month"] == time.split('-')[1]) & (Date["day"] == time.split('-')[2]) :
							time2 = sc_onhub_connect_temp[i].split(' ')[1].split('"')[0]
							add_data = float(time2.split(":")[0]) + (float(time2.split(":")[1]) / 60) + ((float(time2.split(":")[2]) / 60) / 60)  # X축 시간 계산  ##########split 데이터 수정
							sc_onhub_connect.append(round(add_data,4))
							index = sc_onhub_connect_temp[i].split(' ')[4]
							onhub_connect_annot[round(add_data,4)]=index+'|'+'MAC address : '+ sc_onhub_connect_temp[i].split(' ')[2].split('"')[1].split('"')[0] +'\n'+'time : '+ sc_onhub_connect_temp[i].split(' ')[0].split('"')[1] + ' '+sc_onhub_connect_temp[i].split(' ')[1].split('"')[0]+'\n'+'Action: Connected'
							sc_onhub_connect_index.append(int(index))
						else:
							continue
				else:
					gap = utc_timezone - utc_timezone_dic[sc_onhub_connect_temp[0].split(' ')[3]]
					for i in range(len(sc_onhub_connect_temp)):
						time_temp = sc_onhub_connect_temp[i].split('"')[1].split('"')[0]
						convert_time = self.convert_utc_timezone(time_temp, gap)
						time = convert_time.split(' ')[0]
						if (Date["year"] == time.split('-')[0]) & (Date["month"] == time.split('-')[1]) & (Date["day"] == time.split('-')[2]) :
							time2 = convert_time.split(' ')[1]
							add_data = float(time2.split(":")[0]) + (float(time2.split(":")[1]) / 60) + ((float(time2.split(":")[2]) / 60) / 60)  # X축 시간 계산  ##########split 데이터 수정
							sc_onhub_connect.append(round(add_data,4))
							index = sc_onhub_connect_temp[i].split(' ')[4]
							onhub_connect_annot[round(add_data,4)]=index+'|'+'MAC address : '+ sc_onhub_connect_temp[i].split(' ')[2].split('"')[1].split('"')[0] +'\n'+'time : '+ convert_time+'\n'+'Action: Connected'
							sc_onhub_connect_index.append(int(index))
				self.onhub_connect = plt.scatter(sc_onhub_connect, sc_onhub_connect_index, color='R', edgecolors='R',s=50, label='Connected')
			else:
				self.onhub_connect = plt.scatter(sc_onhub_connect, sc_onhub_connect_index, color='R', edgecolors='R',s=50)

			if out_data["onhub_disconnect"]:
				sc_onhub_disconnect_temp = out_data["onhub_disconnect"]
				if utc_timezone_dic[sc_onhub_disconnect_temp[0].split(' ')[3]] == utc_timezone:
					for i in range(len(sc_onhub_disconnect_temp)):
						time = sc_onhub_disconnect_temp[i].split(' ')[0].split('"')[1]
						if (Date["year"] == time.split('-')[0]) & (Date["month"] == time.split('-')[1]) & (Date["day"] == time.split('-')[2]):
							time2 = sc_onhub_disconnect_temp[i].split(' ')[1].split('"')[0]
							add_data = float(time2.split(":")[0]) + (float(time2.split(":")[1]) / 60) + ((float(time2.split(":")[2].split(".")[0])/60)/60)  # X축 시간 계산
							sc_onhub_disconnect.append(round(add_data, 4))
							index = sc_onhub_disconnect_temp[i].split(' ')[4]
							sc_onhub_disconnect_index.append(int(index))
							onhub_disconnect_annot[round(add_data, 4)] = index + '|' + 'MAC address : ' + sc_onhub_disconnect_temp[i].split(' ')[2].split('"')[1].split('"')[0] + '\n'+ 'time : ' + sc_onhub_disconnect_temp[i].split(' ')[0].split('"')[1] + ' ' + sc_onhub_disconnect_temp[i].split(' ')[1].split('"')[0]+'\n'+'Action: Disconnected'
						else:
							continue
				else:
					gap = utc_timezone - utc_timezone_dic[sc_onhub_disconnect_temp[0].split(' ')[3]]
					for i in range(len(sc_onhub_disconnect_temp)):
						time_temp = sc_onhub_disconnect_temp[i].split('"')[1].split('"')[0]
						convert_time = self.convert_utc_timezone(time_temp, gap)
						time = convert_time.split(' ')[0]
						if (Date["year"] == time.split('-')[0]) & (Date["month"] == time.split('-')[1]) & (Date["day"] == time.split('-')[2]):
							time2 = convert_time.split(' ')[1]
							add_data = float(time2.split(":")[0]) + (float(time2.split(":")[1]) / 60) + ((float(time2.split(":")[2].split(".")[0])/60)/60)  # X축 시간 계산
							sc_onhub_disconnect.append(round(add_data, 4))
							index = sc_onhub_disconnect_temp[i].split(' ')[4]
							sc_onhub_disconnect_index.append(int(index))
							onhub_disconnect_annot[round(add_data, 4)] = index + '|' + 'MAC address : ' + sc_onhub_disconnect_temp[i].split(' ')[2].split('"')[1].split('"')[0] + '\n'+ 'time : ' + convert_time+'\n'+'Action: Disconnected'
				self.onhub_disconnect = plt.scatter(sc_onhub_disconnect, sc_onhub_disconnect_index, marker='X',color='k', label='Disconnected')
			else:
				self.onhub_disconnect = plt.scatter(sc_onhub_disconnect, sc_onhub_disconnect_index, marker='X',color='k')

			if out_data["amazon_echo"]:
				sc_amazon_echo_temp = out_data["amazon_echo"]
				if utc_timezone_dic[sc_amazon_echo_temp[0][3]] == utc_timezone:
					for i in range(len(sc_amazon_echo_temp)):
						time = sc_amazon_echo_temp[i][0].split('"')[1].split(' ')[0]
						if (Date["year"] == time.split('-')[0]) & (Date["month"] == time.split('-')[1]) & (Date["day"] == time.split('-')[2]):
							time2 = sc_amazon_echo_temp[i][0].split(' ')[1].split('"')[0]
							add_data = float(time2.split(":")[0]) + (float(time2.split(":")[1]) / 60) + ((float(time2.split(":")[2].split(".")[0]) / 60) / 60)  # X축 시간 계산
							sc_amazon_echo.append(round(add_data, 4))
							index = sc_amazon_echo_temp[i][4]
							sc_amazon_echo_index.append(int(index))
							echo_annot[round(add_data, 4)] = 'File name : '+ sc_amazon_echo_temp[i][1] + '\n' +  'time : ' + sc_amazon_echo_temp[i][0].split('"')[1].split('"')[0]  + '\n' +  'command : ' + sc_amazon_echo_temp[i][2]
						else:
							continue
				else:
					gap = utc_timezone - utc_timezone_dic[sc_amazon_echo_temp[0][3]]
					for i in range(len(sc_amazon_echo_temp)):
						time_temp = sc_amazon_echo_temp[i][0].split('"')[1].split('"')[0]
						convert_time = self.convert_utc_timezone(time_temp, gap)
						time = convert_time.split(' ')[0]
						if (Date["year"] == time.split('-')[0]) & (Date["month"] == time.split('-')[1]) & (Date["day"] == time.split('-')[2]):
							time2 = convert_time.split(' ')[1]
							add_data = float(time2.split(":")[0]) + (float(time2.split(":")[1]) / 60) + ((float(time2.split(":")[2].split(".")[0]) / 60) / 60)  # X축 시간 계산
							sc_amazon_echo.append(round(add_data, 4))
							index = sc_amazon_echo_temp[i][4]
							sc_amazon_echo_index.append(int(index))
							echo_annot[round(add_data, 4)] = 'File name : '+ sc_amazon_echo_temp[i][1] + '\n' + 'time : ' + convert_time + '\n' +  'command : ' + sc_amazon_echo_temp[i][2]
				self.amazon_echo = plt.scatter(sc_amazon_echo, sc_amazon_echo_index, marker='*', color='b', label='Command Event')
			else:
				self.amazon_echo = plt.scatter(sc_amazon_echo, sc_amazon_echo_index, marker='*', color='b')

			if out_data["Database"]:
				sc_Database_temp = out_data["Database"]
				if utc_timezone_dic[sc_Database_temp[0][2]] == utc_timezone:
					for i in range(len(sc_Database_temp)):
						time = sc_Database_temp[i][0].split('"')[1].split(' ')[0]
						if (Date["year"] == time.split('-')[0]) & (Date["month"] == time.split('-')[1]) & (Date["day"] == time.split('-')[2]):
							time2 = sc_Database_temp[i][0].split(' ')[1].split('"')[0]
							add_data = float(time2.split(":")[0]) + (float(time2.split(":")[1]) / 60) + (
							(float(time2.split(":")[2].split(".")[0]) / 60) / 60)  # X축 시간 계산
							sc_Database.append(round(add_data, 4))
							index = sc_Database_temp[i][3]
							sc_Database_index.append(int(index))
							Database_annot[round(add_data, 4)] = 'File name : ' +  sc_Database_temp[i][1] + '\n' + 'time : ' + sc_Database_temp[i][0].split('"')[1].split('"')[0] + '\n' + 'Action: File Modified'
						else:
							continue
				else:
					gap = utc_timezone - utc_timezone_dic[sc_Database_temp[0][2]]
					for i in range(len(sc_Database_temp)):
						time_temp = sc_Database_temp[i][0].split('"')[1].split('"')[0]
						convert_time = self.convert_utc_timezone(time_temp, gap)
						time = convert_time.split(' ')[0]
						if (Date["year"] == time.split('-')[0]) & (Date["month"] == time.split('-')[1]) & (Date["day"] == time.split('-')[2]):
							time2 = convert_time.split(' ')[1]
							add_data = float(time2.split(":")[0]) + (float(time2.split(":")[1]) / 60) + ((float(time2.split(":")[2].split(".")[0]) / 60) / 60)  # X축 시간 계산
							sc_Database.append(round(add_data, 4))
							index = sc_Database_temp[i][3]
							sc_Database_index.append(int(index))
							Database_annot[round(add_data, 4)] = 'File name : ' + sc_Database_temp[i][1] + '\n' + 'time : ' + convert_time + '\n' + 'Action: File Modified'
				self.Database = plt.scatter(sc_Database, sc_Database_index, marker='<', color='g', label='File Modified')
			else:
				self.Database = plt.scatter(sc_Database, sc_Database_index, marker='<',color='g')


			plt.legend(loc = 'best')
			self.annot.set_visible(False)
			self.canvas.draw()
			self.canvas.mpl_connect("motion_notify_event", self.event)

	def event(self,event):
		if event.inaxes is not None:
			if self.onhub_connect.contains(event)[0] is True:
				onhub_connect_x, onhub_connect_index = self.onhub_connect.contains(event)
				self.update_connect_onhub(onhub_connect_index)
				self.annot.set_visible(True)
				event.canvas.draw()
			elif self.onhub_disconnect.contains(event)[0] is True:
				onhub_disconnect_x, onhub_disconnect_index = self.onhub_disconnect.contains(event)
				self.update_disconnect_onhub(onhub_disconnect_index)
				self.annot.set_visible(True)
				event.canvas.draw()
			elif self.amazon_echo.contains(event)[0] is True:
				amazon_echo_x, amazon_echo_index = self.amazon_echo.contains(event)
				self.update_amazon_echo(amazon_echo_index)
				self.annot.set_visible(True)
				event.canvas.draw()
			elif self.Database.contains(event)[0] is True:
				Database_x, Database_index = self.Database.contains(event)
				self.updat_database(Database_index)
				self.annot.set_visible(True)
				event.canvas.draw()
			else:
				self.annot.set_visible(False)
				self.canvas.draw_idle()

	def updat_database(self,ind):
		pos = self.Database.get_offsets()[ind["ind"][0]]
		self.annot.xy = pos
		text = Database_annot[pos[0]]
		self.annot.set_text(text)

	def update_amazon_echo(self,ind):
		pos = self.amazon_echo.get_offsets()[ind["ind"][0]]
		self.annot.xy = pos
		text = echo_annot[pos[0]]
		self.annot.set_text(text)

	def update_connect_onhub(self, ind):
		pos = self.onhub_connect.get_offsets()[ind["ind"][0]]
		self.annot.xy = pos
		text = onhub_connect_annot[pos[0]]
		if int(text.split('|')[0]) == pos[1]:
			self.annot.set_text(text.split('|')[1])
		else:
			pass

	def update_disconnect_onhub(self, ind):
		pos = self.onhub_disconnect.get_offsets()[ind["ind"][0]]
		self.annot.xy = pos
		text = onhub_disconnect_annot[pos[0]]
		if int(text.split('|')[0]) == pos[1]:
			self.annot.set_text(text.split('|')[1])
		else:
			pass


if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	MainWindow = QtGui.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())

