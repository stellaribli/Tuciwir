import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QLabel, QMainWindow
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

class MainReviewer(QDialog):
    def __init__(self):
        super(MainReviewer,self).__init__()
        loadUi('reviewerall.ui',self)   
        self.tabelsemuapesanan.setColumnWidth(0,300) 
        self.tabelsemuapesanan.setColumnWidth(1,400) 
        self.tabelsemuapesanan.setColumnWidth(2,300) 
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
            self.tabelsemuapesanan.setItem(row, 1, QtWidgets.QTableWidgetItem(str(booking['tgl_pesan'])))
            self.tabelsemuapesanan.setItem(row, 2, QtWidgets.QTableWidgetItem(a))
            row += 1
        # item = cur.execute('SELECT b."ID_Booking", b."tgl_pesan", r."isDone" FROM booking b, review r WHERE r."ID_Booking"=b."ID_Booking"')
        # isdone = cur.execute('SELECT r."isDone" FROM booking b, review r WHERE r."ID_Booking"=b."ID_Booking"')
        # result = item.fetchall()
        # resultisdone = isdone.fetchall()
        # # return result
        # tablerow = 0
        # self.tabelsemuapesanan.setRowCount(5)
        # # if item."isDone" = True:
        # #     isDone = 'Sudah Selesai'
        # tablerow = 0
        # for row in result:
        #     # for dua in resultisdone:
        #     #     print(row)
        #     #     if dua=="True":
        #     #         dua="Sudah Selesai"
        #     #     print(dua)
        # # print("hai")
        # # print(result[:2])
        #     self.tabelsemuapesanan.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0]))
        #     self.tabelsemuapesanan.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[0]))
        #     tablerow+=1
# class Login(QDialog):
#     def __init__(self):
#         super(Login,self).__init__()
#         loadUi('login.ui',self)
#         self.loginbutton.clicked.connect(self.loginfunction)
#         self.password.setEchoMode(QtWidgets.QLineEdit.Password)
#         self.createaccbutton.clicked.connect(self.gotocreate)
        
#     def loginfunction(self):
#         email=self.email.text()
#         password=self.password.text()
#         print("Successfully logged in with email: ", email, "and password:", password)
        
#         data = requests.get('http://127.0.0.1:8000/booking')
#         print(data.json())

#     def gotocreate(self):
#         createacc=CreateAcc()
#         widget.addWidget(createacc)
#         widget.setCurrentIndex(widget.currentIndex()+1)

# class CreateAcc(QDialog):
#     def __init__(self):
#         super(CreateAcc,self).__init__()
#         loadUi("createacc.ui",self)
#         self.signupbutton.clicked.connect(self.createaccfunction)
#         self.password.setEchoMode(QtWidgets.QLineEdit.Password)
#         self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)
#         self.loginaccbutton.clicked.connect(self.gotologin)


#     def createaccfunction(self):
#         namalengkap = self.namalengkap.text()
#         email = self.email.text()
#         tanggallahir = self.tanggallahir.text()
#         jeniskelamin = self.jeniskelamin.text()
#         nomorhp = self.nomorhp.text()
#         if self.password.text()==self.confirmpass.text():
#             password=self.password.text()
#             print("Successfully created acc with email: ", email)
#             text_file = open("login.txt", "w")
#             text_file.write(namalengkap + '\n')
#             text_file.write(email + '\n')
#             text_file.write(tanggallahir + '\n')
#             text_file.write(jeniskelamin + '\n')
#             text_file.write(nomorhp + '\n')
#             text_file.write(password)
#             text_file.close()
#             login=Login()
#             widget.addWidget(login)
#             widget.setCurrentIndex(widget.currentIndex()+1)
#         else:
#             print("Password Berbeda!")

#     def gotologin(self):
#         loginacc=Login()
#         widget.addWidget(loginacc)
#         widget.setCurrentIndex(widget.currentIndex()+1)

app=QApplication(sys.argv)
mainreviewer=MainReviewer()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainreviewer)
widget.setFixedWidth(1600)
widget.setFixedHeight(900)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exit")