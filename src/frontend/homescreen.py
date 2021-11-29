from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QDialog, QMainWindow, QMessageBox, QPushButton, QLabel
from PyQt5.uic import loadUi
import sys
sys.path.insert(0, './src')
import os
import requests

class HomeScreen(QMainWindow):
    def __init__(self):
        super(HomeScreen, self).__init__()
        loadUi('homescreen.ui', self)
        self.setWindowTitle('Home Screen')
        self.setWindowIcon(QtGui.QIcon('src/frontend/images/logo askel.png'))
        self.bookingButton.clicked.connect(self.goToBooking)
        self.statusPesananButton.clicked.connect(self.goToStatus)
    

    def goToBooking(self):
        QMessageBox.about(self, "Info", "Go to booking")
    
    def goToStatus(self):
        QMessageBox.about(self, "Info", "Go to status")
    


app = QApplication(sys.argv)
window = HomeScreen()
window.show()
app.exec_()