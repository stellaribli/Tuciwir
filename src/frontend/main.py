from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QDialog, QMessageBox, QPushButton, QLabel
from PyQt5.uic import loadUi
import sys
sys.path.insert(0, './src')
import os
import requests

cur_booking_id = 1

class PilihPaket(QDialog):
    def __init__(self):
        super(PilihPaket, self).__init__()
        loadUi('paket.ui', self)
        #Paket 1
        self.PesanPaket1.clicked.connect(lambda: self.pesanpaket(1,1))
        self.jmlCV.setText(str(self.getPaket(1)['jumlah_cv'])+" CV")
        self.jmlHari.setText(str(self.getPaket(1)['durasi'])+" Hari")
        self.harga.setText("Rp "+ str(self.getPaket(1)['harga']))
        #Paket 2
        self.PesanPaket2.clicked.connect(lambda: self.pesanpaket(2,1))
        self.jmlCV_2.setText(str(self.getPaket(2)['jumlah_cv'])+" CV")
        self.jmlHari_2.setText(str(self.getPaket(2)['durasi'])+" Hari")
        self.harga_2.setText("Rp "+ str(self.getPaket(2)['harga']))
        #Paket 3
        self.PesanPaket3.clicked.connect(lambda: self.pesanpaket(3,1))
        self.jmlCV_3.setText(str(self.getPaket(3)['jumlah_cv'])+" CV")
        self.jmlHari_3.setText(str(self.getPaket(3)['durasi'])+" Hari")
        self.harga_3.setText("Rp "+ str(self.getPaket(3)['harga']))
        
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
            self.close()

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

app = QApplication(sys.argv)
window = PilihPaket()
widget=QtWidgets.QStackedWidget()
widget.addWidget(window)
widget.setFixedWidth(900)
widget.setFixedHeight(500)
widget.show()
app.exec_()
