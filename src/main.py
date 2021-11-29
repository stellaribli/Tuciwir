import sys
from PyQt5.QtWidgets import QFileDialog, QPushButton, QDialog, QApplication, QWidget, QLabel, QMainWindow, QMessageBox, QCheckBox, QLineEdit
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from typing import List
import requests
import urllib
import json
from PyQt5 import QtCore, QtGui, QtWidgets
import PyPDF2
import os
from PyQt5.QtWidgets import QApplication, QFileDialog, QDialog, QMessageBox, QPushButton, QLabel
sys.path.insert(0, './src')
import os
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

cur_booking_id = 23
cur_user_ID = 26
booking_id = 23

#Homepage
class HomeScreen(QMainWindow):
    def __init__(self):
        super(HomeScreen, self).__init__()
        loadUi('homescreen.ui', self)
        self.setWindowTitle('Home Screen')
        self.setWindowIcon(QtGui.QIcon('src/frontend/images/logo askel.png'))
        self.bookingButton.clicked.connect(self.goToBooking)
        self.statusPesananButton.clicked.connect(self.goToStatus)

    def goToBooking(self):
        #QMessageBox.about(self, "Info", "Go to booking")
        pilihpaket = PilihPaket()
        widget.addWidget(pilihpaket)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def goToStatus(self):
        QMessageBox.about(self, "Info", "Go to status")

#Pemesanan
class PilihPaket(QDialog):
    def __init__(self):
        super(PilihPaket, self).__init__()
        loadUi('paket.ui', self)
        self.kembali.clicked.connect(lambda: self.back())
        #Paket 1
        self.PesanPaket1.clicked.connect(lambda: self.pesanpaket(1,cur_user_ID))
        self.jmlCV.setText(str(self.getPaket(1)['jumlah_cv'])+" CV")
        self.jmlHari.setText(str(self.getPaket(1)['durasi'])+" Hari")
        self.harga.setText("Rp "+ str(self.getPaket(1)['harga']))
        #Paket 2
        self.PesanPaket2.clicked.connect(lambda: self.pesanpaket(2,cur_user_ID))
        self.jmlCV_2.setText(str(self.getPaket(2)['jumlah_cv'])+" CV")
        self.jmlHari_2.setText(str(self.getPaket(2)['durasi'])+" Hari")
        self.harga_2.setText("Rp "+ str(self.getPaket(2)['harga']))
        #Paket 3
        self.PesanPaket3.clicked.connect(lambda: self.pesanpaket(3,cur_user_ID))
        self.jmlCV_3.setText(str(self.getPaket(3)['jumlah_cv'])+" CV")
        self.jmlHari_3.setText(str(self.getPaket(3)['durasi'])+" Hari")
        self.harga_3.setText("Rp "+ str(self.getPaket(3)['harga']))
        
    def back(self):
        widget.setCurrentIndex(widget.currentIndex()-1)
        pilihpaket = PilihPaket()
        widget.addWidget(pilihpaket)

    def pesanpaket(self, paket_id, tuteers_id):
        global cur_booking_id
        req = requests.post(f'http://127.0.0.1:8000/create-booking?paket_id={paket_id}&tuteers_id={tuteers_id}')
        if paket_id:
            print("Berhasil membuat pesanan")

            #update current id booking
            dataBooking = requests.get(f'http://127.0.0.1:8000/booking-by-tuteers_id?tuteers_id={tuteers_id}')
            booking_id = int(dataBooking.json())
            cur_booking_id = booking_id
            print("id Booking saat ini " + str(cur_booking_id))

            #go to pembayaran
            pembayaran=Pembayaran()
            widget.addWidget(pembayaran)
            widget.setCurrentIndex(widget.currentIndex()+1)
            #self.close()

    def getPaket(self, paket_id):
        data = requests.get(f'http://127.0.0.1:8000/paket-by-paket_id?paket_id={paket_id}')
        return data.json()
    
    def getBookingTuteers(self, tuteers_id):
        data = requests.get(f'http://127.0.0.1:8000/booking-by-tuteers_id?tuteers_id={tuteers_id}')
        return data.json()

