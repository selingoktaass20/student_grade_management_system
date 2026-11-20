import sqlite3

# VERİTABANI BAĞLANTISI

baglanti = sqlite3.connect("ogrenci_sistemi.db")
cursor = baglanti.cursor()

# TABLOLARI OLUŞTUR

cursor.execute("""
CREATE TABLE IF NOT EXISTS ogrenciler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ogrenci_no INTEGER UNIQUE NOT NULL,
    ad TEXT NOT NULL,
    soyad TEXT NOT NULL,
    bolum TEXT NOT NULL,
    sinif INTEGER NOT NULL
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS notlar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ogrenci_no INTEGER NOT NULL,
    ders TEXT NOT NULL,
    vize REAL NOT NULL,
    final REAL NOT NULL
)
""")


baglanti.commit()


# ÖĞRENCİ SINIFI

class Ogrenci:

    def __init__(self, ogrenci_no, ad, soyad, bolum, sinif):
        self.ogrenci_no = ogrenci_no
        self.ad = ad
        self.soyad = soyad
        self.bolum = bolum
        self.sinif = sinif

    def bilgileri_goster(self):
        print("-----------------------------")
        print("Öğrenci No:", self.ogrenci_no)
        print("Ad:", self.ad)
        print("Soyad:", self.soyad)
        print("Bölüm:", self.bolum)
        print("Sınıf:", self.sinif)
        print("-----------------------------")



# DERSLER
# Tuple kullanıyoruz.

dersler = (
    "Python",
    "SQL",
    "Matematik",
    "Algoritma"
)



# ÖĞRENCİ EKLEME

def ogrenci_ekle():

    print("\n--- ÖĞRENCİ EKLE ---")

    ogrenci_no = int(input("Öğrenci numarası: "))

    # Aynı öğrenci var mı kontrol ediyoruz.
    cursor.execute(
        "SELECT * FROM ogrenciler WHERE ogrenci_no = ?",
        (ogrenci_no,)
    )

    ogrenci_var_mi = cursor.fetchone()

    if ogrenci_var_mi:
        print("\nBu öğrenci numarası zaten kayıtlı.")
        return

    ad = input("Ad: ")
    soyad = input("Soyad: ")
    bolum = input("Bölüm: ")
    sinif = int(input("Sınıf: "))

    ogrenci = Ogrenci(
        ogrenci_no,
        ad,
        soyad,
        bolum,
        sinif
    )

    cursor.execute("""
    INSERT INTO ogrenciler
    (ogrenci_no, ad, soyad, bolum, sinif)
    VALUES (?, ?, ?, ?, ?)
    """,
                   (
                       ogrenci.ogrenci_no,
                       ogrenci.ad,
                       ogrenci.soyad,
                       ogrenci.bolum,
                       ogrenci.sinif
                   )
                   )

    baglanti.commit()

    print("\n", ogrenci.ad, ogrenci.soyad, "başarıyla eklendi.")



# ÖĞRENCİLERİ LİSTELE

def ogrencileri_listele():

    print("\n--- ÖĞRENCİLER ---")

    cursor.execute("SELECT * FROM ogrenciler")

    ogrenciler = cursor.fetchall()

    if len(ogrenciler) == 0:
        print("Henüz öğrenci bulunmamaktadır.")
        return

    for ogrenci in ogrenciler:

        print(
            ogrenci[1],
            "|",
            ogrenci[2],
            ogrenci[3],
            "|",
            ogrenci[4],
            "|",
            str(ogrenci[5]) + ". Sınıf"
        )



# ÖĞRENCİ ARA

def ogrenci_ara():

    print("\n--- ÖĞRENCİ ARA ---")

    ogrenci_no = int(input("Öğrenci numarası: "))

    cursor.execute(
        "SELECT * FROM ogrenciler WHERE ogrenci_no = ?",
        (ogrenci_no,)
    )

    ogrenci = cursor.fetchone()

    if ogrenci:

        bulunan_ogrenci = Ogrenci(
            ogrenci[1],
            ogrenci[2],
            ogrenci[3],
            ogrenci[4],
            ogrenci[5]
        )

        print("\nÖğrenci bulundu.")

        bulunan_ogrenci.bilgileri_goster()

    else:
        print("\nÖğrenci bulunamadı.")



