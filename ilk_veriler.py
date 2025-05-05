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
from sqlalchemy import text

def ekle_veriler():
    print("Örnek veriler ekleniyor...")
    
    # Verileri temizle
    try:
        # Önce kitap-yazar ilişkilerini temizle
        db.session.execute(text('DELETE FROM KitapYazarlari'))
        
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
        yazar5 = Yazar(Ad="Oğuz", Soyad="Atay", Biyografi="Türk mühendis, öğretim üyesi ve yazar.")
        yazar6 = Yazar(Ad="Victor", Soyad="Hugo", Biyografi="Fransız şair, romancı ve oyun yazarı.")
        yazar7 = Yazar(Ad="Fyodor", Soyad="Dostoyevski", Biyografi="Rus roman yazarı, kısa öykü yazarı, deneme yazarı ve gazeteci.")
        yazar8 = Yazar(Ad="Stefan", Soyad="Zweig", Biyografi="Avusturyalı romancı, oyun yazarı, gazeteci ve biyografi yazarı.")
        yazar9 = Yazar(Ad="Franz", Soyad="Kafka", Biyografi="Alman dilinde yazan Çek kökenli yazar.")
        
        db.session.add_all([yazar1, yazar2, yazar3, yazar4, yazar5, yazar6, yazar7, yazar8, yazar9])
        
        # Yayınevleri ekle
        yayinevi1 = Yayinevi(Ad="YKY", Adres="İstanbul", Telefon="0212 111 22 33")
        yayinevi2 = Yayinevi(Ad="Can Yayınları", Adres="İstanbul", Telefon="0212 444 55 66")
        yayinevi3 = Yayinevi(Ad="İletişim", Adres="İstanbul", Telefon="0212 777 88 99")
        yayinevi4 = Yayinevi(Ad="İş Bankası Kültür Yayınları", Adres="İstanbul", Telefon="0212 222 33 44")
        yayinevi5 = Yayinevi(Ad="Türkiye İş Bankası Kültür Yayınları", Adres="İstanbul", Telefon="0212 333 44 55")
        
        db.session.add_all([yayinevi1, yayinevi2, yayinevi3, yayinevi4, yayinevi5])
        
        # Kategoriler ekle
        kategori1 = Kategori(Ad="Roman")
        kategori2 = Kategori(Ad="Öykü")
        kategori3 = Kategori(Ad="Şiir")
        kategori4 = Kategori(Ad="Bilim Kurgu")
        kategori5 = Kategori(Ad="Tarih")
        kategori6 = Kategori(Ad="Distopya")
        kategori7 = Kategori(Ad="Klasik")
        
        db.session.add_all([kategori1, kategori2, kategori3, kategori4, kategori5, kategori6, kategori7])
        
        # Önce commit yaparak yukarıdaki verilerin ID'lerini oluşturalım
        db.session.commit()
        
        # Kitaplar ekle - artık kapak resmi dosyaları ile birlikte
        kitap1 = Kitap(
            ISBN="9789750802195",
            Ad="İnce Memed",
            YayinYili=2019,
            SayfaSayisi=450,
            Fiyat=75.00,
            StokAdedi=25,
            YayineviID=yayinevi1.YayineviID,
            KategoriID=kategori1.KategoriID,
            KapakResmi="ince_memed.jpg"
        )
        db.session.add(kitap1)
        db.session.flush()  # ID'yi oluştur
        kitap1.yazarlar.append(yazar1)
        
        kitap2 = Kitap(
            ISBN="9789750802324",
            Ad="Benim Adım Kırmızı",
            YayinYili=2020,
            SayfaSayisi=478,
            Fiyat=85.00,
            StokAdedi=15,
            YayineviID=yayinevi2.YayineviID,
            KategoriID=kategori1.KategoriID,
            KapakResmi="benim_adim_kirmizi.jpg"
        )
        db.session.add(kitap2)
        db.session.flush()
        kitap2.yazarlar.append(yazar2)
        
        kitap3 = Kitap(
            ISBN="9789750803578",
            Ad="Kürk Mantolu Madonna",
            YayinYili=2018,
            SayfaSayisi=160,
            Fiyat=45.00,
            StokAdedi=30,
            YayineviID=yayinevi2.YayineviID,
            KategoriID=kategori1.KategoriID,
            KapakResmi="kurk_mantolu_madonna.jpg"
        )
        db.session.add(kitap3)
        db.session.flush()
        kitap3.yazarlar.append(yazar3)
        
        kitap4 = Kitap(
            ISBN="9789750804956",
            Ad="1984",
            YayinYili=2020,
            SayfaSayisi=350,
            Fiyat=65.00,
            StokAdedi=20,
            YayineviID=yayinevi3.YayineviID,
            KategoriID=kategori6.KategoriID,
            KapakResmi="1984.jpg"
        )
        db.session.add(kitap4)
        db.session.flush()
        kitap4.yazarlar.append(yazar4)
        
        kitap5 = Kitap(
            ISBN="9789750805321",
            Ad="Hayvan Çiftliği",
            YayinYili=2019,
            SayfaSayisi=152,
            Fiyat=55.00,
            StokAdedi=18,
            YayineviID=yayinevi3.YayineviID,
            KategoriID=kategori1.KategoriID,
            KapakResmi="hayvan_ciftligi.jpg"
        )
        db.session.add(kitap5)
        db.session.flush()
        kitap5.yazarlar.append(yazar4)
        
        # Yeni kitapları ekle
        kitap6 = Kitap(
            ISBN="9789750806234",
            Ad="Tutunamayanlar",
            YayinYili=2015,
            SayfaSayisi=724,
            Fiyat=95.00,
            StokAdedi=10,
            YayineviID=yayinevi1.YayineviID,
            KategoriID=kategori1.KategoriID,
            KapakResmi="tutunamayanlar.jpg"
        )
        db.session.add(kitap6)
        db.session.flush()
        kitap6.yazarlar.append(yazar5)
        
        kitap7 = Kitap(
            ISBN="9789750807456",
            Ad="Sefiller",
            YayinYili=2017,
            SayfaSayisi=1560,
            Fiyat=120.00,
            StokAdedi=8,
            YayineviID=yayinevi4.YayineviID,
            KategoriID=kategori7.KategoriID,
            KapakResmi="sefiller.jpg"
        )
        db.session.add(kitap7)
        db.session.flush()
        kitap7.yazarlar.append(yazar6)
        
        kitap8 = Kitap(
            ISBN="9789750808234",
            Ad="Suç ve Ceza",
            YayinYili=2016,
            SayfaSayisi=687,
            Fiyat=85.00,
            StokAdedi=12,
            YayineviID=yayinevi5.YayineviID,
            KategoriID=kategori7.KategoriID,
            KapakResmi="suc_ve_ceza.jpg"
        )
        db.session.add(kitap8)
        db.session.flush()
        kitap8.yazarlar.append(yazar7)
        
        kitap9 = Kitap(
            ISBN="9789750809876",
            Ad="Satranç",
            YayinYili=2019,
            SayfaSayisi=83,
            Fiyat=35.00,
            StokAdedi=25,
            YayineviID=yayinevi2.YayineviID,
            KategoriID=kategori2.KategoriID,
            KapakResmi="satranc.jpg"
        )
        db.session.add(kitap9)
        db.session.flush()
        kitap9.yazarlar.append(yazar8)
        
        kitap10 = Kitap(
            ISBN="9789750810342",
            Ad="Dönüşüm",
            YayinYili=2018,
            SayfaSayisi=96,
            Fiyat=42.00,
            StokAdedi=20,
            YayineviID=yayinevi3.YayineviID,
            KategoriID=kategori2.KategoriID,
            KapakResmi="donusum.jpg"
        )
        db.session.add(kitap10)
        db.session.flush()
        kitap10.yazarlar.append(yazar9)
        
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