import mysql.connector
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QDateTimeEdit
from PyQt5.QtCore import QTimer, QDateTime
from mysql.connector import Error

class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.PB_Login.clicked.connect(self.CariData)
        self.PB_SignUp.clicked.connect(self.gotosignup)
        self.PB_ganti.hide()
        self.PB_ganti.clicked.connect(self.lupa_password)
    
    def gotosignup(self):
        signup = SignUp()
        widget.addWidget(signup)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Koneksi(self):
        koneksi = mysql.connector.connect(host='localhost', user='root', password='', database='pas_dbms')
        cur = koneksi.cursor()
        return cur, koneksi

    def CariData(self):
        statemenSQL = "SELECT nama_admin, password FROM admin WHERE nama_admin LIKE '" + self.LEName.text() + "' AND password LIKE '" + self.LEPassword.text() + "'"
        try:
            cur, koneksi = self.Koneksi()
            cur.execute(statemenSQL)
            data = cur.fetchone()
            if data == None :
                QMessageBox.critical(self,"Error", "Maaf, Username atau Password salah")
                self.PB_ganti.show()
            else:
                self.gotomenu()
        except Error as e:
            QMessageBox.critical(self,"Error", "Error mengakses data")
        finally:
            koneksi.close()
    
    def label(self):
        nama = self.LEName.text()
        print (nama)
        
    def gotomenu(self):
        menu = Menu()
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def lupa_password(self):
        Lupa = LupaPassword()
        widget.addWidget(Lupa)
        widget.setCurrentIndex(widget.currentIndex() + 1) 

class LupaPassword(QDialog):
    def __init__(self):
        super(LupaPassword, self ).__init__()
        loadUi("ganti_password.ui", self)
        self.PB_Ok.clicked.connect(self.username)
        self.PB_ganti.clicked.connect(self.ganti)
        self.PB_login.clicked.connect(self.gotologin)
    def Koneksi(self):
        koneksi = mysql.connector.connect(host='localhost', user='root',password='', database='pas_dbms')
        cur = koneksi.cursor()
        return cur, koneksi
 
    def username(self):
        no_telp = self.LETelp.text()
        statemenSQL = "SELECT nama_admin FROM admin WHERE no_telp = %s"
        try:
            cur, koneksi = self.Koneksi()
            cur.execute(statemenSQL, (no_telp,))
            baris = cur.fetchone()
            if baris is None:
                QMessageBox.critical(self, "Error", "Nomor telepon tidak valid")
                self.LEUsername.clear()
            else:
                nama = baris[0]
                self.LEUsername.setText(str(nama))
        finally:
            koneksi.close()
  
    def ganti(self):
        no_telp = self.LETelp.text()
        new = self.LE_PassBaru.text()
        try:
            cur, koneksi = self.Koneksi()
            update_query = f"UPDATE admin SET password = '{new}' WHERE no_telp = '{no_telp}'"
            cur.execute(update_query)
            koneksi.commit()
        except:
            QMessageBox.critical(self, "Gagal", "Gagal mengganti password")
        else:
            QMessageBox.information(self, "Berhasil", "Password Telah diganti")
        finally:
            koneksi.close()

    def gotologin(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)    

class SignUp(QDialog):
    def __init__(self):
        super(SignUp, self ).__init__()
        loadUi("Registrasi.ui", self)
        self.PB_Buatakun.clicked.connect(self.BuatData)
        self.PB_Kembalilogin.clicked.connect(self.gotologin)
    
    def gotologin(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)    
        
    def Koneksi(self):
        koneksi = mysql.connector.connect(host='localhost', user='root',password='', database='pas_dbms')
        cur = koneksi.cursor()
        return cur, koneksi

    def BuatData(self):
        id_admin = self.LEID.text()
        password = self.LEPassword.text()
        nama_admin = self.LEName.text()
        no_telp = self.LENo_Telp.text()
        statemenSQL = f"INSERT INTO admin (id_admin, password, nama_admin, no_telp) VALUES ('{id_admin}', '{password}', '{nama_admin}', '{no_telp}')"
        try:
            cur, koneksi = self.Koneksi()
            cur.execute(statemenSQL)
            koneksi.commit()
            QMessageBox.information(self,"Berhasil","User Berhasil Ditambahkan")
        except mysql.connector.Error as e:
            QMessageBox.critical(self,"Error", "ID Sudah Tidak " )
        finally:
            cur.close()
            koneksi.close()  

class Menu(QDialog):
    def __init__(self):
        super(Menu, self).__init__()
        loadUi("MenuUtama.ui", self)
        self.PB_Tambahkan.clicked.connect(self.TambahkanData)
        self.PB_LogOut.clicked.connect(self.gotologin)
        self.PB_LogOut2.clicked.connect(self.gotologin)
        self.PB_OK.clicked.connect(self.OK)
        self.PB_Masukkan.clicked.connect(self.masukkan)
        self.PB_Konfirmasi.clicked.connect(self.Kembalian)
        self.PB_CetakStruk.clicked.connect(self.CetakStruk)
        self.PB_TambahStok.clicked.connect(self.TambahStok)
        self.PB_HapusBarang.clicked.connect(self.HapusBarang)
        self.refresh()
        self.refresh2
        self.bersihkan()
        self.update_datetime()
        self.user()

    def Koneksi(self):
        koneksi = mysql.connector.connect(host='localhost', user='root',password='', database='pas_dbms')
        cur = koneksi.cursor()
        return cur, koneksi
    
    def HapusBarang(self):
        id_barang = self.LE_ID_Barang.text()
        statementSQL = f"DELETE FROM barang WHERE id_barang = '{id_barang}';"
        try:
            cur, koneksi = self.Koneksi()
            cur.execute(statementSQL)
            koneksi.commit()  
        except Exception as e:
            QMessageBox.critical(self, "Gagal", f"Gagal menghapus barang")
        else:
            QMessageBox.information(self, "Berhasil", "Barang telah dihapus")
            self.refresh()
            self.LE_ID_Barang.clear()
        finally:
            koneksi.close()


    def TambahStok(self):
        id = self.LE_ID_Barang.text()
        stok = self.LE_StokBarang.text()
        try:
            cur, koneksi = self.Koneksi()
            update_query = f"UPDATE barang SET stok_barang = stok_barang + {stok} WHERE id_barang = {id}"
            cur.execute(update_query)
            koneksi.commit()
        except:
            QMessageBox.critical(self, "Gagal", "Gagal menambah stok barang")
        else:
            QMessageBox.information(self, "Berhasil", "Stok Barang telah ditambahkan")
            self.refresh()
            self.LE_ID_Barang.clear()
        finally:
            koneksi.close()

    def user(self):
        login_instance = widget.currentWidget()
        username = login_instance.LEName.text()
        self.L_Nama.setText(f"Halo {username}")

    def OK(self):
        self.nama()
        self.harga()

    def gotologin(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def TambahkanData(self):
        id_barang = self.LE_ID_Barang.text()
        nama_barang  = self.LE_NamaBarang.text()
        stok_barang = self.LE_StokBarang.text()
        harga_barang = self.LE_HargaBarang.text()
        
        statemenSQL = f"INSERT INTO barang (id_barang, nama_barang, stok_barang, harga_barang) VALUES ({id_barang}, '{nama_barang}', {stok_barang}, {harga_barang})"
        try:
            cur, koneksi =   self.Koneksi()
            cur.execute(statemenSQL)
            koneksi.commit()
            QMessageBox.information(self,"Berhasil","Data Berhasil Ditambahkan")
            self.refresh()
            self.LE_ID_Barang.clear()
            self.LE_NamaBarang.clear()
            self.LE_StokBarang.clear()
            self.LE_HargaBarang.clear()
        except mysql.connector.Error:
            QMessageBox.critical(self,"Error", "Error mengakses data " )
        finally:
            cur.close()
            koneksi.close()

    def refresh(self):
        statemenSQL = "SELECT * FROM barang"
        try :
            cur, koneksi = self.Koneksi()
            cur.execute(statemenSQL)
            result = cur.fetchall()
            self.T_Barang.clearContents()
            self.T_Barang.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.T_Barang.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.T_Barang.setItem(row_number,column_number, QtWidgets.QTableWidgetItem(str(data)))
        except mysql.connector.Error :
            QMessageBox.critical(self,"Error", "Error saat mengakses tabel  " )
        finally:
            koneksi.close()

    def harga(self):
        id_barang = self.LE_IDBarang.text()
        statemenSQL = f"SELECT harga_barang FROM barang WHERE id_barang LIKE '{id_barang}'"
        try:
            cur, koneksi = self.Koneksi()
            cur.execute(statemenSQL)
            baris = cur.fetchone()
            if baris is None:
                QMessageBox.critical(self, "Error", "Tidak ditemukan harga dengan Id Produk ini")
                self.LE_Harga.clear()
            else:
                harga = baris[0]
                self.LE_Harga.setText(str(harga))
        finally:
            koneksi.close()

    def nama(self):
        id_barang = self.LE_IDBarang.text()
        statemenSQL = f"SELECT nama_barang FROM barang WHERE id_barang LIKE '{id_barang}'"
        try:
            cur, koneksi = self.Koneksi()
            cur.execute(statemenSQL)
            baris = cur.fetchone()
            if baris is None:
                QMessageBox.critical(self, "Error", "Tidak ditemukan harga dengan Id Produk ini")
                self.LE_Nama_Barang.clear()
            else:
                nama = baris[0]
                self.LE_Nama_Barang.setText(str(nama))
        finally:
            koneksi.close()

    def masukkan(self):
        nama_barang = self.LE_Nama_Barang.text()
        harga = float(self.LE_Harga.text())
        jml_beli =float(self.LE_Jumlah.text())
        jml_harga = harga * jml_beli
        statemenSQL = f"INSERT INTO pembelian (nama_barang, harga, jml_beli, jml_harga) VALUES ('{nama_barang}', {harga}, {jml_beli}, {jml_harga})"
        try:
            cur, koneksi = self.Koneksi()
            cur.execute(statemenSQL)
            self.LE_Bayar.clear()
            koneksi.commit()
            self.refresh2()
            self.total()
            self.JualProduk()
        except mysql.connector.Error as e:
            QMessageBox.critical(self,"Error", "Error mengakses data: " )
        finally:
            cur.close()
            koneksi.close()

    def refresh2(self):
        statemenSQL = "SELECT * FROM pembelian"
        try:
            cur, koneksi = self.Koneksi()
            cur.execute(statemenSQL)
            result = cur.fetchall()
            self.T_Pembelian.clearContents()
            self.T_Pembelian.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.T_Pembelian.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.T_Pembelian.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        finally:
            koneksi.close()

    def total(self):
        statemenSQL = f"SELECT sum(jml_harga) as total FROM pembelian"
        try:
            cur, koneksi = self.Koneksi()
            cur.execute(statemenSQL)
            baris = cur.fetchone()
            if baris is None:
                self.LE_Total.clear()
            else:
                jml_harga= baris[0]
                self.LE_Total.setText(str(jml_harga))
        finally:
            koneksi.close()
 

    def Kembalian(self):
        if len(self.LE_Bayar.text()) !=0:
            bayar=float(self.LE_Bayar.text())
        else:
            bayar=0
        total=float(self.LE_Total.text())
        kembalian=bayar-total
        if kembalian >= 0:
            self.LE_Kembalian.setText(str (kembalian))
        else:
            QMessageBox.critical(self, "Error", "Uang anda tidak cukup")

    def bersihkan(self):
        statementSQL = "DELETE FROM pembelian"
        try:
            cur, koneksi = self.Koneksi()
            cur.execute(statementSQL)
            koneksi.commit() 
            self.refresh2()
        finally:
            koneksi.close()

    def JualProduk(self):
        id = self.LE_IDBarang.text()
        jumlah = int(self.LE_Jumlah.text())
        cur, koneksi = self.Koneksi()
        query = f"SELECT stok_barang FROM barang WHERE id_barang like {id}"
        cur.execute(query)
        result = cur.fetchone()
        if result:
            stok = result[0]
            if stok >= jumlah:
                stokBaru = stok - jumlah
                update_query = "UPDATE barang SET stok_barang = %s WHERE id_barang = %s"
                cur.execute(update_query, (stokBaru, id))
                koneksi.commit()
                self.refresh()
        koneksi.close()  

    def Tanggal(self):
        self.dateTimeEdit = QDateTimeEdit()
        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.dateTimeEdit.setDisplayFormat("dd/MM/yyyy hh:mm:ss")

        timer = QTimer(self)
        timer.timeout.connect(self.update_datetime)
        timer.start(1000)

    def update_datetime(self):
        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())

    def Tabel_Struk(self):
        statemenSQL = "SELECT * FROM pembelian"
        try:
            cur, koneksi = self.Koneksi()
            cur.execute(statemenSQL)
            result = cur.fetchall()
            self.T_Pembelian.clearContents()
            self.T_Pembelian.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.T_Pembelian.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.T_Pembelian.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        finally:
            koneksi.close()

    def CetakStruk(self):
        struk = Struk()
        widget.addWidget(struk)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        self.refresh()
        self.refresh2()
        self.bersihkan()
        