# DERSLERİ GÖSTER

def dersleri_goster():

    print("\n--- DERSLER ---")

    sayac = 1

    for ders in dersler:
        print(sayac, "-", ders)
        sayac += 1


# NOT EKLE

def not_ekle():

    print("\n--- NOT EKLE ---")

    ogrenci_no = int(input("Öğrenci numarası: "))

    cursor.execute(
        "SELECT * FROM ogrenciler WHERE ogrenci_no = ?",
        (ogrenci_no,)
    )

    ogrenci = cursor.fetchone()

    if not ogrenci:
        print("\nÖğrenci bulunamadı.")
        return

    print(
        "\nÖğrenci:",
        ogrenci[2],
        ogrenci[3]
    )

    dersleri_goster()

    ders_secimi = int(input("\nDers seçiniz: "))

    if ders_secimi < 1 or ders_secimi > len(dersler):
        print("Geçersiz ders seçimi.")
        return

    secilen_ders = dersler[ders_secimi - 1]

    vize = float(input("Vize notu: "))

    if vize < 0 or vize > 100:
        print("Vize notu 0 ile 100 arasında olmalıdır.")
        return

    final = float(input("Final notu: "))

    if final < 0 or final > 100:
        print("Final notu 0 ile 100 arasında olmalıdır.")
        return

    cursor.execute("""
    INSERT INTO notlar
    (ogrenci_no, ders, vize, final)
    VALUES (?, ?, ?, ?)
    """,
                   (
                       ogrenci_no,
                       secilen_ders,
                       vize,
                       final
                   )
                   )

    baglanti.commit()

    print("\nNot başarıyla eklendi.")


# ORTALAMA HESAPLA

def ortalama_hesapla(vize, final):

    ortalama = (vize * 0.40) + (final * 0.60)

    return ortalama


# GEÇTİ / KALDI

def durum_hesapla(ortalama):

    if ortalama >= 50:
        return "GEÇTİ"

    else:
        return "KALDI"



# ÖĞRENCİNİN NOTLARINI GÖSTER


def notlari_goster():

    print("\n--- ÖĞRENCİ NOTLARI ---")

    ogrenci_no = int(input("Öğrenci numarası: "))

    cursor.execute(
        "SELECT * FROM ogrenciler WHERE ogrenci_no = ?",
        (ogrenci_no,)
    )

    ogrenci = cursor.fetchone()

    if not ogrenci:
        print("\nÖğrenci bulunamadı.")
        return

    print(
        "\nÖğrenci:",
        ogrenci[2],
        ogrenci[3]
    )

    cursor.execute(
        "SELECT * FROM notlar WHERE ogrenci_no = ?",
        (ogrenci_no,)
    )

    notlar = cursor.fetchall()

    if len(notlar) == 0:
        print("\nBu öğrencinin henüz notu bulunmamaktadır.")
        return

    for not_bilgisi in notlar:

        ders = not_bilgisi[2]
        vize = not_bilgisi[3]
        final = not_bilgisi[4]

        ortalama = ortalama_hesapla(
            vize,
            final
        )

        durum = durum_hesapla(
            ortalama
        )

        print("\n----------------------")
        print("Ders:", ders)
        print("Vize:", vize)
        print("Final:", final)
        print("Ortalama:", round(ortalama, 2))
        print("Durum:", durum)



# GENEL ORTALAMA

def genel_ortalama_hesapla():

    print("\n--- GENEL ORTALAMA ---")

    ogrenci_no = int(input("Öğrenci numarası: "))

    cursor.execute(
        "SELECT * FROM ogrenciler WHERE ogrenci_no = ?",
        (ogrenci_no,)
    )

    ogrenci = cursor.fetchone()

    if not ogrenci:
        print("\nÖğrenci bulunamadı.")
        return

    cursor.execute(
        "SELECT * FROM notlar WHERE ogrenci_no = ?",
        (ogrenci_no,)
    )

    notlar = cursor.fetchall()

    if len(notlar) == 0:
        print("\nÖğrencinin herhangi bir notu bulunmamaktadır.")
        return

    toplam = 0

    for not_bilgisi in notlar:

        vize = not_bilgisi[3]
        final = not_bilgisi[4]

        ortalama = ortalama_hesapla(
            vize,
            final
        )

        toplam += ortalama

    genel_ortalama = toplam / len(notlar)

    print(
        "\nÖğrenci:",
        ogrenci[2],
        ogrenci[3]
    )

    print(
        "Genel Ortalama:",
        round(genel_ortalama, 2)
    )

    if genel_ortalama >= 50:
        print("Genel Durum: BAŞARILI")

    else:
        print("Genel Durum: BAŞARISIZ")


# ÖĞRENCİ SİL

def ogrenci_sil():

    print("\n--- ÖĞRENCİ SİL ---")

    ogrenci_no = int(input("Silinecek öğrenci numarası: "))

    cursor.execute(
        "SELECT * FROM ogrenciler WHERE ogrenci_no = ?",
        (ogrenci_no,)
    )

    ogrenci = cursor.fetchone()

    if not ogrenci:
        print("\nÖğrenci bulunamadı.")
        return

    cursor.execute(
        "DELETE FROM ogrenciler WHERE ogrenci_no = ?",
        (ogrenci_no,)
    )

    # Öğrencinin notlarını da siliyoruz.
    cursor.execute(
        "DELETE FROM notlar WHERE ogrenci_no = ?",
        (ogrenci_no,)
    )

    baglanti.commit()

    print(
        "\n",
        ogrenci[2],
        ogrenci[3],
        "sistemden silindi."
    )



# BÖLÜMLERİ GÖSTER

def bolumleri_goster():

    print("\n--- SİSTEMDEKİ BÖLÜMLER ---")

    cursor.execute(
        "SELECT bolum FROM ogrenciler"
    )

    sonuc = cursor.fetchall()

    if len(sonuc) == 0:
        print("Sistemde öğrenci bulunmamaktadır.")
        return

    # SET
    bolumler = set()

    for bolum in sonuc:
        bolumler.add(bolum[0])

    for bolum in bolumler:
        print("-", bolum)


# İSTATİSTİKLER

def istatistikleri_goster():

    print("\n--- İSTATİSTİKLER ---")

    cursor.execute(
        "SELECT * FROM ogrenciler"
    )

    ogrenciler = cursor.fetchall()

    cursor.execute(
        "SELECT * FROM notlar"
    )

    notlar = cursor.fetchall()

    print(
        "Toplam öğrenci:",
        len(ogrenciler)
    )

    print(
        "Toplam not kaydı:",
        len(notlar)
    )

    if len(ogrenciler) == 0:
        return

    bolumler = set()

    for ogrenci in ogrenciler:
        bolumler.add(ogrenci[4])

    print(
        "Toplam bölüm:",
        len(bolumler)
    )



# MENÜ

def menu_goster():

    print("\n")
    print("=================================")
    print("      ÖĞRENCİ NOT SİSTEMİ")
    print("=================================")
    print("1 - Öğrenci Ekle")
    print("2 - Öğrencileri Listele")
    print("3 - Öğrenci Ara")
    print("4 - Not Ekle")
    print("5 - Öğrencinin Notlarını Göster")
    print("6 - Genel Ortalama Hesapla")
    print("7 - Öğrenci Sil")
    print("8 - Bölümleri Göster")
    print("9 - İstatistikleri Göster")
    print("0 - Çıkış")
    print("=================================")


# ANA PROGRAM

while True:

    menu_goster()

    secim = input("Seçiminiz: ")

    if secim == "1":
        ogrenci_ekle()

    elif secim == "2":
        ogrencileri_listele()

    elif secim == "3":
        ogrenci_ara()

    elif secim == "4":
        not_ekle()

    elif secim == "5":
        notlari_goster()

    elif secim == "6":
        genel_ortalama_hesapla()

    elif secim == "7":
        ogrenci_sil()

    elif secim == "8":
        bolumleri_goster()

    elif secim == "9":
        istatistikleri_goster()

    elif secim == "0":

        print("\nProgram kapatılıyor...")
        print("Görüşmek üzere!")

        break

    else:
        print("\nGeçersiz seçim yaptınız.")


# VERİTABANI BAĞLANTISINI KAPAT
baglanti.close()
