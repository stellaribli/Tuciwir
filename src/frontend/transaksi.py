from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QDialog, QMessageBox, QPushButton, QLabel
from PyQt5.uic import loadUi
import sys
sys.path.insert(0, './src')
import os
import requests

cur_booking_id = 1

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
            self.close()

    def getPaketofBooking(self, booking_id):
        data = requests.get(f'http://127.0.0.1:8000/paket-of-booking?booking_id={booking_id}')
        return data.json()
    
    def getBooking(self, booking_id):
        data = requests.get(f'http://127.0.0.1:8000/booking-by-booking_id?booking_id={booking_id}')
        return data.json()

app = QApplication(sys.argv)
window = Pembayaran()
window.show()
app.exec_()

