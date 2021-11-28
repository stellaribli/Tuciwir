import sys
# import design
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QLabel, QMainWindow, QMessageBox, QCheckBox
from PyQt5 import QtGui, QtCore
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from re import search
from typing import List
import requests
import urllib


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
            print(hasil.json())
            print("Successfully logged in with email: ", email)
            widget.setCurrentIndex(2) #Nanti diganti jadi ke tuteers
        else:
            url = 'http://127.0.0.1:8000/loginadmin?' + parsed
            hasil =  requests.get(url)
            if hasil.text == "true":
                loggedin = True
                f = {'em' : email}
                parsed = (urllib.parse.urlencode(f))
                url = 'http://127.0.0.1:8000/ambilDataReviewer?' + parsed
                hasil =  requests.get(url)
                print(hasil.json())
                print("Berhasil Login Sebagai Admin!")
                widget.setCurrentIndex(2) #nanti diganti ke admin
            else:
                print("Password Salah")
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
            print("Successfully created acc with email: ", email)
            widget.setCurrentIndex(0)
        else:
            print("Password Berbeda!")
            msg = QMessageBox()
            msg.setWindowTitle("Tutorial on PyQt5")
            msg.setText("This is the main text!")    
            msg.exec_()

    def gotologin(self):
        # prevIndex = 1
        widget.setCurrentIndex(0)

class ResetPassword(QDialog):
    def __init__(self):
        super(ResetPassword,self).__init__()
        loadUi('resetpass.ui',self)  
        self.kembali.clicked.connect(self.back)

    def resetpass(self):
        if self.passbaru.text()==self.passbaru_2.text():
            parse = {'email': self.passlama.text(), 'passbaru' : self.passbaru.text()}
            url = 'http://127.0.0.1:8000/resetPasswordSQL/?' + parse
            requests.get(url)
            widget.setCurrentIndex(0)
            
    def back(self):
        prevIndex = 0
        widget.setCurrentIndex(0) 

app=QApplication(sys.argv)
mainwindow=CreateAcc()
widget=QtWidgets.QStackedWidget()

widget.addWidget(Login()) #Index jadi 0
widget.addWidget(CreateAcc())  #Index jadi 1
widget.addWidget(ResetPassword())  #Index jadi 2
widget.setFixedWidth(1600)
widget.setFixedHeight(900)
widget.show()
app.exec_()
