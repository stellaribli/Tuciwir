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

# prevIndex = 0
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
        print("Successfully logged in with email: ", email, "and password:", password)
        return

    def gotocreate(self):
        prevIndex = 0
        widget.setCurrentIndex(1)

    def gotoreset(self):
        prevIndex = 0
        widget.setCurrentIndex(2)    
    

class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc,self).__init__()
        loadUi("createacc.ui",self)
        self.signupbutton.clicked.connect(self.createaccfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.loginaccbutton.clicked.connect(self.gotologin)
        # self.kembali.clicked.connect(self.back)

    # def back(self):
    #     a = prevIndex
    #     prevIndex = 1
    #     widget.setCurrentIndex(a)            

    def createaccfunction(self):
        jeniskelamin = ""
        if self.Female.isChecked():
            jeniskelamin = "Female"
        elif self.Male.isChecked():
            jeniskelamin = "Male"

        if self.password.text()==self.confirmpass.text():
            print(jeniskelamin)
            namalengkap = self.namalengkap.text()
            email = self.email.text()
            year = self.year.text()
            month = self.month.text()
            date = self.date.text()
            nomorhp = self.nomorhp.text()
            password=self.password.text()
            confirmpass = self.confirmpass.text()
            # print(isChecked(self.Female))
            # fem = self.Female.toggled.connect(lambda:self.btnstate(self.Female))
            # url = 'http://127.0.0.1:8000/registerSQL?name=' + namalengkap + '&email=' + email + '&password=' + password + '&reenterpass=' + confirmpass + '&noHP=' + nomorhp + '&year=' + year + '&month=' + month + '&date=' + date + '&gender=' + jeniskelamin
            # requests.post(url)
            print("Successfully created acc with email: ", email)
            login=Login()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex()+1)
        else:
            print("Password Berbeda!")
            msg = QMessageBox()
            msg.setWindowTitle("Tutorial on PyQt5")
            msg.setText("This is the main text!")    
            x = msg.exec_()

    def gotologin(self):
        loginacc=Login()
        # prevIndex = 1
        widget.setCurrentIndex(0)

class ResetPassword(QDialog):
    def __init__(self):
        super(ResetPassword,self).__init__()
        loadUi('resetpass.ui',self)  
        self.kembali.clicked.connect(self.back)

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