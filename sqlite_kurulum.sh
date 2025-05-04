#!/bin/bash
# Kitabevi Otomasyon Sistemi SQLite Kurulum Betiği
# Bu betik, kurulum adımlarını SQLite veritabanı kullanarak otomatik olarak çalıştırır.
# Çalıştırmak için: chmod +x sqlite_kurulum.sh && ./sqlite_kurulum.sh

echo "Kitabevi Otomasyon Sistemi SQLite Kurulumu Başlatılıyor..."
echo "------------------------------------------------"

# Proje klasörüne git
cd "$(dirname "$0")"

# Sanal ortam kontrolü
if [ ! -d "venv" ]; then
    echo "Sanal ortam oluşturuluyor..."
    python3 -m venv venv
fi

# Sanal ortamı aktifleştir
echo "Sanal ortam aktifleştiriliyor..."
source venv/bin/activate

# Gereksinimleri yükle
echo "Gerekli kütüphaneler yükleniyor..."
pip install -r requirements.txt

# SQLite için .env dosyasını oluştur
echo "DATABASE_URL=sqlite:///$(pwd)/app.db" > .env
echo "SECRET_KEY=otomasyongizlianahtar" >> .env
echo ".env dosyası oluşturuldu."

# Flask uygulamasını ayarla
export FLASK_APP=run.py

# Veritabanı dosyasını sil (eğer varsa)
if [ -f "app.db" ]; then
    echo "Eski veritabanı siliniyor..."
    rm app.db
fi

# Migration klasörünü sil (eğer varsa)
if [ -d "migrations" ]; then
    echo "Eski migrations klasörü siliniyor..."
    rm -rf migrations
fi

# Veritabanı şemasını oluştur
echo "Veritabanı şeması oluşturuluyor..."
flask db init
flask db migrate -m "initial migration"
flask db upgrade

# Admin kullanıcısını oluştur
echo "Admin kullanıcısı oluşturuluyor..."
python3 -c "
from app import create_app, db
from app.models import Personel
app = create_app()
with app.app_context():
    if not Personel.query.filter_by(KullaniciAdi='admin').first():
        admin = Personel(KullaniciAdi='admin', Ad='Admin', Soyad='User', Rol='Admin')
        admin.set_password('password')
        db.session.add(admin)
        db.session.commit()
        print('Admin kullanıcısı oluşturuldu!')
    else:
        print('Admin kullanıcısı zaten mevcut.')
"

# Örnek verileri ekle
echo "Örnek veriler ekleniyor..."
python3 -c "
from app import create_app
from ilk_veriler import ekle_veriler
app = create_app()
with app.app_context():
    ekle_veriler()
"

echo "------------------------------------------------"
echo "Kurulum Tamamlandı!"
echo "Uygulamayı başlatmak için: flask run"
echo "Tarayıcınızdan http://127.0.0.1:5000 adresine gidebilirsiniz."
echo "Giriş bilgileri: admin / password"