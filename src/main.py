import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QLabel, QMainWindow, QMessageBox, QCheckBox, QLineEdit
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from typing import List
import requests
import urllib
import json

loggedin = False
currentUser = ''
class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi('login.ui',self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.gotocreate)
        self.loginaccbutton_3.clicked.connect(self.gotoreset)
        
    def loginfunction(self):
        email=self.email.text()
        password=self.password.text()
        f = {'email' : email, 'password' : password}
        parsed = (urllib.parse.urlencode(f))
        url = 'http://127.0.0.1:8000/login?' + parsed
        hasil =  requests.get(url)
        x = str(hasil.text)
        global loggedin
        global currentUser 
        if hasil.text == "true":
            loggedin = True
            f = {'em' : email}
            parsed = (urllib.parse.urlencode(f))
            url = 'http://127.0.0.1:8000/ambilDataTuteers?' + parsed
            hasil =  requests.get(url)
            currentUser = hasil.json()
            widget.setCurrentIndex(3) #Nanti diganti jadi ke tuteers
        else:
            url = 'http://127.0.0.1:8000/loginadmin?' + parsed
            hasil =  requests.get(url)
            if hasil.text == "true":
                loggedin = True
                f = {'em' : email}
                parsed = (urllib.parse.urlencode(f))
                url = 'http://127.0.0.1:8000/ambilDataReviewer?' + parsed
                hasil =  requests.get(url)
                currentUser = hasil.json()
                print(currentUser)
                widget.setCurrentIndex(3) #nanti diganti ke admin
            else:
                loggedin = False
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('Login Tidak Berhasil!')
                msg.exec_()
        return

    def gotocreate(self):
        widget.setCurrentIndex(1)

    def gotoreset(self):
        widget.setCurrentIndex(2)
    
class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc,self).__init__()
        loadUi("createacc.ui",self)
        self.signupbutton.clicked.connect(self.createaccfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.loginaccbutton.clicked.connect(self.gotologin)
    
    def createaccfunction(self):
        jeniskelamin = ""
        if self.Female.isChecked():
            jeniskelamin = "Female"
        elif self.Male.isChecked():
            jeniskelamin = "Male"

        if self.password.text()==self.confirmpass.text():
            jen = jeniskelamin
            namalengkap = self.namalengkap.text()
            email = self.email.text()
            year = self.year.text()
            month = self.month.text()
            date = self.date.text()
            nomorhp = self.nomorhp.text()
            password=self.password.text()
            confirmpass = self.confirmpass.text()
            f = {'name': namalengkap, 'email' : email, 'password' : password, 'reenterpass' : confirmpass, 'noHP':nomorhp, 'year':year, 'month':month, 'date' : date,'gender': jen}
            parsed = (urllib.parse.urlencode(f))
            url = 'http://127.0.0.1:8000/registerSQL?' + parsed
            requests.post(url)
            QLineEdit.clear(self)
            widget.setCurrentIndex(0)
            
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Input Password Salah!')
            msg.exec_()

    def gotologin(self):
        widget.setCurrentIndex(0)

class ResetPassword(QDialog):
    def __init__(self):
        super(ResetPassword,self).__init__()
        loadUi('resetpass.ui',self)  
        self.kembali.clicked.connect(self.back)
        self.simpanbutton.clicked.connect(self.resetpass)
    def resetpass(self):
        if self.passbaru.text()==self.passbaru_2.text():
            f = {'email': self.passlama.text(), 'passbaru' : self.passbaru.text()}
            parsed = (urllib.parse.urlencode(f))
            url = 'http://127.0.0.1:8000/resetPasswordSQL/?' + parsed
            requests.get(url)
            widget.setCurrentIndex(0)
    def back(self):
        widget.setCurrentIndex(0) 

class AboutUs(QDialog):
    def __init__(self):
        super(AboutUs,self).__init__()
        loadUi('aboutme.ui',self) 
        self.logoutbutton.clicked.connect(self.gotologin)     
        self.aboutmebutton.clicked.connect(self.gotoaboutus) 
        # self.logoutbutton.connect(self.usr)
        # self.layananbutton.clicked.connect(self.gotolayanan) 
    
    # def usr(self):
    #     # a = (currentUser['nama'])
    #     a=""
    #     a = 'sstela'
    #     print(currentUser)
    #     if (currentUser!=''):
    #         a = currentUser['nama']
    #         a = a[0:]
    #     self.logoutbutton.setText(a)    

    def gotologin(self):
        widget.setCurrentIndex(0)
    # def gotolayanan(self):
    #     widget.setCurrentIndex(#lalaalala)
    def gotoaboutus(self):
        widget.setCurrentIndex(3)    
app=QApplication(sys.argv)
widget=QtWidgets.QStackedWidget()

widget.addWidget(Login()) #Index jadi 0
widget.addWidget(CreateAcc()) 
widget.addWidget(ResetPassword())
widget.addWidget(AboutUs())  
widget.setFixedWidth(1600)
widget.setFixedHeight(900)
widget.show()
app.exec_()
