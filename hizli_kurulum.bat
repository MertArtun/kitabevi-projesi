@echo off
REM Kitabevi Otomasyon Sistemi Hızlı Kurulum Betiği (Windows)
REM Bu batch dosyası Windows için kurulum adımlarını otomatik olarak çalıştırır.

echo Kitabevi Otomasyon Sistemi Kurulumu Baslatiliyor...
echo ------------------------------------------------

REM Proje klasörüne git
cd /d "%~dp0"

REM Sanal ortam kontrolü
if not exist "venv" (
    echo Sanal ortam olusturuluyor...
    python -m venv venv
)

REM Sanal ortamı aktifleştir
echo Sanal ortam aktiflestiriliyor...
call venv\Scripts\activate

REM Gereksinimleri yükle
echo Gerekli kutuphaneler yukleniyor...
pip install -r requirements.txt

REM .env dosyasını oluştur
if not exist ".env" (
    echo DATABASE_URL=postgresql://postgres:postgres@localhost/kitabevi > .env
    echo SECRET_KEY=otomasyongizlianahtar >> .env
    echo .env dosyasi olusturuldu.
)

REM PostgreSQL kontrolü
echo PostgreSQL veritabani kontrolu yapiliyor...
echo NOT: PostgreSQL'in kurulu ve çalışıyor olduğundan emin olun.
echo Windows için https://www.postgresql.org/download/windows/ adresinden indirebilirsiniz.
echo Veritabani olusturulmasi gerekiyor. pgAdmin veya psql ile 'kitabevi' adinda bir veritabani olusturun.
pause

REM Flask uygulamasını ayarla
set FLASK_APP=run.py

REM Veritabanı şemasını oluştur
echo Veritabani semasi olusturuluyor...
flask db init
flask db migrate -m "initial migration" 
flask db upgrade

REM Admin kullanıcısını oluştur
echo Admin kullanicisi olusturuluyor...
python -c "from app import create_app, db; from app.models import Personel; app = create_app(); ctx = app.app_context(); ctx.push(); admin = Personel.query.filter_by(KullaniciAdi='admin').first(); admin_new = False if admin else True; if admin_new: admin = Personel(KullaniciAdi='admin', Ad='Admin', Soyad='User', Rol='Admin'); admin.set_password('password'); db.session.add(admin); db.session.commit(); print('Admin kullanicisi olusturuldu!'); else: print('Admin kullanicisi zaten mevcut.'); ctx.pop();"

REM Örnek verileri ekle
echo Ornek veriler ekleniyor...
python -c "from app import create_app; from ilk_veriler import ekle_veriler; app = create_app(); ctx = app.app_context(); ctx.push(); ekle_veriler(); ctx.pop();"

echo ------------------------------------------------
echo Kurulum Tamamlandi!
echo Uygulamayi baslatmak icin: flask run
echo Tarayicinizdan http://127.0.0.1:5000 adresine gidebilirsiniz.
echo Giris bilgileri: admin / password
pause