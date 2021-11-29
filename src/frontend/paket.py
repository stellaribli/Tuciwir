from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QDialog, QMessageBox, QPushButton, QLabel
from PyQt5.uic import loadUi
import sys
sys.path.insert(0, './src')
import os
import requests

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
        req = requests.post(f'http://127.0.0.1:8000/create-booking?paket_id={paket_id}&tuteers_id={tuteers_id}')
        if paket_id:
            print("berhasil")
            self.close()
    def getPaket(self, paket_id):
        data = requests.get(f'http://127.0.0.1:8000/paket-by-paket_id?paket_id={paket_id}')
        return data.json()

app = QApplication(sys.argv)
window = PilihPaket()
window.show()
app.exec_()
