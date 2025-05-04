# Kitabevi Otomasyon Sistemi

## Proje Özeti
Bu proje, bir kitabevinin temel operasyonlarını (kitap yönetimi, müşteri yönetimi, satış işlemleri, stok takibi) dijital ortama taşımayı amaçlayan bir otomasyon sistemidir. Sistem, kullanıcı dostu bir arayüz üzerinden kitapların, yazarların, yayınevlerinin, müşterilerin ve satışların kaydedilmesini, güncellenmesini, silinmesini ve sorgulanmasını sağlamaktadır.

## Geliştirme Ortamı
- İşletim Sistemi: Windows 10/11, macOS, Linux
- Yazılım Dili: Python 3.10+
- Framework: Flask 2.2.3
- Veritabanı: SQLite (Geliştirme) / PostgreSQL (Üretim)
- IDE: VS Code
- Diğer Araçlar: Git, SQLite Browser

## Kurulum ve Çalıştırma (SQLite ile)
1. Repoyu klonlayın:
   ```
   git clone https://github.com/kullanici/kitabevi-projesi.git
   cd kitabevi-projesi
   ```

2. SQLite kurulum betiğini çalıştırın:
   ```
   # macOS/Linux için
   chmod +x sqlite_kurulum.sh
   ./sqlite_kurulum.sh
   
   # Windows için
   # sqlite_kurulum.bat dosyasını çalıştırın
   ```

3. Veya manuel olarak kurulum yapın:
   a. Sanal ortam oluşturun ve aktive edin:
      ```
      python -m venv venv
      
      # Windows
      venv\Scripts\activate
      
      # macOS/Linux
      source venv/bin/activate
      ```
   
   b. Gerekli kütüphaneleri yükleyin:
      ```
      pip install -r requirements.txt
      ```
   
   c. Veritabanını oluşturun:
      ```
      export FLASK_APP=run.py  # macOS/Linux için
      # Windows için: set FLASK_APP=run.py
      
      flask db init
      flask db migrate -m "initial migration"
      flask db upgrade
      ```
   
   d. Admin kullanıcısı oluşturun:
      ```
      flask shell
      ```
      
      Shell içinde:
      ```python
      from app import db
      from app.models import Personel
      
      admin = Personel(KullaniciAdi="admin", Ad="Admin", Soyad="User", Rol="Admin")
      admin.set_password("password")
      db.session.add(admin)
      db.session.commit()
      exit()
      ```
   
   e. Uygulamayı başlatın:
      ```
      flask run
      ```

4. Tarayıcıdan http://127.0.0.1:5000 adresine giderek sisteme erişebilirsiniz:
   - Kullanıcı Adı: admin
   - Şifre: password

## Proje Yapısı
```
kitabevi-projesi/
├── app/                    # Ana uygulama paketi
│   ├── __init__.py         # Uygulama fabrikası, blueprint kaydı
│   ├── models.py           # Veritabanı modelleri
│   ├── auth/               # Kimlik doğrulama modülü
│   ├── kitaplar/           # Kitap yönetimi modülü
│   ├── satis/              # Satış işlemleri modülü
│   ├── main/               # Ana sayfa modülü
│   ├── static/             # CSS, JS, resim dosyaları
│   └── templates/          # HTML şablonları
├── migrations/             # Veritabanı migration dosyaları
├── app.db                  # SQLite veritabanı dosyası
├── sql_scripts/            # SQL betikleri (PostgreSQL için)
├── config.py               # Yapılandırma ayarları
├── requirements.txt        # Gerekli Python kütüphaneleri
├── run.py                  # Uygulamayı başlatan script
└── README.md               # Proje dokümanı
```

## Özellikler
- Kitap katalog yönetimi (kitap, yazar, yayınevi, kategori)
- Müşteri yönetimi
- Satış işlemleri
- Stok takibi (otomatik stok güncellemesi)
- Kullanıcı (personel) yetkilendirme sistemi
- Raporlama (satış raporları)