# Kitabevi Otomasyon Sistemi - Proje Planı

Bu doküman, "Kitabevi Otomasyon Sistemi" projesini belirtilen gereksinimlere uygun hale getirmek için izlenecek adımları detaylandırmaktadır.

## Mevcut Durum Analizi

Proje, Python ve Flask framework'ü kullanılarak modüler bir yapıda geliştirilmiştir. SQLAlchemy, Flask-Login, Flask-Migrate gibi yaygın ve uygun kütüphaneler kullanılmıştır. Veritabanı şeması 8 tablo içermekte ve tablolar arasında ilişkiler kurulmuştur. Index, View ve Trigger kullanımları `sql_scripts/schema.sql` dosyasında tanımlanmıştır. `README.md` dosyası projenin temel bilgilerini içermektedir.

## Gereksinimler ve Uygunluk

Belirtilen proje gereksinimleri ve mevcut projenin uygunluğu aşağıda özetlenmiştir:

- **Teknoloji ve Yazılım Dili**: Python ve Flask kullanılmıştır. **Uygun.**
- **Veritabanı Tablo Sayısı ve İlişkiler**: 8 tablo ve aralarında ilişkiler mevcuttur. **Uygun.**
- **Tablolarda 5N Kuralı**: Mevcut şema iyi bir normalizasyon seviyesine sahiptir. **Uygun (Varsayımsal olarak).**
- **Index, View ve Trigger Kullanımı**: `sql_scripts/schema.sql` dosyasında tanımlanmıştır. **Uygun.**
- **GitHub Platformu ve README**: Proje GitHub'a yüklenecek ve `README.md` güncellenmiştir. **Uygun.**
- **Proje Raporu**: IEEE şablonuna uygun rapor hazırlanacaktır. **Yapılacak.**
- **Teslimat Dosyaları**: Belirtilen formatlarda dosyalar hazırlanacaktır. **Yapılacak.**
- **Arayüz Tasarımı**: Mevcut şablonlar var, görsel inceleme ve iyileştirme gerekebilir. **Gözden Geçirilecek/İyileştirilecek.**
- **Özgünlük**: Projenin özgün yönleri belirlenecektir. **Değerlendirilecek.**

## Önerilen Plan Adımları

Aşağıdaki adımlar, projenin tüm gereksinimleri karşıladığından emin olmak için izlenecektir:

1.  **Veritabanı Şemasını Son Kontrol**:
    *   `sql_scripts/schema.sql` dosyasındaki index, view ve trigger tanımlarının uygulamanın ihtiyaçlarına tam olarak uyduğundan emin olun.
    *   Gerekirse bu dosyada veya migrasyonlarda ek düzenlemeler yapın.
2.  **README.md Dosyasını Gözden Geçir**:
    *   Güncellenen `README.md` dosyasını inceleyin.
    *   Tüm gerekli bilgileri (proje özeti, geliştirme ortamı, kurulum, veritabanı detayları, yapı, özellikler, rapor, teslimat dosyaları) içerdiğinden emin olun.
    *   Arayüz görselleri bölümüne ekran görüntülerinizi ekleyin.
3.  **Proje Raporunu Hazırla**:
    *   IEEE şablonuna uygun proje raporunuzu tamamlayın.
    *   Raporu PDF formatında kaydedin (`grupno_rapor.pdf`). (Bu adım sizin tarafınızdan yapılacaktır.)
4.  **Teslimat Dosyalarını Derle**:
    *   `sql_scripts/schema.sql` dosyasının içeriğini `grupno_sql_betikleri.txt` dosyasına kopyalayın.
    *   Tüm program kod dosyalarınızı (app/ altındaki tüm .py, .html, .css, .js dosyaları, config.py, run.py, ilk_veriler.py vb.) tek bir `grupno_kaynakkod.txt` dosyasında birleştirin.
    *   GitHub deponuzun URL'sini içeren bir `grupno_github.txt` dosyası oluşturun. (Bu adım sizin tarafınızdan yapılacaktır.)
5.  **Arayüz Tasarımını İyileştir**:
    *   Kullanıcı arayüzünüzü (HTML şablonları ve CSS) değerlendirme kriterlerine göre gözden geçirin.
    *   Kullanıcı deneyimini ve görsel çekiciliği artırmak için gerekli iyileştirmeleri yapın. (Bu adım sizin tarafınızdan yapılacaktır.)
6.  **Özgünlüğü Değerlendir**:
    *   Projenizin özgün yönlerini belirleyin.
    *   Bu özgünlükleri proje raporunuzda vurgulayın. (Bu adım sizin tarafınızdan yapılacaktır.)
7.  **GitHub'a Yükle**:
    *   Projenizin son halini (güncellenmiş README, rapor, teslimat dosyaları dahil) GitHub deponuza yükleyin. (Bu adım sizin tarafınızdan yapılacaktır.)

Bu plan, projenizi başarıyla tamamlamanız ve teslimat gereksinimlerini karşılamanız için bir yol haritası sunmaktadır.