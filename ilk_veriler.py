"""
Kitabevi Otomasyon Sistemi için örnek veriler
---------------------------------------------
Bu script, veritabanına örnek veriler ekler.
Sistemi test etmek için kullanabilirsiniz.

Kullanım:
-------
1. Sanal ortamı aktifleştirin
2. flask shell
3. exec(open('ilk_veriler.py').read())
"""

from app import db
from app.models import Yazar, Yayinevi, Kategori, Kitap, Personel, Musteri
from werkzeug.security import generate_password_hash
from datetime import datetime

def ekle_veriler():
    print("Örnek veriler ekleniyor...")
    
    # Verileri temizle
    try:
        Kitap.query.delete()
        Yazar.query.delete()
        Yayinevi.query.delete()
        Kategori.query.delete()
        Musteri.query.delete()
        
        # Admin dışındaki personeli temizle
        Personel.query.filter(Personel.KullaniciAdi != 'admin').delete()
        
        db.session.commit()
        print("Mevcut veriler temizlendi.")
    except Exception as e:
        db.session.rollback()
        print(f"Veri temizleme hatası: {str(e)}")
        return
    
    try:
        # Personel ekle
        personel1 = Personel(
            KullaniciAdi="kasiyer1",
            SifreHash=generate_password_hash("kasiyer123"),
            Ad="Ahmet",
            Soyad="Yılmaz",
            Rol="Kasiyer"
        )
        db.session.add(personel1)
        
        # Yazarlar ekle
        yazar1 = Yazar(Ad="Yaşar", Soyad="Kemal", Biyografi="Türk edebiyatının en önemli yazarlarından.")
        yazar2 = Yazar(Ad="Orhan", Soyad="Pamuk", Biyografi="Nobel ödüllü Türk yazar.")
        yazar3 = Yazar(Ad="Sabahattin", Soyad="Ali", Biyografi="Öykü ve roman yazarı.")
        yazar4 = Yazar(Ad="George", Soyad="Orwell", Biyografi="İngiliz yazar, gazeteci ve eleştirmen.")
        
        db.session.add_all([yazar1, yazar2, yazar3, yazar4])
        
        # Yayınevleri ekle
        yayinevi1 = Yayinevi(Ad="YKY", Adres="İstanbul", Telefon="0212 111 22 33")
        yayinevi2 = Yayinevi(Ad="Can Yayınları", Adres="İstanbul", Telefon="0212 444 55 66")
        yayinevi3 = Yayinevi(Ad="İletişim", Adres="İstanbul", Telefon="0212 777 88 99")
        
        db.session.add_all([yayinevi1, yayinevi2, yayinevi3])
        
        # Kategoriler ekle
        kategori1 = Kategori(Ad="Roman")
        kategori2 = Kategori(Ad="Öykü")
        kategori3 = Kategori(Ad="Şiir")
        kategori4 = Kategori(Ad="Bilim Kurgu")
        kategori5 = Kategori(Ad="Tarih")
        
        db.session.add_all([kategori1, kategori2, kategori3, kategori4, kategori5])
        
        db.session.commit()
        
        # Kitaplar ekle
        kitap1 = Kitap(
            ISBN="9789750802195",
            Ad="İnce Memed",
            YayinYili=2019,
            SayfaSayisi=450,
            Fiyat=75.00,
            StokAdedi=25,
            YayineviID=yayinevi1.YayineviID,
            KategoriID=kategori1.KategoriID
        )
        kitap1.yazarlar.append(yazar1)
        
        kitap2 = Kitap(
            ISBN="9789750802324",
            Ad="Benim Adım Kırmızı",
            YayinYili=2020,
            SayfaSayisi=478,
            Fiyat=85.00,
            StokAdedi=15,
            YayineviID=yayinevi2.YayineviID,
            KategoriID=kategori1.KategoriID
        )
        kitap2.yazarlar.append(yazar2)
        
        kitap3 = Kitap(
            ISBN="9789750803578",
            Ad="Kürk Mantolu Madonna",
            YayinYili=2018,
            SayfaSayisi=160,
            Fiyat=45.00,
            StokAdedi=30,
            YayineviID=yayinevi2.YayineviID,
            KategoriID=kategori1.KategoriID
        )
        kitap3.yazarlar.append(yazar3)
        
        kitap4 = Kitap(
            ISBN="9789750804956",
            Ad="1984",
            YayinYili=2020,
            SayfaSayisi=350,
            Fiyat=65.00,
            StokAdedi=20,
            YayineviID=yayinevi3.YayineviID,
            KategoriID=kategori4.KategoriID
        )
        kitap4.yazarlar.append(yazar4)
        
        kitap5 = Kitap(
            ISBN="9789750805321",
            Ad="Hayvan Çiftliği",
            YayinYili=2019,
            SayfaSayisi=152,
            Fiyat=55.00,
            StokAdedi=18,
            YayineviID=yayinevi3.YayineviID,
            KategoriID=kategori1.KategoriID
        )
        kitap5.yazarlar.append(yazar4)
        
        db.session.add_all([kitap1, kitap2, kitap3, kitap4, kitap5])
        
        # Müşteriler ekle
        musteri1 = Musteri(
            Ad="Mehmet",
            Soyad="Kaya",
            Email="mehmet.kaya@example.com",
            Telefon="0535 111 22 33",
            KayitTarihi=datetime.now()
        )
        
        musteri2 = Musteri(
            Ad="Ayşe",
            Soyad="Demir",
            Email="ayse.demir@example.com",
            Telefon="0542 333 44 55",
            KayitTarihi=datetime.now()
        )
        
        db.session.add_all([musteri1, musteri2])
        
        db.session.commit()
        print("Örnek veriler başarıyla eklendi!")
    
    except Exception as e:
        db.session.rollback()
        print(f"Veri ekleme hatası: {str(e)}")

# Flask shell içinde çalıştırılacak
if __name__ == '__main__':
    ekle_veriler()