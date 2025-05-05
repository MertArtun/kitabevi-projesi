import random
from faker import Faker
from app import create_app, db
from app.models import Kitap, Yazar, Yayinevi, Kategori
import os

# Faker kütüphanesi ile sahte veri üretimi
fake = Faker('tr_TR') # Türkçe veri üretimi için

# Uygulama bağlamını oluştur
app = create_app()
app.app_context().push()

# --- Örnek Veri Oluşturma Fonksiyonları ---

def create_or_get_yazarlar(count=20):
    """Belirtilen sayıda yazar oluşturur veya mevcutları döndürür."""
    yazarlar = Yazar.query.all()
    if len(yazarlar) >= count:
        return yazarlar[:count]
    
    new_yazarlar = []
    for _ in range(count - len(yazarlar)):
        yazar = Yazar(Ad=fake.first_name(), Soyad=fake.last_name(), Biyografi=fake.text(max_nb_chars=200))
        db.session.add(yazar)
        new_yazarlar.append(yazar)
    
    try:
        db.session.commit()
        print(f"{len(new_yazarlar)} yeni yazar eklendi.")
        return Yazar.query.limit(count).all()
    except Exception as e:
        db.session.rollback()
        print(f"Yazar eklenirken hata oluştu: {e}")
        return Yazar.query.limit(count).all()

def create_or_get_yayinevleri(count=10):
    """Belirtilen sayıda yayınevi oluşturur veya mevcutları döndürür."""
    yayinevleri = Yayinevi.query.all()
    if len(yayinevleri) >= count:
        return yayinevleri[:count]
        
    new_yayinevleri = []
    existing_names = {y.Ad for y in yayinevleri}
    
    attempts = 0
    while len(yayinevleri) + len(new_yayinevleri) < count and attempts < count * 2:
        attempts += 1
        ad = fake.company() + " Yayınları"
        if ad not in existing_names:
            yayinevi = Yayinevi(Ad=ad, Adres=fake.address(), Telefon=fake.phone_number())
            db.session.add(yayinevi)
            new_yayinevleri.append(yayinevi)
            existing_names.add(ad)
            
    try:
        db.session.commit()
        print(f"{len(new_yayinevleri)} yeni yayınevi eklendi.")
        return Yayinevi.query.limit(count).all()
    except Exception as e:
        db.session.rollback()
        print(f"Yayınevi eklenirken hata oluştu: {e}")
        return Yayinevi.query.limit(count).all()

def create_or_get_kategoriler(kategori_listesi=None):
    """Belirtilen listedeki kategorileri oluşturur veya mevcutları döndürür."""
    if kategori_listesi is None:
        kategori_listesi = ["Roman", "Bilim Kurgu", "Fantastik", "Polisiye", "Tarih", 
                           "Kişisel Gelişim", "Çocuk Kitapları", "Şiir", "Deneme", "Biyografi"]
                           
    kategoriler = Kategori.query.all()
    existing_names = {k.Ad for k in kategoriler}
    new_kategoriler = []
    
    for ad in kategori_listesi:
        if ad not in existing_names:
            kategori = Kategori(Ad=ad)
            db.session.add(kategori)
            new_kategoriler.append(kategori)
            existing_names.add(ad)
            
    try:
        db.session.commit()
        if new_kategoriler:
            print(f"{len(new_kategoriler)} yeni kategori eklendi.")
        return Kategori.query.filter(Kategori.Ad.in_(kategori_listesi)).all()
    except Exception as e:
        db.session.rollback()
        print(f"Kategori eklenirken hata oluştu: {e}")
        return Kategori.query.filter(Kategori.Ad.in_(kategori_listesi)).all()

def get_existing_covers():
    """Mevcut kapak resimlerinin listesini döndürür."""
    kapak_klasoru = os.path.join(app.root_path, 'static', 'img', 'kitap_kapaklari')
    if not os.path.exists(kapak_klasoru):
        return ['default_book_cover.jpg']
    
    files = [f for f in os.listdir(kapak_klasoru) if os.path.isfile(os.path.join(kapak_klasoru, f))]
    if not files:
        return ['default_book_cover.jpg']
    return files

# --- Ana Kitap Ekleme Fonksiyonu ---

def add_books(count=50):
    """Veritabanına belirtilen sayıda örnek kitap ekler."""
    print("Örnek veriler oluşturuluyor...")
    yazarlar = create_or_get_yazarlar()
    yayinevleri = create_or_get_yayinevleri()
    kategoriler = create_or_get_kategoriler()
    kapaklar = get_existing_covers()
    
    if not yazarlar or not yayinevleri or not kategoriler:
        print("Hata: Yazar, yayınevi veya kategori oluşturulamadı. Kitap eklenemiyor.")
        return

    print(f"{count} adet kitap eklenecek...")
    added_count = 0
    for i in range(count):
        try:
            # Benzersiz ISBN oluştur
            isbn = fake.isbn13(separator="")
            while Kitap.query.filter_by(ISBN=isbn).first():
                 isbn = fake.isbn13(separator="")

            kitap = Kitap(
                ISBN=isbn,
                Ad=fake.catch_phrase().title(), # Rastgele kitap adı
                YayinYili=random.randint(1950, 2024),
                SayfaSayisi=random.randint(100, 800),
                Fiyat=round(random.uniform(20.0, 250.0), 2),
                StokAdedi=random.randint(0, 100),
                YayineviID=random.choice(yayinevleri).YayineviID,
                KategoriID=random.choice(kategoriler).KategoriID,
                KapakResmi=random.choice(kapaklar) # Rastgele bir kapak seç
            )
            
            # Rastgele 1 veya 2 yazar ata
            num_authors = random.randint(1, 2)
            selected_authors = random.sample(yazarlar, num_authors)
            for yazar in selected_authors:
                kitap.yazarlar.append(yazar)
                
            db.session.add(kitap)
            
            # Her 10 kitapta bir commit yap (performans için)
            if (i + 1) % 10 == 0:
                db.session.commit()
                print(f"{i + 1} kitap eklendi...")
            
            added_count += 1

        except Exception as e:
            db.session.rollback()
            print(f"Kitap eklenirken hata oluştu (ISBN: {isbn}): {e}")
            # Hata durumunda bir sonraki kitaba geç
            continue 
            
    # Kalanları commit et
    try:
        db.session.commit()
        print(f"Toplam {added_count} kitap başarıyla eklendi.")
    except Exception as e:
        db.session.rollback()
        print(f"Son commit sırasında hata oluştu: {e}")


if __name__ == '__main__':
    add_books(50)