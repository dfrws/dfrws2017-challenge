 # -*- coding: utf8 -*-

__author__ = "DF&C"

import sys
from collections import OrderedDict
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import string
import _DB_Collector
import _File_Merge
from datetime import datetime, timedelta
import sqlite3
from tabulate import tabulate
import csv
import re
import os

class Merge_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(320, 240)
        self.listView_merge = QtWidgets.QListView(Form)
        self.listView_merge.setGeometry(QtCore.QRect(0, 0, 321, 211))
        self.listView_merge.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.listView_merge.setObjectName("listView_merge")
        self.pushButton_merge = QtWidgets.QPushButton(Form)
        self.pushButton_merge.setGeometry(QtCore.QRect(-6, 210, 331, 31))
        self.pushButton_merge.setObjectName("pushButton_merge")
        self.pw_label = QtWidgets.QLabel(Form)
        self.pw_label.setGeometry(QtCore.QRect(0, 0, 321, 211))
        self.pw_label.setObjectName("pw_label")
        self.pw_label.raise_()
        self.listView_merge.raise_()
        self.pushButton_merge.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_merge.setText(_translate("Form", "Mearge"))
        self.pw_label.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:600;\">Please wait...</span></p></body></html>"))



class Ui_MainWindow(QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(880, 570)
        MainWindow.setFixedSize(880,570)
        MainWindow.setStyleSheet(" QScrollBar:vertical {\n"
"     border: None;\n"
"     background: #4A4A4A;\n"
"     width: 15px;\n"
"     margin: 0px 0 0px 0;\n"
" }\n"
" QScrollBar::handle:vertical {\n"
"     background: grey;\n"
"     min-height: 30px;\n"
" }\n"
" QScrollBar::add-line:vertical {\n"
"     border: None;\n"
"     background: None;\n"
"     height: 10px;\n"
"     subcontrol-position: bottom;\n"
"     subcontrol-origin: margin;\n"
" }\n"
"\n"
" QScrollBar::sub-line:vertical {\n"
"     border: None;\n"
"     background: None;\n"
"     height: 1px;\n"
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"     border:None;\n"
"     width: 1px;\n"
"     height: 1px;\n"
"     background: None;\n"
" }\n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
"\n"
"\n"
"QScrollBar:horizontal {\n"
"    border: #4A4A4A;\n"
"    background: #4A4A4A;\n"
"    \n"
"    height: 15px;\n"
"    margin: 0px 0px 0 0px;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background: grey;\n"
"    min-width: 20px;\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    border: None;\n"
"    background: None;\n"
"    width: 20px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:horizontal {\n"
"    border: None;\n"
"    background: None;\n"
"    width: 20px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-page:horizontal {\n"
"    background: None;\n"
"}\n"
"QScrollBar::add-page:horizontal {\n"
"    background: None;\n"
"}\n"
"QMenuBar {\n"
"    background-color: #252525\n"
"}\n"
"\n"
"QMenuBar::item {\n"
"\n"
"color : white\n"
"}\n"
"\n"
"QMenuBar::item:selected { \n"
"    background: #A4A4A4;\n"
"}\n"
"\n"
"QMenuBar::item:pressed {\n"
"    background: #A4A4A4;\n"
"}\n"
"\n"
"QMenu{\n"
"    Background-color:#252525;\n"
"    border: None;\n"
"}\n"
"QMenu::item{\n"
"     color : white\n"
"}\n"
"QMenu::item:selected { \n"
"    background: #A4A4A4;\n"
"}\n"
"QMenu::item:pressed {\n"
"    background: #A4A4A4;\n"
"}\n"
"QLabel{\n"
"    color : white;\n"
"}\n"
)

        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)

        brush = QtGui.QBrush(QtGui.QColor(36, 36, 36))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)


        brush = QtGui.QBrush(QtGui.QColor(74, 74, 74))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)

        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)


        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(640, 505, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setEnabled(False)

        self.pushButton_save = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_save.setGeometry(QtCore.QRect(730, 505, 115, 23))
        self.pushButton_save.setObjectName("pushButton_save")

        self.pushButton_back = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_back.setGeometry(QtCore.QRect(500, 505, 115, 23))
        self.pushButton_back.setObjectName("pushButton_back")
        self.pushButton_back.setEnabled(False)
        

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 450, 831, 16))
        self.label.setText("파일 : ")
        self.label.setObjectName("label")

        self.treeWidget = QtWidgets.QTreeWidget(MainWindow)
        self.treeWidget.setGeometry(QtCore.QRect(20, 50, 831, 412))
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.header().setVisible(True)
        self.treeWidget.header().hide() 
        self.treeWidget.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.treeWidget.header().setStretchLastSection(True)
        self.treeWidget.setPalette(palette)
        self.treeWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        #self.treeWidget.raise_()
        
        font = QtGui.QFont()
        font.setFamily("굴림체")
        font.setBold(False)
        font.setWeight(50)

        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(20, 30, 831, 411))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setFont(font)
        self.textBrowser.setPalette(palette)
        self.textBrowser.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.textBrowser.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)

        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(20, 470, 831, 31))
        #self.textBrowser_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #self.treeWidget.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.textBrowser_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.textBrowser_2.setFont(font)
        self.textBrowser_2.setPalette(palette)
        self.textBrowser_2.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.treeWidget.itemClicked.connect(self.item_view)
        self.pushButton.clicked.connect(self.sqlite_view)
        self.pushButton_save.clicked.connect(self.file_save)
        self.pushButton_back.clicked.connect(self.back)
        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setPalette(palette)
        
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        #self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_Open = QtWidgets.QAction(MainWindow)
        self.action_Open.setObjectName("action_Open")
        self.action_Merge = QtWidgets.QAction(MainWindow)
        self.action_Merge.setObjectName("action_merge")

        self.menu_File.addAction(self.action_Open)
        self.menu_File.addAction(self.action_Merge)

        self.menubar.addAction(self.menu_File.menuAction())
        
        self.action_Open.triggered.connect(self.Open_file)
        self.action_Merge.triggered.connect(self.Merge_file)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.time_l ='s'

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", ""))                    
        self.pushButton.setText(_translate("MainWindow", "DB_VIEW"))
        self.pushButton_save.setText(_translate("MainWindow", "Make_File"))
        self.pushButton_back.setText(_translate("MainWindow", "Back"))
        MainWindow.setWindowTitle(_translate("MainWindow", "DB_Viewer"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.action_Open.setText(_translate("MainWindow", "&Open File"))
        self.action_Merge.setText(_translate("MainWindow","&Merge"))

        self.action_Open.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.action_Merge.setShortcut(_translate("MainWindow","Ctrl+M"))
        
    def Merge_file(self):
        #print 'm'
        #app_m = QtWidgets.QApplication(sys.argv)
        #self.Form_m = QApplication(sys.argv)

        self.A=_File_Merge.MyWindow()
        self.A.show()
        #self.Form_m.show()
        #sys.exit(app_m.exec_())
        
    def Open_file(self):
        try:
            self.data_dict={}
            self.data_dict.clear()
            
            self.filename = QFileDialog.getOpenFileName(None, 'Open File',"D:\\")
        
            name=self.filename[0].encode("UTF-8")
            name=name.split('/')

            self.entry=_DB_Collector.Directory_entry(self.filename[0])

            data =self.entry.export_data()
        
            self.lines = data[0]
            self.data_dict =data[1]
            self.SGD =data[2]
            self.IPG =data[3]
            self.GDB =data[4]
            self.ext4_list=data[5]


            self.linesA=[]
            self.linesB=[]
            self.linesC=[]

            self.treeWidget.clear()
            self.textBrowser.setText('')
            self.textBrowser_2.setText('')
            self.label.setText('File : %s'%name[len(name)-1])
            
            self.filter()

            self.lines.sort()
            self.linesA.sort()
            self.linesB.sort()
            self.linesC.sort()

            if len(self.linesA)!=0:
                parent = QTreeWidgetItem(self.treeWidget)
                parent.setText(0,'MAC_Address_List')
                for line in self.linesA:
                    child = QTreeWidgetItem(parent)
                    child.setText(0,line)

            if len(self.linesB)!=0:
                parent2 = QTreeWidgetItem(self.treeWidget)
                parent2.setText(0,'Device_Info')
                for line in self.linesB:
                    child = QTreeWidgetItem(parent2)
                    child.setText(0,line)

            if len(self.linesC)!=0:
                parent3 = QTreeWidgetItem(self.treeWidget)
                parent3.setText(0, 'DB_List')
                for line in self.linesC:
                    child = QTreeWidgetItem(parent3)
                    #    child.setFlags(child.flags() | QtCore.Qt.ItemIsUserCheckable)
                    child.setText(0, line)
                    #    child.setCheckState(0, QtCore.Qt.Unchecked)

            #####TEST ALL-ITEMS#####
            # parent4 = QTreeWidgetItem(self.treeWidget)
            # parent4.setText(0,'TEST-PAGE')
            # for line in self.lines:
            #     child = QTreeWidgetItem(parent4)
            #     child.setText(0,line)
           


            self.treeWidget.expandAll()


        except Exception as ex: 
            print ex
            return 0 
    
    def filter(self):
        try:
            db_list=['db','mdb','accdb','adp','dbf','database']
            
            name1 = '/system/usagestats/usage-'
            name2 = '/misc/bluedroid/bt_config.xml'
            name3 = '/misc/wifi/wpa_supplicant.conf'
            name4 = '/bluetooth/bt_addr'
            name5 = '/wifi/.mac.info'

            A=re.compile('/([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2}')
            B=re.compile('%s[0-9]{8}|%s|%s|%s|%s'%(name1,name2,name3,name4,name5))
            del self.linesA[0:len(self.linesA)]
            del self.linesB[0:len(self.linesB)]
            del self.linesC[0:len(self.linesC)]
            #self.liens_filter=[]
            for line in self.lines:
                if line.split('/')[-1:][0] in db_list or line.split('.')[-1:][0] in db_list :
                    self.linesC.append(line)
                #DB

                elif A.match(line[-18:]) :
                    self.linesA.append(line)
                #MAC

                elif B.search(line):
                    self.linesB.append(line)
                #device info

        except Exception as ex: 
            print ex
            return 0

    def sqlite_view(self):
        try:
            self.textBrowser.raise_()
            self.treeWidget.lower()

            colmIndex=0
            data= str(self.treeWidget.currentItem().text(colmIndex))#.split('/')
            #current = self.treeWidget.currentItem()
            conn = sqlite3.connect(self.Model_Name+'/DB/'+data)#[-1])
            cursor =conn.cursor()
            table = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            
            t_name=[]           
            for name in table:
                t_name.append(name[0])
            
            self.textBrowser.setText('')

            self.pushButton_back.setEnabled(True)

            for name in t_name:
                cursor.execute("SELECT * FROM %s"%name)
                self.textBrowser.insertPlainText(name+'_table\n')
                names = list(map(lambda x: x[0], cursor.description))
                rows=cursor.fetchall()
                self.textBrowser.insertPlainText(tabulate(rows,headers=names)+'\n\n\n')

            cursor.close()
            conn.close()

        except Exception as ex: 
            print ex
            self.pushButton_back.setEnabled(True)
            self.textBrowser_2.setText(str(ex))
            return 0  

    def back(self):
        try:
            self.textBrowser.lower()
            self.treeWidget.raise_()
            self.textBrowser.setText("")
            self.pushButton_back.setEnabled(False)
            
        except Exception as ex: 
            print ex
            return 0
           
    def item_view(self):
        try:
            colmIndex=0
            data= str(self.treeWidget.currentItem().text(colmIndex))
            
            self.partition_tmp=self.ext4_list[int(data[0:1])]


            if data not in self.linesC:
                self.pushButton.setEnabled(False)
                
            for inode,name in self.data_dict.items():
                if name==data:
                    #self.download_file(inode,name)
                    break
            self.time_l = self.modified_time(inode,name)
            self.textBrowser_2.setText('%s :: Inode : %08X :: 최종수정시간 : %s'%(data.split('/')[-1:][0],inode,str(self.time_l[0])+' '+str(self.time_l[1])))
            
            try:
                if open((self.Model_Name+'/DB/'+data),'rb'):
                    self.pushButton.setEnabled(True)
            except:
                print '1'

        except Exception as ex:
            print ex
            return 0    

    def depth_f(self,offset,b_n_offset):
        f=open(self.filename[0],'rb')
        internal_offset=[]
        f.seek(offset)
        
        data=f.read(12)
        if(ord(data[0])!=0x0A and (ord(data[1])!=0xF3)):
            return 0

        depth=ord(data[6])^(ord(data[7])<<8)
        if (depth ==0 ):
            leaf_num=ord(data[2])^(ord(data[3])<<8)
            while leaf_num>0:
                exdata=f.read(6)
                blockcount=ord(exdata[4])^(ord(exdata[5])<<8)
                exdata=f.read(6)
                lenexdata=len(exdata)
                n_offset=0
                for i in range(lenexdata):
                    n_offset^=(ord(exdata[(lenexdata+1-i)%lenexdata])<<(((lenexdata-1)*8)-8*i))
                n_offset=n_offset*0x1000+self.partition_tmp
                b_n_offset.append(str(blockcount)+'_'+str(n_offset))
                leaf_num-=1
        else:
            internal_num=ord(data[2])^(ord(data[3])<<8)
            while internal_num>0:
                n_offset=0
                internaldata=f.read(12)
                n_offset=(ord(internaldata[9])<<40)^(ord(internaldata[8])<<32)^(ord(internaldata[7])<<24)^(ord(internaldata[6])<<16)^(ord(internaldata[5])<<8)^(ord(internaldata[4]))
                n_offset=n_offset*0x1000+self.partition_tmp
                internal_offset.append(n_offset)
                internal_num-=1
            for i in range(len(internal_offset)):
                self.depth_f(internal_offset[i],b_n_offset)
        f.close
                
    def download_file(self,inode,name):
        #op=name.split('/')[-1:]
        self.textBrowser.setText('')
        directory = os.path.split(name)
        if not os.path.exists(directory[0]):
            os.makedirs(directory[0])
        f=open(self.filename[0],'rb')
        m=open(name,'wb')
        #print self.partition_tmp
        #print inode,SGD
        #######################################################################
        blocknum=(inode-1)/self.IPG
        inodeT=(inode%self.IPG)-1
        f.seek(self.GDB+(blocknum*self.SGD)+0x08)
        readTable=f.read(4)
        readTable=(ord(readTable[0]))^(ord(readTable[1])<<8)^(ord(readTable[2])<<16)^(ord(readTable[3])<<24)
        readTable=(readTable*0x1000) + (inodeT*0x100)+self.partition_tmp

        # f.seek(readTable+0x10)
        # last=f.read(4)
        # last=(ord(last[0]))^(ord(last[1])<<8)^(ord(last[2])<<16)^(ord(last[3])<<24)
        # self.time_l = str(datetime(1970,1,1,0,0,0)+timedelta(seconds=last))+' (UTC+09:00)'
        
        # self.textBrowser_2.setText('%s :: Inode : %08X :: 최종수정시간 : %s'%(directory[1],inode,self.time_l))
        b_n_offset=[]
        
        self.depth_f(readTable+0x28,b_n_offset)
        #######################################################################
        offset=0
        self.treeWidget.setEnabled(False) # View가 완성될때까진 클릭막기
        self.pushButton.setEnabled(False)
        self.pushButton_save.setEnabled(False)
        self.pushButton.setText('wait..')
        
        for i in range(len(b_n_offset)):
            count=0
            bn=int(b_n_offset[i].split('_')[0])
            f.seek(int(b_n_offset[i].split('_')[1]))
            while count<bn*0x1000:
                data= f.read(0x1000)
                m.write(data)
                # len_data =len(data)
                # result = "      %04X : "%offset

                # for i in range(len_data): result +='%02X '%ord(data[i])
                # for i in range(len_data):
	            #     if(ord(data[i])) >=32  and (ord(data[i])) <=126 : result += data[i]
	            #     else : result += '.'

                #offset+=16
                count+=0x1000
                
                #self.printHEX.connect(result)
                #self.textBrowser.insertPlainText(result+'\n')
                QApplication.processEvents()

        
        self.treeWidget.setEnabled(True)  # View가 완성되면 클릭 다시가능하게하기  
        
        self.pushButton_save.setEnabled(True)
        self.pushButton.setText('DB_VIEW')
        m.close
        f.close

        del b_n_offset[0:len(b_n_offset)]

    def modified_time(self,inode,name):
        f=open(self.filename[0],'rb')
        blocknum=(inode-1)/self.IPG
        inodeT=(inode%self.IPG)-1
        f.seek(self.GDB+(blocknum*self.SGD)+0x08)
        readTable=f.read(4)
        readTable=(ord(readTable[0]))^(ord(readTable[1])<<8)^(ord(readTable[2])<<16)^(ord(readTable[3])<<24)
        readTable=(readTable*0x1000) + (inodeT*0x100)+self.partition_tmp

        f.seek(readTable+0x10)
        last=f.read(4)
        last=(ord(last[0]))^(ord(last[1])<<8)^(ord(last[2])<<16)^(ord(last[3])<<24)

        utc=0

        time_t=[datetime(1970,1,1,0+utc,0,0)+timedelta(seconds=last),'(UTC+{0:02d}:00)'.format(utc)]    
        return time_t 
        
    def file_save(self):
        #make_CSV
        try:
            self.Model_Name =''
            text, ok = QInputDialog.getText(self,'Type Model Name','Type Model Name')
            if ok:
                self.Model_Name = text
            else:
                return 0
            ##########################################################################
            self.treeWidget.setEnabled(False) # 완성될때까진 클릭막기
            self.pushButton.setEnabled(False)
            self.pushButton_save.setEnabled(False)
            
            #self.lines
            if len(self.linesC)!=0:
                log=[]

                for line in self.linesC:
                    for inode,name in self.data_dict.items():
                        if name==line:
                            self.partition_tmp=self.ext4_list[int(line[0:1])]
                            #log.append([name,Model_Name,self.modified_time(inode,name)])
                            A=self.modified_time(inode,name)
                            # A_D=str(A[0].strftime('%Y-%m-%d'))
                            # A_M=str(A[0].strftime('%H:%M:%S'))
                            log.append([A[0].strftime('=\"%Y-%m-%d %H:%M:%S\"'),name])
                csvname='%s/%s.csv'%(self.Model_Name,self.filename[0].split('/')[-1:][0])
                #bluetooth_csv='%s/bluetooth.csv'%self.Model_Name
                #print csvname
    
                directory = os.path.dirname(csvname)
                if not os.path.exists(directory):
                    os.makedirs(directory)

                nowt=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                pathname='Database_%s(%s)-%s'%(self.filename[0].split('/')[-1:][0],self.Model_Name,nowt)
                f= open(csvname,'wb') 
                wr=csv.writer(f)
                wr.writerow([pathname,A[1]])
                wr.writerow(['Modified Time','FileName'])
                for i in range(len(log)):
                    wr.writerow(log[i])

                f.close()
                del log[0:len(log)]
            
        except Exception as ex:
            print ex
            return 0

        #make_db & device_info
        try:
            for line in self.linesC:
                for inode,name in self.data_dict.items():
                    if name==line:
                        self.partition_tmp=self.ext4_list[int(line[0:1])]
                        self.download_file(inode,self.Model_Name+'/DB/'+name)

            for line in self.linesB:
                for inode,name in self.data_dict.items():
                    if name==line:
                        self.partition_tmp=self.ext4_list[int(line[0:1])]
                        self.download_file(inode,self.Model_Name+'/Device_Info/'+name)

        except Exception as ex:
            print ex,'db_error_page'
            return 0   
        ##make_MAC_address
        try:
            if len(self.linesA)!=0:

                bluetooth_csv='%s/bluetooth.csv'%self.Model_Name

                directory = os.path.dirname(bluetooth_csv)
                if not os.path.exists(directory):
                    os.makedirs(directory)

                f= open(bluetooth_csv,'wb') 
                wr=csv.writer(f)
                wr.writerow(['MAC_Address','name','Time Data'])
                for line in self.linesA:
                    for inode,name in self.data_dict.items():
                        if name==line:
                            bt=self.entry.InodeTable(inode)
                            for j in range(len(bt)):
                                caloffset=int(bt[j].split('_')[1])
                            btf=open(self.filename[0],'r')
                            btf.seek(caloffset)
                            btname=btf.readline()
                            btname=btf.readline()
                            btf.close
                            

                            A=self.modified_time(inode,name)
                            try:
                                log.append([name.split('/')[-1],btname.split('=')[1].split('\n')[0],A[0]])
                            except:
                                log.append([name.split('/')[-1],self.Model_Name,A[0]])
                                        
                for i in range(len(log)):
                    wr.writerow(log[i])
                # for i in range(len(self.linesA)):
                #     wr.writerow(self.linesA[i])

                f.close()
                del log[0:len(log)]
            

        except Exception as ex:
            print ex , 'MAC_error_page'
            return 0

        self.treeWidget.setEnabled(True) # 완성될때까진 클릭막기
        self.pushButton.setEnabled(True)
        self.pushButton_save.setEnabled(True)

if __name__ == "__main__":
    import sys  #gui


    app = QtWidgets.QApplication(sys.argv) 
    MainWindow = QtWidgets.QMainWindow() 
    
    ui = Ui_MainWindow() 
    ui.setupUi(MainWindow) 
    MainWindow.show() 
    sys.exit(app.exec_()) 


   