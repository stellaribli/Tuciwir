import os
import os.path
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QMessageBox, QFileDialog
from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import requests
import urllib
sys.path.insert(0, './src')


cur_booking_id = 1
cur_user_ID = 1
loggedin = False
currentUser = ''
currentName = ''
booking_id = 2


if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(
        QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


# Stella
class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi('login.ui', self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.gotocreate)
        self.loginaccbutton_3.clicked.connect(self.gotoreset)

    def loginfunction(self):
        email = self.email.text()
        password = self.password.text()
        f = {'email': email, 'password': password}
        parsed = (urllib.parse.urlencode(f))
        url = 'https://tuciwir.azurewebsites.net/login?' + parsed
        hasil = requests.get(url)
        x = str(hasil.text)
        global loggedin
        global currentUser
        global currentName
        global cur_user_ID
        if hasil.text == "true":
            loggedin = True
            f = {'em': email}
            parsed = (urllib.parse.urlencode(f))
            url = 'https://tuciwir.azurewebsites.net/ambilDataTuteers?' + parsed
            hasil = requests.get(url)
            currentUser = hasil.json()
            currentName = currentUser['nama']
            cur_user_ID = currentUser['ID_Tuteers']
            print(cur_user_ID)
            widget.setCurrentIndex(4)

            self.email.setText("")
            self.password.setText("")
        else:
            url = 'https://tuciwir.azurewebsites.net/loginadmin?' + parsed
            hasil = requests.get(url)
            if hasil.text == "true":
                loggedin = True
                f = {'em': email}
                parsed = (urllib.parse.urlencode(f))
                url = 'https://tuciwir.azurewebsites.net/ambilDataReviewer?' + parsed
                hasil = requests.get(url)
                currentUser = hasil.json()
                cur_user_ID = currentUser['ID_Reviewer']
                reviewer1 = MainReviewer1()
                widget.addWidget(reviewer1)
                widget.setCurrentWidget(reviewer1)
                self.email.setText("")
                self.password.setText("")
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
        self.email.setText("")
        self.password.setText("")

    def gotoreset(self):
        widget.setCurrentIndex(2)
        self.email.setText("")
        self.password.setText("")


class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc, self).__init__()
        loadUi("createacc.ui", self)
        self.signupbutton.clicked.connect(self.createaccfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.loginaccbutton.clicked.connect(self.gotologin)

    def createaccfunction(self):
        jeniskelamin = ""
        statusEmail = ""
        f = {'email': self.email.text()}
        parsed = (urllib.parse.urlencode(f))
        url = 'https://tuciwir.azurewebsites.net/CheckTuteersAccount?' + parsed
        urlAdmin = 'https://tuciwir.azurewebsites.net/CheckReviewerAccount?' + parsed
        if str(requests.get(url).text) == "true":
            statusEmail = "Tuteers"
        elif str(requests.get(urlAdmin).text) == "true":
            statusEmail = "Admin"
        if not self.Female.isChecked() and not self.Male.isChecked():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Pastikan semua field sudah terisi!')
            msg.exec_()
        else:
            if self.namalengkap.text() == "" or self.email.text() == "" or self.year.text() == "" or self.month.text() == "" or self.date.text() == "" or self.nomorhp.text() == "" or self.password.text() == "" or self.confirmpass.text() == "":
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('Pastikan semua field sudah terisi!')
                msg.exec_()
            elif statusEmail == "Tuteers":
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('Akun anda sudah terdaftar!')
                msg.exec_()
            elif statusEmail == "Admin":
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText(
                    'Akun anda sudah terdaftar sebagai admin!')
                msg.exec_()
            elif self.password.text() != self.confirmpass.text():
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('Input Password Salah!')
                msg.exec_()
            else:
                if self.Female.isChecked():
                    jeniskelamin = "Female"
                elif self.Male.isChecked():
                    jeniskelamin = "Male"
                jen = jeniskelamin
                namalengkap = self.namalengkap.text()
                email = self.email.text()
                year = self.year.text()
                month = self.month.text()
                date = self.date.text()
                nomorhp = self.nomorhp.text()
                password = self.password.text()
                confirmpass = self.confirmpass.text()
                f = {'name': namalengkap, 'email': email, 'password': password, 'reenterpass': confirmpass,
                     'noHP': nomorhp, 'year': year, 'month': month, 'date': date, 'gender': jen}
                parsed = (urllib.parse.urlencode(f))
                url = 'https://tuciwir.azurewebsites.net/registerSQL?' + parsed
                requests.post(url)
                # QLineEdit.clear(self)
                widget.setCurrentIndex(0)
                self.namalengkap.setText("")
                self.email.setText("")
                self.year.setText("")
                self.month.setText("")
                self.date.setText("")
                self.nomorhp.setText("")
                self.password.setText("")
                self.confirmpass.setText("")

    def gotologin(self):
        widget.setCurrentIndex(0)
        self.namalengkap.setText("")
        self.email.setText("")
        self.year.setText("")
        self.month.setText("")
        self.date.setText("")
        self.nomorhp.setText("")
        self.password.setText("")
        self.confirmpass.setText("")


class ResetPassword(QDialog):
    def __init__(self):
        super(ResetPassword, self).__init__()
        loadUi('resetpass.ui', self)
        self.kembali.clicked.connect(self.back)
        self.simpanbutton.clicked.connect(self.resetpass)

    def resetpass(self):
        if self.passbaru.text() == self.passbaru_2.text():
            f = {'email': self.passlama.text(), 'passbaru': self.passbaru.text()}
            parsed = (urllib.parse.urlencode(f))
            url = 'https://tuciwir.azurewebsites.net/resetPasswordSQL/?' + parsed
            requests.get(url)
            widget.setCurrentIndex(0)
            self.passbaru.setText("")
            self.passbaru_2.setText("")
            self.passlama.setText("")

    def back(self):
        widget.setCurrentIndex(0)
        self.passbaru.setText("")
        self.passbaru_2.setText("")
        self.passlama.setText("")


class AboutUs(QDialog):
    def __init__(self):
        super(AboutUs, self).__init__()
        loadUi('aboutus.ui', self)
        self.logoutbutton.clicked.connect(self.goToLogin)
        self.aboutmebutton.clicked.connect(self.gotoaboutus)
        self.layananbutton_4.clicked.connect(self.goToHome)

    def goToLogin(self):
        global loggedin
        loggedin = False
        widget.setCurrentIndex(0)

    # def gotolayanan(self):
    #     widget.setCurrentIndex(#lalaalala)

    def gotoaboutus(self):
        widget.setCurrentIndex(3)

    def goToHome(self):
        widget.setCurrentIndex(4)


# Tugus
class HomeScreen(QMainWindow):
    def __init__(self):
        super(HomeScreen, self).__init__()
        loadUi('homescreen.ui', self)
        self.setWindowTitle('Home Screen')
        self.bookingButton.clicked.connect(self.goToBooking)
        self.statusPesananButton.clicked.connect(self.goToStatus)
        self.aboutmebutton.clicked.connect(self.goToAbout)
        self.logoutbutton.clicked.connect(self.goToLogin)

    def goToBooking(self):
        pesan = PilihPaket()
        widget.addWidget(pesan)
        widget.setCurrentWidget(pesan)

    def goToStatus(self):
        riwayat = PesananTuteers1()
        widget.addWidget(riwayat)
        widget.setCurrentWidget(riwayat)

    def goToAbout(self):
        widget.setCurrentIndex(3)

    def goToLogin(self):
        global loggedin
        loggedin = False
        widget.setCurrentIndex(0)


class UploadCV(QDialog):
    def __init__(self):
        super(UploadCV, self).__init__()
        loadUi("uploadcv.ui", self)
        print("uploadcv " + str(cur_booking_id))
        print("uploadcv " + str(cur_user_ID))
        print("uploadcv " + str(self.getPaketBooking(cur_booking_id)))
        self.setWindowTitle('Upload CV')
        self.uploadButton.clicked.connect(self.uploadCV)
        self.uploadedFile = None
        self.dataPaket = self.getPaketBooking(cur_booking_id)
        self.submitBookingButton.clicked.connect(
            lambda: self.submitBooking(cur_booking_id))
        self.jmlCV.setText(str(self.dataPaket.json()['jumlah_cv']) + "CV")
        self.jmlHari.setText(str(self.dataPaket.json()['durasi']) + " Hari")
        self.rincian.setText("Paket " + str(self.dataPaket.json()
                             ['jumlah_cv']) + " CV " + str(self.dataPaket.json()['durasi']) + " Hari")
        self.harga.setText("Rp" + str(self.dataPaket.json()['harga']))
        self.bookingNumber.setText(
            "#" + str(self.dataPaket.json()['ID_Booking']))
        self.delete_button.hide()
        self.homescreen.hide()
        self.prosesReview.hide()
        self.delete_button.clicked.connect(self.deleteCV)
        self.homescreen.clicked.connect(self.goToHomeScreen)

    def uploadCV(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Upload CV File", "", "PDF Files (*.pdf)")
        if fileName:
            self.uploadedFile = fileName
            # print(self.uploadedFile)
            self.fileName.setText(os.path.basename(fileName))
            self.delete_button.show()
        else:
            print("No file selected")

    def submitBooking(self, booking_id):
        if self.uploadedFile:
            with open(self.uploadedFile, 'rb') as f:
                files = {'uploaded_file': f}
                headers = {'Accept': 'application/json'}
                request = requests.put(
                    f'https://tuciwir.azurewebsites.net/upload-cv?booking_id={booking_id}', files=files, headers=headers)
                # print(request.status_code)
                # print(request.text)
                if (request.text[0] == "CV exists!"):
                    self.remove_CV_from_Booking(booking_id)
                    request = requests.put(
                        f'https://tuciwir.azurewebsites.net/upload-cv?booking_id={booking_id}', files=files, headers=headers)
                    # print(request.status_code)
                    # print(request.text['message'])
                    QMessageBox.about(
                        self, "Success", f"CV untuk booking {booking_id} berhasil di upload!")
                else:
                    QMessageBox.about(
                        self, "Success", f"CV untuk booking {booking_id} berhasil di upload!")
                self.delete_button.hide()
                self.homescreen.show()
                self.uploadButton.hide()
                self.submitBookingButton.hide()
                self.prosesReview.show()
                # self.aboutmebutton.show()
                # self.layananbutton_4.show()
        else:
            QMessageBox.warning(self, "Warning", "Please upload your CV file")

    def getPaketBooking(self, booking_id):
        data = requests.get(
            f'https://tuciwir.azurewebsites.net/paket-of-booking?booking_id={booking_id}')
        return data

    def deleteCV(self):
        self.uploadedFile = None
        self.fileName.setText("No File Uploaded!")
        self.delete_button.hide()

    def remove_CV_from_Booking(self, booking_id):
        req = requests.put(
            f'https://tuciwir.azurewebsites.net/remove-cv-from-booking?booking_id={booking_id}')
        # print(req.text)

    def goToHomeScreen(self):
        widget.setCurrentIndex(4)

    def goToAboutMe(self):
        widget.setCurrentIndex(3)

# Agunk


class PilihPaket(QDialog):
    def __init__(self):
        super(PilihPaket, self).__init__()
        loadUi('paket.ui', self)
        # Paket 1
        self.PesanPaket1.clicked.connect(
            lambda: self.pesanpaket(1, cur_user_ID))
        self.jmlCV.setText(str(self.getPaket(1)['jumlah_cv'])+" CV")
        self.jmlHari.setText(str(self.getPaket(1)['durasi'])+" Hari")
        self.harga.setText("Rp " + str(self.getPaket(1)['harga']))
        # Paket 2
        self.PesanPaket2.clicked.connect(
            lambda: self.pesanpaket(2, cur_user_ID))
        self.jmlCV_2.setText(str(self.getPaket(2)['jumlah_cv'])+" CV")
        self.jmlHari_2.setText(str(self.getPaket(2)['durasi'])+" Hari")
        self.harga_2.setText("Rp " + str(self.getPaket(2)['harga']))
        # Paket 3
        self.PesanPaket3.clicked.connect(
            lambda: self.pesanpaket(3, cur_user_ID))
        self.jmlCV_3.setText(str(self.getPaket(3)['jumlah_cv'])+" CV")
        self.jmlHari_3.setText(str(self.getPaket(3)['durasi'])+" Hari")
        self.harga_3.setText("Rp " + str(self.getPaket(3)['harga']))
        # NAVBAR
        self.layananbutton_4.clicked.connect(lambda: self.goToHomepage())
        self.aboutmebutton.clicked.connect(lambda: self.goToAboutMe())
        self.logoutbutton.clicked.connect(self.goToLogin)

    def pesanpaket(self, paket_id, tuteers_id):
        global cur_booking_id
        req = requests.post(
            f'https://tuciwir.azurewebsites.net/create-booking?paket_id={paket_id}&tuteers_id={tuteers_id}')
        if paket_id:
            print("Berhasil membuat pesanan")

            # update current id booking
            dataBooking = requests.get(
                f'https://tuciwir.azurewebsites.net/booking-by-tuteers_id?tuteers_id={tuteers_id}')
            booking_id = int(dataBooking.json())
            cur_booking_id = booking_id
            print("id Booking saat ini " + str(cur_booking_id))
            pembayaran = Pembayaran()
            widget.addWidget(pembayaran)
            widget.setCurrentWidget(pembayaran)

            # self.close()

    def getPaket(self, paket_id):
        data = requests.get(
            f'https://tuciwir.azurewebsites.net/paket-by-paket_id?paket_id={paket_id}')
        return data.json()

    def getBookingTuteers(self, tuteers_id):
        data = requests.get(
            f'https://tuciwir.azurewebsites.net/booking-by-tuteers_id?tuteers_id={tuteers_id}')
        return data.json()

    def goToHomepage(self):
        widget.setCurrentIndex(4)

    def goToAboutMe(self):
        widget.setCurrentIndex(3)

    def goToLogin(self):
        global loggedin
        loggedin = False
        widget.setCurrentIndex(0)


class Pembayaran(QDialog):
    def __init__(self):
        super(Pembayaran, self).__init__()
        loadUi('transaksi.ui', self)
        print(cur_booking_id)
        print(self.getPaketofBooking(cur_booking_id))
        self.bayar.clicked.connect(lambda: self.pembayaran(cur_booking_id))
        self.cancel.clicked.connect(lambda: self.BatalPesanan(cur_booking_id))
        self.cancel.clicked.connect(self.goToHome)
        self.rincian.setText("Paket " + str(self.getPaketofBooking(cur_booking_id)[
                             'jumlah_cv']) + " CV - " + str(self.getPaketofBooking(cur_booking_id)['durasi']) + " Hari")
        self.harga.setText(
            "Rp " + str(self.getPaketofBooking(cur_booking_id)['harga']))
        self.bookingNumber.setText(
            "#" + str(self.getBooking(cur_booking_id)['ID_Booking']))
        self.logoutbutton.clicked.connect(self.goToLogin)
        self.reloadUi()

    def goToHome(self):
        widget.setCurrentIndex(5)

    def goToStatus(self):
        pass

    def goToAbout(self):
        widget.setCurrentIndex(3)

    def goToLogin(self):
        global loggedin
        loggedin = False
        widget.setCurrentIndex(0)

    def reloadUi(self):
        self.rincian.setText("Paket " + str(self.getPaketofBooking(cur_booking_id)[
                             'jumlah_cv']) + " CV - " + str(self.getPaketofBooking(cur_booking_id)['durasi']) + " Hari")
        self.harga.setText(
            "Rp " + str(self.getPaketofBooking(cur_booking_id)['harga']))
        self.bookingNumber.setText(
            "#" + str(self.getBooking(cur_booking_id)['ID_Booking']))

    def pembayaran(self, booking_id):
        req = requests.post(
            f'https://tuciwir.azurewebsites.net/create-transaksi?booking_id={booking_id}')
        if booking_id:
            print("berhasil melakukan pembayaran untuk No.Booking "+str(booking_id))
            upload = UploadCV()
            widget.addWidget(upload)
            widget.setCurrentWidget(upload)

    def BatalPesanan(self, booking_id):
        req = requests.delete(
            f'https://tuciwir.azurewebsites.net/delete-booking-by-booking_id?booking_id={booking_id}')
        if booking_id:
            print("berhasil membatalkan pesanan dengan No. Booking "+str(booking_id))
            pilihpaket = PilihPaket()
            widget.addWidget(pilihpaket)
            widget.setCurrentIndex(6)

            # self.close()

    def getPaketofBooking(self, booking_id):
        data = requests.get(
            f'https://tuciwir.azurewebsites.net/paket-of-booking?booking_id={booking_id}')
        return data.json()

    def getBooking(self, booking_id):
        data = requests.get(
            f'https://tuciwir.azurewebsites.net/booking-by-booking_id?booking_id={booking_id}')
        return data.json()

# CacCAA


class MainReviewer2(QDialog, QMainWindow):
    def __init__(self):
        super(MainReviewer2, self).__init__()
        loadUi('reviewercus.ui', self)
        self.tabelsemuapesanan.setColumnWidth(0, 220)
        self.tabelsemuapesanan.setColumnWidth(1, 280)
        self.tabelsemuapesanan.setColumnWidth(2, 320)
        self.buttonpesanan.clicked.connect(self.gotomain1)
        self.buttonunduh.clicked.connect(self.download_cv)
        self.buttonunggah.clicked.connect(self.upload_cv_review)
        self.uploadedFile = None
        self.logoutbutton.clicked.connect(self.logout)
        self.load_data()

    def load_data(self):
        headers = {'Accept': 'application/json'}
        req = requests.get(
            f'http://tuciwir.azurewebsites.net/reviewerbookingdia?id_reviewer={cur_user_ID}', headers=headers)
        booking_data = req.json()
        self.tabelsemuapesanan.setRowCount(len(booking_data))
        row = 0
        for booking in (booking_data):
            a = str(booking['isDone'])
            if a == "True":
                a = "Review Selesai"
            else:
                a = "Dalam Review"
            self.tabelsemuapesanan.setItem(
                row, 0, QtWidgets.QTableWidgetItem(str(booking['ID_Booking'])))
            self.tabelsemuapesanan.setItem(
                row, 1, QtWidgets.QTableWidgetItem(str(booking['tgl'])))
            self.tabelsemuapesanan.setItem(
                row, 2, QtWidgets.QTableWidgetItem(a))
            row += 1

    def download_cv(self):
        booking_id = int(self.inputpilih.text())
        header = {'Content-Type': 'application/json'}
        try:
            request = requests.get(
                f'http://tuciwir.azurewebsites.net/download-cv?booking_id={booking_id}', headers=header)
            filename_raw = request.headers['Content-Disposition'].split('filename="')[
                1]
            filename = filename_raw.split('"')[0]
            options = QFileDialog.Options()
            try:
                file = QFileDialog.getSaveFileName(
                    self, "Save File", filename, "PDF Files (*.pdf)", options=options)
                if file[0]:
                    with open(file[0], 'wb') as f:
                        f.write(request.content)
                    QMessageBox.information(
                        self, 'Success', 'CV has been downloaded')
            except:
                QMessageBox.information(
                    self, 'Fail', 'Cannot download CV! File Error!')
        except:
            QMessageBox.information(
                self, 'Fail', 'Cannot download CV! Either CV is not uploaded or internal server error!')

    def upload_cv_review(self):
        booking_id = int(self.inputpilih.text())
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Upload CV File", "", "PDF Files (*.pdf)")
        if fileName:
            self.uploadedFile = fileName
            self.submitReview(booking_id)

    def submitReview(self, booking_id):
        global cur_user_ID
        if self.uploadedFile:
            with open(self.uploadedFile, 'rb') as f:
                files = {'uploaded_file': f}
                headers = {'Accept': 'application/json'}
                request = requests.put(
                    f'https://tuciwir.azurewebsites.net/upload-review?booking_id={booking_id}&reviewer_id={cur_user_ID}', files=files, headers=headers)
                # print(request.status_code)
                # print(request.text)
                if (request.text[0] == "Review exists!"):
                    self.remove_CV_from_Review(booking_id)
                    request = requests.put(
                        f'https://tuciwir.azurewebsites.net/upload-review?booking_id={booking_id}', files=files, headers=headers)
                    # print(request.status_code)
                    # print(request.text['message'])
                    QMessageBox.about(
                        self, "Success", f"CV Review untuk booking {booking_id} berhasil di upload!")
                else:
                    QMessageBox.about(
                        self, "Success", f"CV Review untuk booking {booking_id} berhasil di upload!")
                # self.aboutmebutton.show()
                # self.layananbutton_4.show()
        else:
            QMessageBox.warning(self, "Warning", "Please upload your CV file")

    def remove_CV_from_Review(self, booking_id):
        headers = {'Accept': 'application/json'}
        request = requests.delete(
            f'https://tuciwir.azurewebsites.net/delete-review?booking_id={booking_id}&reviewer_id={cur_user_ID}', headers=headers)
        # print(request.status_code)
        # print(request.text)
        QMessageBox.about(
            self, "Success", f"CV Review untuk booking {booking_id} berhasil di hapus!")

    def gotomain1(self):
        mainreviewer1 = MainReviewer1()
        widget.addWidget(mainreviewer1)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def logout(self):
        global cur_user_ID
        cur_user_ID = 0
        widget.setCurrentIndex(0)


class MainReviewer1(QDialog, QMainWindow):
    def __init__(self):
        super(MainReviewer1, self).__init__()
        loadUi('reviewerall.ui', self)
        self.tabelsemuapesanan.setColumnWidth(0, 220)
        self.tabelsemuapesanan.setColumnWidth(1, 280)
        self.tabelsemuapesanan.setColumnWidth(2, 320)
        self.buttonpesanandia.clicked.connect(self.gotomain2)
        self.buttonpilih.clicked.connect(self.ambilpilihan)
        self.logoutbutton.clicked.connect(self.logout)
        self.load_data1()

    def load_data1(self):
        headers = {'Accept': 'application/json'}
        req = requests.get(
            'http://tuciwir.azurewebsites.net/reviewerbooking', headers=headers)
        booking_data = req.json()
        self.tabelsemuapesanan.setRowCount(len(booking_data))
        row = 0
        a = "Belum Direview"
        for booking in (booking_data):
            self.tabelsemuapesanan.setItem(
                row, 0, QtWidgets.QTableWidgetItem(str(booking['ID_Booking'])))
            self.tabelsemuapesanan.setItem(
                row, 1, QtWidgets.QTableWidgetItem(str(booking['tgl'])))
            self.tabelsemuapesanan.setItem(
                row, 2, QtWidgets.QTableWidgetItem(a))
            row += 1

    def ambilpilihan(self):
        global cur_user_ID
        id_booking = self.inputpilih.text()
        masukan = {'id_reviewer': cur_user_ID, 'id_booking': id_booking}
        parsed = (urllib.parse.urlencode(masukan))
        url = 'http://tuciwir.azurewebsites.net/reviewerpilihbooking?' + parsed
        requests.post(url)
        QMessageBox.information(self, 'Success', 'Booking has been chosen')

    def gotomain2(self):
        mainreviewer2 = MainReviewer2()
        widget.addWidget(mainreviewer2)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def logout(self):
        global cur_user_ID
        cur_user_ID = 0
        widget.setCurrentIndex(0)


# AZKA

class PesananTuteers2(QDialog, QMainWindow):
    def __init__(self):
        super(PesananTuteers2, self).__init__()
        loadUi('riwayatselesainew.ui', self)
        self.tabelsemuapesanan.setColumnWidth(0, 180)
        self.tabelsemuapesanan.setColumnWidth(1, 280)
        self.tabelsemuapesanan.setColumnWidth(2, 280)
        self.buttonpesanan.clicked.connect(self.gotomain1)
        self.buttonunduh.clicked.connect(self.download_cv_review)
        self.load_data()
        self.logoutbutton.clicked.connect(self.goToLogin)
        self.layananbutton_4.clicked.connect(self.goToHome)
        self.aboutmebutton.clicked.connect(self.goToAboutMe)

    def load_data(self):
        global cur_user_ID
        headers = {'Accept': 'application/json'}
        req = requests.get(
            f'http://tuciwir.azurewebsites.net/reviewdone?tuteers_id={cur_user_ID}', headers=headers)
        booking_data = req.json()
        self.tabelsemuapesanan.setRowCount(len(booking_data))
        row = 0
        for booking in (booking_data):
            a = str(booking['isDone'])
            if a == "True":
                a = "Review Selesai"
            else:
                a = "Dalam Review"
            self.tabelsemuapesanan.setItem(
                row, 0, QtWidgets.QTableWidgetItem(str(booking['ID_Booking'])))
            self.tabelsemuapesanan.setItem(
                row, 1, QtWidgets.QTableWidgetItem(str(booking['tgl'])))
            self.tabelsemuapesanan.setItem(
                row, 2, QtWidgets.QTableWidgetItem(a))
            row += 1

    def download_cv_review(self):
        booking_id = int(self.inputpilih.text())
        header = {'Content-Type': 'application/json'}
        try:
            request = requests.get(
                f'http://tuciwir.azurewebsites.net/download-cv-review?booking_id={booking_id}', headers=header)
            filename_raw = request.headers['Content-Disposition'].split('filename="')[1]
            filename = filename_raw.split('"')[0]
            options = QFileDialog.Options()
            try:
                file = QFileDialog.getSaveFileName(
                    self, "Save File", filename, "PDF Files (*.pdf)", options=options)
                if file[0]:
                    with open(file[0], 'wb') as f:
                        f.write(request.content)
                    QMessageBox.information(
                        self, 'Success', 'CV has been downloaded')
            except:
                QMessageBox.information(
                    self, 'Fail', 'Cannot download CV! File Error!')
        except Exception as e:
            print(e)
            QMessageBox.information(
                self, 'Fail', 'Cannot download Review! Either Review is not uploaded or internal server error!')

    def upload_cv_review(self):
        booking_id = int(self.inputpilih.text())
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Upload CV File", "", "PDF Files (*.pdf)")
        if fileName:
            self.uploadedFile = fileName
            QMessageBox.information(self, 'Success', 'CV has been uploaded')
            self.submitReview(booking_id)

    def gotomain1(self):
        pesanan1 = PesananTuteers1()
        widget.addWidget(pesanan1)
        widget.setCurrentWidget(pesanan1)

    def goToLogin(self):
        widget.setCurrentIndex(0)

    def goToHome(self):
        widget.setCurrentIndex(4)

    def goToAboutMe(self):
        widget.setCurrentIndex(3)


class PesananTuteers1(QDialog, QMainWindow):
    def __init__(self):
        super(PesananTuteers1, self).__init__()
        loadUi('riwayatdiprosesnew.ui', self)
        self.tabelsemuapesanan.setColumnWidth(0, 180)
        self.tabelsemuapesanan.setColumnWidth(1, 280)
        self.tabelsemuapesanan.setColumnWidth(2, 280)
        self.buttonpesanandia.clicked.connect(self.gotomain2)
        self.buttonunduh.clicked.connect(self.download_cv)
        self.logoutbutton.clicked.connect(self.goToLogin)
        self.layananbutton_4.clicked.connect(self.goToHome)
        self.aboutmebutton.clicked.connect(self.goToAboutMe)
        self.load_data1()

    def load_data1(self):
        headers = {'Accept': 'application/json'}
        req = requests.get(
            f'http://tuciwir.azurewebsites.net/reviewdiproses?tuteers_id={cur_user_ID}', headers=headers)
        booking_data = req.json()
        self.tabelsemuapesanan.setRowCount(len(booking_data))
        row = 0
        for booking in (booking_data):
            self.tabelsemuapesanan.setItem(
                row, 0, QtWidgets.QTableWidgetItem(str(booking['ID_Booking'])))
            self.tabelsemuapesanan.setItem(
                row, 1, QtWidgets.QTableWidgetItem(str(booking['tgl'])))
            self.tabelsemuapesanan.setItem(
                row, 2, QtWidgets.QTableWidgetItem(str(booking['status'])))
            row += 1

    def download_cv(self):
        booking_id = int(self.inputpilih.text())
        header = {'Content-Type': 'application/json'}
        try:
            request = requests.get(
                f'http://tuciwir.azurewebsites.net/download-cv?booking_id={booking_id}', headers=header)
            filename_raw = request.headers['Content-Disposition'].split('filename="')[
                1]
            filename = filename_raw.split('"')[0]
            options = QFileDialog.Options()
            file = QFileDialog.getSaveFileName(
                self, "Save File", filename, "PDF Files (*.pdf)", options=options)
            if file[0]:
                with open(file[0], 'wb') as f:
                    f.write(request.content)
                QMessageBox.information(
                    self, 'Success', 'CV has been downloaded')
        except requests.exceptions.ConnectionError as r:
            r.status_code = "Connection refused"
            print(r.status_code)

    def goToHome(self):
        widget.setCurrentIndex(4)

    def goToAboutMe(self):
        widget.setCurrentIndex(3)

    def goToLogin(self):
        widget.setCurrentIndex(0)

    def gotomain2(self):
        pesanan2 = PesananTuteers2()
        widget.addWidget(pesanan2)
        widget.setCurrentWidget(pesanan2)


app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
widget.addWidget(Login())  # Index jadi 0
widget.addWidget(CreateAcc())  # Index jadi 1
widget.addWidget(ResetPassword())  # Index jadi 2
widget.addWidget(AboutUs())  # Index jadi 3
widget.addWidget(HomeScreen())  # Index jadi 4
pilihPaket = PilihPaket()
widget.addWidget(pilihPaket)
# widget.addWidget(MainReviewer1()) #Index jadi 5
# widget.addWidget(MainReviewer2()) #Index jadi 6
widget.setCurrentIndex(0)
widget.setFixedWidth(1280)
widget.setFixedHeight(720)
widget.show()
app.exec_()
