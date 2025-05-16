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
   ```bash
   git clone https://github.com/MertArtun/kitabevi-projesi.git
   cd kitabevi-projesi
   ```

2. SQLite kurulum betiğini çalıştırın (Opsiyonel, manuel kurulum adımları aşağıdadır):
   ```bash
   chmod +x sqlite_kurulum.sh
   ./sqlite_kurulum.sh

   sqlite_kurulum.bat
   ```

3. Veya manuel olarak kurulum yapın:
   a. Sanal ortam oluşturun ve aktive edin:
      ```bash
      python -m venv venv

      venv\Scripts\activate

      source venv/bin/activate
      ```

   b. Gerekli kütüphaneleri yükleyin:
      ```bash
      pip install -r requirements.txt
      ```

   c. Veritabanını oluşturun ve migrate edin:
      ```bash
      export FLASK_APP=run.py
      
      set FLASK_APP=run.py

      flask db init
      flask db migrate -m "initial migration"
      flask db upgrade
      ```

   d. Admin kullanıcısı oluşturun (Eğer `sqlite_kurulum` betikleri kullanılmadıysa veya özel bir admin isteniyorsa):
      ```bash
      flask shell
      ```
      Shell içinde aşağıdaki Python komutlarını çalıştırın:
      ```python
      from app import db
      from app.models import Personel

      admin = Personel(KullaniciAdi="admin", Ad="Admin", Soyad="User", Rol="Admin")
      admin.set_password("password123")
      db.session.add(admin)
      db.session.commit()
      exit()
      ```

   e. Uygulamayı başlatın:
      ```bash
      flask run --port 5001
      ```

4. Tarayıcıdan `http://127.0.0.1:5001` adresine giderek sisteme erişebilirsiniz:
   - Kullanıcı Adı: `admin` (veya yukarıda belirlediğiniz kullanıcı adı)
   - Şifre: `password123` (veya yukarıda belirlediğiniz şifre)

## Veritabanı Şeması
Proje veritabanı, kitabevi operasyonları için gerekli temel varlıkları ve ilişkileri modellemektedir.
- Desteklenen Veritabanları: SQLite (geliştirme için), PostgreSQL (üretim için önerilir).
- Şema, ilişkisel model prensiplerine uygun olarak tasarlanmıştır.
- Toplam 8 ana tablo bulunmaktadır: `Yazarlar`, `Yayinevleri`, `Kategoriler`, `Kitaplar`, `KitapYazarlari` (çok-a-çok ilişki), `Musteriler`, `Personeller`, `Satislar`, `SatisDetaylari`.
- Tablolar arasında yabancı anahtarlar ile ilişkiler kurulmuştur.
- Performans ve iş mantığı için Index, View (`vw_KitapDetaylari`) ve Trigger (`update_stock_after_sale`) kullanımları eklenmiştir.
- Detaylı veritabanı şeması tanımı `sql_scripts/schema.sql` dosyasında bulunabilir.

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
├── sql_scripts/            # SQL betikleri (PostgreSQL şeması, Index, View, Trigger)
├── .gitignore              # Git tarafından takip edilmeyecek dosyalar
├── config.py               # Yapılandırma ayarları
├── requirements.txt        # Gerekli Python kütüphaneleri
├── run.py                  # Uygulamayı başlatan script
├── hizli_kurulum.bat       # Windows için hızlı kurulum betiği
├── hizli_kurulum.sh        # macOS/Linux için hızlı kurulum betiği
└── README.md               # Bu doküman
```

## Özellikler
- Kapsamlı Kitap Katalog Yönetimi: Kitap, yazar, yayınevi ve kategori ekleme, düzenleme, silme.
- Müşteri İlişkileri Yönetimi (CRM): Müşteri bilgilerinin kaydı ve takibi.
- Satış İşlemleri: Kullanıcı dostu sepet mekanizması, satış tamamlama ve fatura (detay) oluşturma.
- Otomatik Stok Takibi: Satış sonrası otomatik stok güncellemesi ve yetersiz stok uyarıları.
- Kullanıcı (Personel) Yönetimi ve Yetkilendirme: Farklı rollerde kullanıcılar (Admin, Personel) ve yetki kontrolü.
- Raporlama: Temel satış raporları.
- Kitap Kapak Resmi Yönetimi: Kitaplara kapak resmi yükleme ve görüntüleme.
- Kitap Arama API'si: Kitapları programatik olarak aramak için bir API endpoint'i.

## Katkıda Bulunma
Katkılarınız ve önerileriniz için lütfen bir issue açın veya pull request gönderin.

## Lisans
Bu proje MIT Lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakınız.