import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class Urun:
    def __init__(self, adi, stok_miktari, fiyat, icerik):
        self.adi = adi
        self.stok_miktari = stok_miktari
        self.fiyat = fiyat
        self.icerik = icerik

class Siparis:
    def __init__(self, kullanici):
        self.kullanici = kullanici
        self.detaylar = {}

    def siparis_ekle(self, urun, miktar):
        self.detaylar[urun.adi] = miktar

class Stok:
    def __init__(self):
        self.urunler = {}

    def urun_ekle(self, urun):
        self.urunler[urun.adi] = urun

    def stok_guncelle(self, urun_adi, miktar):
        self.urunler[urun_adi].stok_miktari += miktar

    def urun_listele(self):
        return self.urunler

class AnaPencere:
    def __init__(self, pencere):
        self.pencere = pencere
        self.pencere.title("Stok Yönetim Sistemi")
        self.pencere.geometry("800x600")
        self.pencere.configure(bg="#2C2F33")

        self.kullanici = None

        # Veritabanı bağlantısını oluştur
        self.veritabani_baglantisi_olustur()

        self.giris_ekrani()

    def veritabani_baglantisi_olustur(self):
        # Veritabanı bağlantısını oluştur
        self.baglanti = sqlite3.connect("stok.db")
        self.cursor = self.baglanti.cursor()

        # Tabloları oluştur
        self.cursor.execute("CREATE TABLE IF NOT EXISTS kullanıcılar (kullanici_adi TEXT, sifre TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS urunler (adi TEXT, stok_miktari INTEGER, fiyat REAL, icerik TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS siparisler (kullanici TEXT, urun_adi TEXT, miktar INTEGER)")

        self.baglanti.commit()

    def giris_ekrani(self):
        self.giris_frame = tk.Frame(self.pencere, bg="#2C2F33")
        self.giris_frame.pack(pady=100)

        self.label_kullanici_adi = tk.Label(self.giris_frame, text="Kullanıcı Adı:", font=("Arial", 14), bg="#2C2F33", fg="white")
        self.label_kullanici_adi.grid(row=0, column=0, padx=10, pady=5)

        self.kullanici_adi = tk.Entry(self.giris_frame, width=30, font=("Arial", 14))
        self.kullanici_adi.grid(row=0, column=1, padx=10, pady=5)

        self.label_sifre = tk.Label(self.giris_frame, text="Şifre:", font=("Arial", 14), bg="#2C2F33", fg="white")
        self.label_sifre.grid(row=1, column=0, padx=10, pady=5)

        self.sifre = tk.Entry(self.giris_frame, width=30, font=("Arial", 14), show="*")
        self.sifre.grid(row=1, column=1, padx=10, pady=5)

        self.button_giris_yap = tk.Button(self.giris_frame, text="Giriş Yap", command=self.giris_yap, font=("Arial", 14, "bold"), width=15, relief="groove", bd=3, bg="#7289DA", fg="white")
        self.button_giris_yap.grid(row=2, column=0, pady=10)

        self.button_kayit_ol = tk.Button(self.giris_frame, text="Kayıt Ol", command=self.kayit_ol, font=("Arial", 14, "bold"), width=15, relief="groove", bd=3, bg="#7289DA", fg="white")
        self.button_kayit_ol.grid(row=2, column=1, pady=10, padx=5)

        self.kullanim_kilavuzu_buton = tk.Button(self.giris_frame, text="Kullanım Kılavuzu", command=self.kullanim_kilavuzu_goster, font=("Arial", 10, "bold"), relief="flat", bg="#7289DA", fg="white")
        self.kullanim_kilavuzu_buton.grid(row=3, column=0, columnspan=2, pady=10)

    def veritabanina_kullanici_ekle(self, kullanici_adi, sifre):
        # Yeni kullanıcıyı veritabanına ekle
        self.cursor.execute("INSERT INTO kullanıcılar VALUES (?, ?)", (kullanici_adi, sifre))
        self.baglanti.commit()

    def kullanicilari_kontrol_et(self, kullanici_adi, sifre):
        # Kullanıcı adı ve şifreyi veritabanından kontrol et
        self.cursor.execute("SELECT * FROM kullanıcılar WHERE kullanici_adi = ? AND sifre = ?", (kullanici_adi, sifre))
        if self.cursor.fetchall():
            return True
        else:
            return False

    def giris_yap(self):
        # Kullanıcı girişini kontrol et
        kullanici_adi = self.kullanici_adi.get()
        sifre = self.sifre.get()

        # Kullanıcı adı ve şifre kontrolü geçici olarak basit bir şekilde yapılıyor
        if self.kullanicilari_kontrol_et(kullanici_adi, sifre):
            self.giris_frame.destroy()
            self.kullanici = kullanici_adi
            self.ana_pencereyi_olustur()
        else:
            messagebox.showerror("Hata", "Geçersiz kullanıcı adı veya şifre.")

    def kayit_ol(self):
        # Yeni kullanıcı kaydı oluştur
        kullanici_adi = self.kullanici_adi.get()
        sifre = self.sifre.get()

        if not self.kullanicilari_kontrol_et(kullanici_adi, sifre):
            self.veritabanina_kullanici_ekle(kullanici_adi, sifre)
            messagebox.showinfo("Bilgi", "Kullanıcı başarıyla oluşturuldu.")
        else:
            messagebox.showerror("Hata", "Bu kullanıcı zaten mevcut.")

    def ana_pencereyi_olustur(self):
        self.ust_frame = tk.Frame(self.pencere, bg="#2C2F33")
        self.ust_frame.pack(pady=20)

        self.label_baslik = tk.Label(self.ust_frame, text="Ne yapmak istersiniz?", font=("Arial", 16, "bold"), bg="#2C2F33", fg="white")
        self.label_baslik.grid(row=0, column=0, padx=10, pady=5)

        self.button_urun_ekle = tk.Button(self.ust_frame, text="Yeni Ürün Ekle", command=self.urun_ekle_ac, font=("Arial", 12, "bold"), width=15, relief="groove", bd=3, bg="#7289DA", fg="white")
        self.button_urun_ekle.grid(row=1, column=0, padx=10, pady=5)

        self.button_stok_listesi = tk.Button(self.ust_frame, text="Stok Listesi", command=self.stok_listesi_ac, font=("Arial", 12, "bold"), width=15, relief="groove", bd=3, bg="#7289DA", fg="white")
        self.button_stok_listesi.grid(row=1, column=1, padx=10, pady=5)

        self.button_siparis_ver = tk.Button(self.ust_frame, text="Sipariş Ver", command=self.siparis_ver_ac, font=("Arial", 12, "bold"), width=15, relief="groove", bd=3, bg="#7289DA", fg="white")
        self.button_siparis_ver.grid(row=1, column=2, padx=10, pady=5)

        self.button_siparis_listesi = tk.Button(self.ust_frame, text="Sipariş Listesi", command=self.siparis_listesi_ac, font=("Arial", 12, "bold"), width=15, relief="groove", bd=3, bg="#7289DA", fg="white")
        self.button_siparis_listesi.grid(row=1, column=3, padx=10, pady=5)

        self.alt_frame = tk.Frame(self.pencere, bg="#2C2F33")
        self.alt_frame.pack(pady=20)

    def urun_ekle_ac(self):
        self.alt_frame.destroy()
        self.alt_frame = tk.Frame(self.pencere, bg="#2C2F33")
        self.alt_frame.pack(pady=20)

        label_urun_adi = tk.Label(self.alt_frame, text="Ürün Adı:", font=("Arial", 12), bg="#2C2F33", fg="white")
        label_urun_adi.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.entry_urun_adi = tk.Entry(self.alt_frame, width=30, font=("Arial", 12))
        self.entry_urun_adi.grid(row=0, column=1, padx=10, pady=5)

        label_stok_miktari = tk.Label(self.alt_frame, text="Stok Miktarı:", font=("Arial", 12), bg="#2C2F33", fg="white")
        label_stok_miktari.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.entry_stok_miktari = tk.Entry(self.alt_frame, width=30, font=("Arial", 12))
        self.entry_stok_miktari.grid(row=1, column=1, padx=10, pady=5)

        label_urun_fiyati = tk.Label(self.alt_frame, text="Fiyat (TL):", font=("Arial", 12), bg="#2C2F33", fg="white")
        label_urun_fiyati.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.entry_urun_fiyati = tk.Entry(self.alt_frame, width=30, font=("Arial", 12))
        self.entry_urun_fiyati.grid(row=2, column=1, padx=10, pady=5)

        label_urun_icerik = tk.Label(self.alt_frame, text="İçerik:", font=("Arial", 12), bg="#2C2F33", fg="white")
        label_urun_icerik.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.entry_urun_icerik = tk.Text(self.alt_frame, width=30, height=10, font=("Arial", 12))
        self.entry_urun_icerik.grid(row=3, column=1, padx=10, pady=5)

        button_urun_ekle = tk.Button(self.alt_frame, text="Ürün Ekle", command=self.urun_ekle, font=("Arial", 12, "bold"), width=15, relief="groove", bd=3, bg="#7289DA", fg="white")
        button_urun_ekle.grid(row=4, column=0, columnspan=2, pady=10)

    def stok_listesi_ac(self):
        self.alt_frame.destroy()
        self.alt_frame = tk.Frame(self.pencere, bg="#2C2F33")
        self.alt_frame.pack(pady=20)

        self.cursor.execute("SELECT * FROM urunler")
        urunler = self.cursor.fetchall()

        tree = ttk.Treeview(self.alt_frame, columns=("Ürün Adı", "Stok Miktarı", "Fiyat (TL)", "İçerik"), show="headings", height=10)
        tree.heading("Ürün Adı", text="Ürün Adı")
        tree.heading("Stok Miktarı", text="Stok Miktarı")
        tree.heading("Fiyat (TL)", text="Fiyat (TL)")
        tree.heading("İçerik", text="İçerik")
        tree.grid(row=0, column=0, padx=10, pady=5)

        for urun in urunler:
            tree.insert("", "end", values=(urun[0], urun[1], urun[2], urun[3]))

        # Ürün Sil butonunu ekleyin
        button_urun_sil = tk.Button(self.alt_frame, text="Ürünü Sil", command=self.urun_sil, font=("Arial", 12, "bold"), width=15, relief="groove", bd=3, bg="#7289DA", fg="white")
        button_urun_sil.grid(row=1, column=0, columnspan=2, pady=10)

    def urun_sil(self):
        # Seçilen ürünü veritabanından sil
        secilen_urun = self.alt_frame.focus()
        urun_adi = self.alt_frame.item(secilen_urun)["values"][0]
        self.cursor.execute("DELETE FROM urunler WHERE adi = ?", (urun_adi,))
        self.baglanti.commit()
        messagebox.showinfo("Bilgi", "Ürün başarıyla silindi.")

    def siparis_ver_ac(self):
        self.alt_frame.destroy()
        self.alt_frame = tk.Frame(self.pencere, bg="#2C2F33")
        self.alt_frame.pack(pady=20)

        label_siparis_urun_adi = tk.Label(self.alt_frame, text="Ürün Adı:", font=("Arial", 12), bg="#2C2F33", fg="white")
        label_siparis_urun_adi.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.entry_siparis_urun_adi = tk.Entry(self.alt_frame, width=30, font=("Arial", 12))
        self.entry_siparis_urun_adi.grid(row=0, column=1, padx=10, pady=5)

        label_siparis_miktari = tk.Label(self.alt_frame, text="Miktar (Max 20 adet):", font=("Arial", 12), bg="#2C2F33", fg="white")
        label_siparis_miktari.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.entry_siparis_miktari = tk.Entry(self.alt_frame, width=30, font=("Arial", 12))
        self.entry_siparis_miktari.grid(row=1, column=1, padx=10, pady=5)

        button_siparis_ver = tk.Button(self.alt_frame, text="Sipariş Ver", command=self.siparis_ver, font=("Arial", 12, "bold"), width=15, relief="groove", bd=3, bg="#7289DA", fg="white")
        button_siparis_ver.grid(row=2, column=0, columnspan=2, pady=10)

    def siparis_ver(self):
        urun_adi = self.entry_siparis_urun_adi.get()
        miktar = int(self.entry_siparis_miktari.get())

        self.cursor.execute("SELECT stok_miktari FROM urunler WHERE adi = ?", (urun_adi,))
        stok_miktari = self.cursor.fetchone()

        if stok_miktari[0] >= miktar and miktar <= 20:
            self.siparis_olustur(urun_adi, miktar)
        else:
            messagebox.showerror("Hata", "Stokta yeterli ürün bulunmamaktadır.")

    def siparis_olustur(self, urun_adi, miktar):
        siparis = Siparis(self.kullanici)
        siparis.siparis_ekle(Stok().urun_listele()[urun_adi], miktar)

        # Siparişi veritabanına ekle
        self.cursor.execute("INSERT INTO siparisler VALUES (?, ?, ?)", (self.kullanici, urun_adi, miktar))
        self.baglanti.commit()

        messagebox.showinfo("Bilgi", "Siparişiniz alınmıştır.")

    def siparis_listesi_ac(self):
        self.alt_frame.destroy()
        self.alt_frame = tk.Frame(self.pencere, bg="#2C2F33")
        self.alt_frame.pack(pady=20)

        self.cursor.execute("SELECT * FROM siparisler WHERE kullanici = ?", (self.kullanici,))
        siparisler = self.cursor.fetchall()

        tree = ttk.Treeview(self.alt_frame, columns=("Ürün Adı", "Miktar"), show="headings", height=10)
        tree.heading("Ürün Adı", text="Ürün Adı")
        tree.heading("Miktar", text="Miktar")
        tree.grid(row=0, column=0, padx=10, pady=5)

        for siparis in siparisler:
            tree.insert("", "end", values=(siparis[1], siparis[2]))

    def urun_ekle(self):
        adi = self.entry_urun_adi.get()
        stok_miktari = int(self.entry_stok_miktari.get())
        fiyat = float(self.entry_urun_fiyati.get())
        icerik = self.entry_urun_icerik.get("1.0", tk.END)

        yeni_urun = Urun(adi, stok_miktari, fiyat, icerik)

        self.stok_ekle(yeni_urun)

    def stok_ekle(self, urun):
        # Yeni ürünü stok listesine ekle
        Stok().urun_ekle(urun)

        # Yeni ürünü veritabanına ekle
        self.cursor.execute("INSERT INTO urunler VALUES (?, ?, ?, ?)", (urun.adi, urun.stok_miktari, urun.fiyat, urun.icerik))
        self.baglanti.commit()

        messagebox.showinfo("Bilgi", "Ürün başarıyla eklendi.")

    def kullanim_kilavuzu_goster(self):
        kullanım_kılavuzu = """
        Kullanım Kılavuzu:

        1. Giriş yapmak için "Kullanıcı Adı" ve "Şifre" alanlarına bilgilerinizi girin.
        2. "Giriş Yap" butonuna tıklayın.
        3. Ürün eklemek için "Yeni Ürün Ekle" butonuna tıklayın.
        4. Stok listesini görüntülemek için "Stok Listesi" butonuna tıklayın.
        5. Sipariş vermek için "Sipariş Ver" butonuna tıklayın.
        6. Sipariş listenizi görüntülemek için "Sipariş Listesi" butonuna tıklayın.
        """
        messagebox.showinfo("Kullanım Kılavuzu", kullanım_kılavuzu)

root = tk.Tk()
uygulama = AnaPencere(root)
root.mainloop()
