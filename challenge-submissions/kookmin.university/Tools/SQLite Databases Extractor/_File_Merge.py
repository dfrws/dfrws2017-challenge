# -*- coding: utf-8 -*-

__author__ = "DF&C"

import sys
from collections import OrderedDict
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import string
import time


class MyListWidget(QListWidget):
    def __init__(self, parent):
        super(MyListWidget, self).__init__(parent)
        self.setGeometry(QtCore.QRect(0, 0, 321, 211))
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

        else:
            super(MyListWidget, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        super(MyListWidget, self).dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                self.addItem(url.path())
                event.acceptProposedAction()

        else:
            super(MyListWidget,self).dropEvent(event)



class MyWindow(QWidget):
    def __init__(self):
        super(MyWindow,self).__init__()
        #self.setGeometry(100,100,300,400)
        self.resize(320, 240)
        self.setWindowTitle("Merge")
        self.listWidget_merge = MyListWidget(self)
        self.pushButton_merge = QtWidgets.QPushButton(self)
        self.pushButton_merge.setGeometry(QtCore.QRect(-6, 210, 331, 31))
        self.pushButton_merge.setObjectName("pushButton_merge")
        
        self.pw_label = QtWidgets.QLabel(self)
        self.pw_label.setGeometry(QtCore.QRect(0, 0, 321, 241))
        self.pw_label.setObjectName("pw_label")
        self.pw_label.lower()
        self.listWidget_merge.raise_()
        self.pushButton_merge.raise_()
        self.pushButton_merge.clicked.connect(self.FileMake)
        
        self.retranslateUi(self)

    def retranslateUi(self, Form):
        self._translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(self._translate("Form", "Merge"))
        self.pushButton_merge.setText(self._translate("Form", "Merge"))
        self.pw_label.setText(self._translate("Merge", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:600;\">Please wait...</span></p></body></html>"))


    def FileMake(self):
        self.listWidget_merge.lower()
        self.pushButton_merge.lower()
        self.pw_label.raise_()
        self.listWidget_merge.setEnabled(False)
        self.pushButton_merge.setEnabled(False)
        self.make()

       
    def make(self):
        time.sleep(1)
        items = []
        for index in xrange(self.listWidget_merge.count()):
            items.append(self.listWidget_merge.item(index).text().encode("UTF-8")[1:])
        
        items.sort()
        #print items
        
        try:
            w=open('File_Merge_Result','wb')
            for x in range (len(items)):
                t=open(items[x],'rb')
                while True:
                    data = t.read(51200)
                    if data=='':break
                    w.write(data)
                t.close
            w.close

            self.pw_label.setText(self._translate("Merge", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:600;\">File Merge Success!!</span></p></body></html>"))
            
            
            # self.pw_label.lower()
            # self.listWidget_merge.raise_()
            # self.pushButton_merge.raise_()
            # self.listWidget_merge.setEnabled(True)
            # self.pushButton_merge.setEnabled(True)

        except Exception as ex: 
            self.pw_label.setText(self._translate("Merge", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:600;\">File Open Error...</span></p></body></html>"))
             

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
