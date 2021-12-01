# IF3152-2021-G09-tuciwir 
Tuciwir adalah aplikasi pemesanan CV Review yang digunakan oleh dua aktor yaitu Tuteers dan Reviewer. 
Tuteers dapat memesan CV Review dengan memilih paket, membayar, dan mengupload CV. Tuteers juga dapat melihat tentang Tuciwir, melihat status pesanan dan mendownload Hasil CV yang sudah direview. Sementara  Reviewer dapat memilih pesanan yang ingin di review, mendownload CV dari pesanan tersebut, dan mengupload Hasil CV yang telah ia review.

## Cara Menjalankan Aplikasi
1. Pindah ke folder src
2. Buka terminal dan ketikkan perintah "python main.py"
3. Aplikasi akan terbuka dan dapat dipakai

## Daftar Modul
* Bukti tampilan layar ada pada folder doc dengan format PNG
1. Manajemen akun -  Stella Ribli (18219027) - login, register, reset password
2. Pilih pesanan - Albertus Agung S (18219066) - pembayaran, pilihanpaket
3. Riwayat pesanan - Azka Alya Ramadhan (18219101) - riwayatdiproses, riwayatselesai
4. Review CV - Zarfa Naida Pratista (18219014) - reviewerall, reviewerpilihan
5. Upload download - Ida Bagus Raditya A.M (18219117) - booking, home, aboutus

## Daftar Tabel Basis Data dan entri
1. booking
(ID_Booking, ID_Paket, ID_Tuteers, cv, tgl_pesan)
2. paket
(ID_Paket, durasi, jumlah_cv, harga)
3. review
(ID_Reviewer, ID_Booking, Hasil_Review, isDone)
4. reviewer
(ID_Reviewer, nama, email, hashedPassword, noHP, tanggalLahir, gender)
5. transaksi
(ID_Transaksi, ID_Booking, Metode_Pembayaran, Bukti_Pembayaran)
6. tuteers
(ID_Tuteers, nama, email, hashedPassword, noHP, tanggalLahir, gender)

## Kontributor
1. Zarfa Naida Pratista (18219014)
2. Stella Ribli (18219027)
3. Albertus Agung S (18219066)
4. Azka Alya Ramadhan (18219101)
5. Ida Bagus Raditya A.M (18219117)