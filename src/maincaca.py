import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QLabel, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
from re import search
from typing import List
from fastapi import Depends, FastAPI, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import psycopg2
import sys
sys.path.insert(0, './src')
import models
import schemas
from database import db
from fastapi.responses import FileResponse
import shutil
import json
import os
import os.path
import requests

cur = db.connect()

class MainReviewer2(QDialog, QMainWindow):
    def __init__(self):
        super(MainReviewer2,self).__init__()
        loadUi('reviewercus.ui',self)  
        # ui = MainReviewer()
        # ui.setupUi(self)
        self.tabelsemuapesanan.setColumnWidth(0,200) 
        self.tabelsemuapesanan.setColumnWidth(1,400) 
        self.tabelsemuapesanan.setColumnWidth(2,300) 
        self.buttonpesanan.clicked.connect(self.gotomain1)
        self.load_data()


    def load_data(self):
        headers = {'Accept': 'application/json'}
        req = requests.get('http://127.0.0.1:8000/booking', headers=headers)
        booking_data = req.json()
        self.tabelsemuapesanan.setRowCount(len(booking_data))
        row = 0
        for booking in (booking_data):
            a=str(booking['isDone'])
            if a=="True":
                a="Review Selesai"
            else:
                a="Dalam Review"
            self.tabelsemuapesanan.setItem(row, 0, QtWidgets.QTableWidgetItem(str(booking['ID_Booking'])))
            self.tabelsemuapesanan.setItem(row, 1, QtWidgets.QTableWidgetItem(str(booking['tgl'])))
            self.tabelsemuapesanan.setItem(row, 2, QtWidgets.QTableWidgetItem(a))
            row += 1
    
    def gotomain1(self):
        mainreviewer1=MainReviewer1()
        widget.addWidget(mainreviewer1)
        widget.setCurrentIndex(widget.currentIndex()+1)

class MainReviewer1(QDialog, QMainWindow):
    def __init__(self):
        super(MainReviewer1,self).__init__()
        loadUi('reviewerall.ui',self)  
        # ui = MainReviewer()
        # ui.setupUi(self)
        self.tabelsemuapesanan.setColumnWidth(0,200) 
        self.tabelsemuapesanan.setColumnWidth(1,400) 
        self.tabelsemuapesanan.setColumnWidth(2,300) 
        self.buttonpesanandia.clicked.connect(self.gotomain2)
        self.load_data1()

    def load_data1(self):
        headers = {'Accept': 'application/json'}
        req = requests.get('http://127.0.0.1:8000/bookingall', headers=headers)
        booking_data = req.json()
        self.tabelsemuapesanan.setRowCount(len(booking_data))
        row = 0
        a="Belum Direview"
        for booking in (booking_data):
            self.tabelsemuapesanan.setItem(row, 0, QtWidgets.QTableWidgetItem(str(booking['ID_Booking'])))
            self.tabelsemuapesanan.setItem(row, 1, QtWidgets.QTableWidgetItem(str(booking['tgl'])))
            self.tabelsemuapesanan.setItem(row, 2, QtWidgets.QTableWidgetItem(a))
            row += 1
            # btn = QPushButton(self.tabelsemuapesanan)
            # btn.setText('add')
            # self.tabelsemuapesanan.setCellWidget(booking, 4, btn)

    def gotomain2(self):
        mainreviewer2=MainReviewer2()
        widget.addWidget(mainreviewer2)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
# void MyClass::MySlot()
# {
#     for (int i = 0; i < 10; ++i) {
#         QPushButton button = new QPushButton(this);
#         button.setText(QString::number(i));
#         connect(button, SIGNAL(clicked(bool)), this, SLOT(onClicked(bool)));
#         layout().addWidget(button); 
#         button.show();
#     }
# }


app=QApplication(sys.argv)
mainreviewer=MainReviewer1()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainreviewer)
widget.setFixedWidth(1600)
widget.setFixedHeight(900)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exit")