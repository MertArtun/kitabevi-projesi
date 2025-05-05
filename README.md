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
   git clone https://github.com/kullanici/kitabevi-projesi.git
   cd kitabevi-projesi
   ```

2. SQLite kurulum betiğini çalıştırın:
   ```bash
   # macOS/Linux için
   chmod +x sqlite_kurulum.sh
   ./sqlite_kurulum.sh

   # Windows için
   # sqlite_kurulum.bat dosyasını çalıştırın
   ```

3. Veya manuel olarak kurulum yapın:
   a. Sanal ortam oluşturun ve aktive edin:
      ```bash
      python -m venv venv

      # Windows
      venv\Scripts\activate

      # macOS/Linux
      source venv/bin/activate
      ```

   b. Gerekli kütüphaneleri yükleyin:
      ```bash
      pip install -r requirements.txt
      ```

   c. Veritabanını oluşturun ve migrate edin:
      ```bash
      export FLASK_APP=run.py  # macOS/Linux için
      # Windows için: set FLASK_APP=run.py

      flask db init
      flask db migrate -m "initial migration"
      flask db upgrade
      ```

   d. Admin kullanıcısı oluşturun:
      ```bash
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
      ```bash
      flask run --port 5001
      ```

4. Tarayıcıdan http://127.0.0.1:5001 adresine giderek sisteme erişebilirsiniz:
   - Kullanıcı Adı: admin
   - Şifre: password

## Veritabanı Şeması
Proje veritabanı, kitabevi operasyonları için gerekli temel varlıkları ve ilişkileri modellemektedir. Şema, 5. Normal Forma (5NF) uygunluk hedeflenerek tasarlanmıştır.
- Toplam 8 tablo bulunmaktadır: Yazarlar, Yayinevleri, Kategoriler, Kitaplar, KitapYazarlari, Musteriler, Personeller, Satislar, SatisDetaylari.
- Tablolar arasında yabancı anahtarlar ile ilişkiler kurulmuştur.
- Performans ve iş mantığı için Index, View ve Trigger kullanımları eklenmiştir.
- Veritabanı şeması tanımı `sql_scripts/schema.sql` dosyasında bulunabilir.

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
├── app.db                  # SQLite veritabanı dosyası (Geliştirme)
├── sql_scripts/            # SQL betikleri (PostgreSQL şeması, Index, View, Trigger)
├── config.py               # Yapılandırma ayarları
├── requirements.txt        # Gerekli Python kütüphaneleri
├── run.py                  # Uygulamayı başlatan script
└── README.md               # Proje dokümanı
```

## Özellikler
- Kitap katalog yönetimi (kitap, yazar, yayınevi, kategori)
- Müşteri yönetimi
- Satış işlemleri (sepet, satış tamamlama, stok güncelleme)
- Stok takibi (otomatik stok güncellemesi)
- Kullanıcı (personel) yetkilendirme sistemi
- Raporlama (satış raporları - PDF özelliği şu an devre dışı)
- Kitap kapak resmi yükleme ve yönetimi
- Kitap arama API'si

## Arayüz Görselleri
Uygulamanın farklı sayfalarına ait ekran görüntüleri bu bölümde veya ayrı bir `screenshots/` dizininde yer almalıdır. README dosyasına görselleri eklemek için markdown formatını kullanabilirsiniz: `![Açıklama](yol/to/gorsel.png)`.

## Proje Raporu
Proje raporu, IEEE konferans şablonuna uygun olarak hazırlanmalı ve bu depoda `grupno_rapor.pdf` adıyla bulunmalıdır.

## Teslimat Dosyaları
Proje teslimi için aşağıdaki dosyalar hazırlanmalıdır:
- Veritabanı dosyaları: `grupno_sql_betikleri.txt` (İçeriği `sql_scripts/schema.sql` dosyasından alınabilir.)
- Program kodları: `grupno_kaynakkod.txt` (Tüm kaynak kod dosyalarını içermelidir.)
- Proje raporu: `grupno_rapor.pdf`
- GitHub bağlantısı: `grupno_github.txt` (Deponuzun URL'sini içermelidir.)