class Pembayaran(QDialog):
    def __init__(self):
        super(Pembayaran, self).__init__()
        loadUi('transaksi.ui', self)
        self.bayar.clicked.connect(lambda: self.pembayaran(cur_booking_id))
        self.cancel.clicked.connect(lambda: self.BatalPesanan(cur_booking_id))
        self.rincian.setText("Paket " + str(self.getPaketofBooking(cur_booking_id)['jumlah_cv']) + " CV - " + str(self.getPaketofBooking(cur_booking_id)['durasi']) + " Hari")
        self.harga.setText("Rp "+ str(self.getPaketofBooking(cur_booking_id)['harga']))
        self.bookingNumber.setText(str(self.getBooking(cur_booking_id)['ID_Booking']))

    def pembayaran(self,booking_id):
        req = requests.post(f'http://127.0.0.1:8000/create-transaksi?booking_id={booking_id}')
        if booking_id:
            print("berhasil melakukan pembayaran untuk No.Booking "+str(booking_id))
            uploadcv = UploadCV()
            widget.addWidget(uploadcv)
            widget.setCurrentIndex(widget.currentIndex()+1)
            #self.close()

    def BatalPesanan(self, booking_id):
        req = requests.delete(f'http://127.0.0.1:8000/delete-booking-by-booking_id?booking_id={booking_id}')
        if booking_id:
            print("berhasil membatalkan pesanan dengan No. Booking "+str(booking_id))
            pilihpaket = PilihPaket()
            widget.addWidget(pilihpaket)
            widget.setCurrentIndex(widget.currentIndex()+1)
            #self.close()

    def getPaketofBooking(self, booking_id):
        data = requests.get(f'http://127.0.0.1:8000/paket-of-booking?booking_id={booking_id}')
        return data.json()
    
    def getBooking(self, booking_id):
        data = requests.get(f'http://127.0.0.1:8000/booking-by-booking_id?booking_id={booking_id}')
        return data.json()

#upload cv
class UploadCV(QDialog):
    def __init__(self):
        super(UploadCV, self).__init__()
        loadUi("uploadcv.ui", self)
        self.setWindowTitle('Upload CV')
        self.uploadButton.clicked.connect(self.uploadCV)
        self.uploadedFile = None
        self.dataPaket = self.getPaketBooking(booking_id)
        self.submitBookingButton.clicked.connect(lambda: self.submitBooking(booking_id))
        self.jmlCV.setText(str(self.dataPaket.json()['jumlah_cv']) + "CV")
        self.jmlHari.setText(str(self.dataPaket.json()['durasi']) + " Hari")
        self.rincian.setText("Paket " + str(self.dataPaket.json()['jumlah_cv']) + " CV " + str(self.dataPaket.json()['durasi']) + " Hari")
        self.harga.setText("Rp" + str(self.dataPaket.json()['harga']))
        self.bookingNumber.setText("#" + str(self.dataPaket.json()['ID_Booking']))
        self.delete_button.hide()
        self.homescreen.hide()
        self.prosesReview.hide()
        self.delete_button.clicked.connect(self.deleteCV)
        self.homescreen.clicked.connect(self.goToHomeScreen)
        self.gambar.setPixmap(QtGui.QPixmap("src/frontend/images/cv.png"))
        self.gambar.show()

    def uploadCV(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Upload CV File", "", "PDF Files (*.pdf)")
        if fileName:
            self.uploadedFile = fileName
            print(self.uploadedFile)
            self.fileName.setText(os.path.basename(fileName))
            self.delete_button.show()

        else:
            print("No file selected")
        
    def submitBooking(self, booking_id):
        if self.uploadedFile:
            with open(self.uploadedFile, 'rb') as f:
                files = {'uploaded_file': f}
                headers = {'Accept': 'application/json'}
                request = requests.put(f'http://127.0.0.1:8000/upload-cv?booking_id={booking_id}', files=files, headers=headers)
                print(request.status_code)
                print(request.text)
                if (request.text[0] == "CV exists!"):
                    self.remove_CV_from_Booking(booking_id)
                    request = requests.put(f'http://127.0.0.1:8000/upload-cv?booking_id={booking_id}', files=files, headers=headers)
                    print(request.status_code)
                    print(request.text['message'])
                    QMessageBox.about(self, "Success", f"CV untuk booking {booking_id} berhasil di upload!")
                if (request.status_code == 200):
                    QMessageBox.about(self, "Success", f"CV untuk booking {booking_id} berhasil di upload!")
                self.delete_button.hide()
                self.homescreen.show()
                self.uploadButton.hide()
                self.submitBookingButton.hide()
                self.prosesReview.show()

        else:
            QMessageBox.warning(self, "Warning", "Please upload your CV file")
    
    def getPaketBooking(self, booking_id):
        data = requests.get(f'http://127.0.0.1:8000/paket-of-booking?booking_id={booking_id}')
        print(data.text)
        return data
    
    def deleteCV(self):
        self.uploadedFile = None
        self.fileName.setText("No File Uploaded!")
        self.delete_button.hide()

    def remove_CV_from_Booking(self, booking_id):
        req = requests.put(f'http://127.0.0.1:8000/remove-cv-from-booking?booking_id={booking_id}')
        print(req.text)

    def goToHomeScreen(self):
        self.close()


app = QApplication(sys.argv)
window = HomeScreen()
widget=QtWidgets.QStackedWidget()
widget.addWidget(window)
widget.setFixedWidth(1000)
widget.setFixedHeight(600)
widget.show()
app.exec_()
