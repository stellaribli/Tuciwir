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

class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi('login.ui',self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.gotocreate)
        
    def loginfunction(self):
        email=self.email.text()
        password=self.password.text()
        print("Successfully logged in with email: ", email, "and password:", password)
        return

    def gotocreate(self):
        createacc=CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)


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
        widget.addWidget(loginacc)
        widget.setCurrentIndex(widget.currentIndex()+1)

app=QApplication(sys.argv)
mainwindow=CreateAcc()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(1435)
widget.setFixedHeight(800)
widget.show()
app.exec_()