class Struk(QDialog):
    def __init__(self):
        super(Struk, self).__init__()
        loadUi("Struk.ui", self)
        self.PB_Kembali.clicked.connect(self.kembali)
        self.LEName.hide()
        self.tabel_struk()
        self.cetak()

    def Koneksi(self):
        koneksi = mysql.connector.connect(host='localhost', user='root', password='', database='pas_dbms')
        cur = koneksi.cursor()
        return cur, koneksi 

    def tabel_struk(self):
        statemenSQL = "SELECT * FROM pembelian"
        try:
            cur, koneksi = self.Koneksi()
            cur.execute(statemenSQL)
            result = cur.fetchall()
            self.T_Struk.clearContents()
            self.T_Struk.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.T_Struk.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.T_Struk.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        finally:
            koneksi.close()

    def cetak(self):
        menu_instance = widget.currentWidget()
        tanggal = menu_instance.dateTimeEdit.text()
        total = menu_instance.LE_Total.text()
        bayar = menu_instance.LE_Bayar.text()
        kembalian = menu_instance.LE_Kembalian.text()

        self.L_Tanggal.setText(tanggal)
        self.L_Total.setText(total)
        self.L_Dibayar.setText(bayar)
        self.L_Kembalian.setText(kembalian)

    def kembali(self):
        login_instance = widget.currentWidget()
        Name = login_instance.LEName.text()
        self.LEName.setText(Name)
        kembali = Menu()
        widget.addWidget(kembali)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
login = Login()
widget.addWidget(login)
widget.setFixedHeight(681)
widget.setFixedWidth(971)
widget.show()
sys.exit(app.exec_())  