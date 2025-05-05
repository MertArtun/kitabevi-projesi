from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.main import bp
from app.models import Kitap, Yazar, Yayinevi, Kategori, Musteri, Satis, SatisDetay
import calendar
from datetime import datetime, timedelta
from sqlalchemy import func, desc # desc import edildi

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    # İstatistikler
    kitap_sayisi = Kitap.query.count()
    yazar_sayisi = Yazar.query.count()
    musteri_sayisi = Musteri.query.count()
    satis_sayisi = Satis.query.count()
    
    # Son 5 satış
    recent_sales = Satis.query.order_by(Satis.SatisTarihi.desc()).limit(5).all()
    
    # Stok sayısı 5'ten az olan kitaplar
    low_stock_books = Kitap.query.filter(Kitap.StokAdedi <= 5).all()
    
    # Son Eklenen Kitaplar (Son 5 kitap)
    latest_books = Kitap.query.order_by(Kitap.KitapID.desc()).limit(5).all() # EklenmeTarihi yerine KitapID kullanıldı
    
    # En Çok Satan Kitaplar (Son 6 ayda en çok satılan 5 kitap)
    # SatisDetay tablosundan kitap ID'lerini gruplayarak toplam miktarı hesapla
    top_selling_books = db.session.query(
        Kitap,
        func.sum(SatisDetay.Adet).label('total_sold') # Miktar yerine Adet kullanıldı
    ).join(SatisDetay).join(Satis).filter(
        Satis.SatisTarihi >= datetime.now() - timedelta(days=180) # Son 6 ay
    ).group_by(Kitap).order_by(func.sum(SatisDetay.Adet).desc()).limit(5).all() # Miktar yerine Adet kullanıldı
    
    # Son 6 ayın satış istatistikleri (Aylık)
    ay_isimleri_son_6 = []
    aylik_satis_sayilari_son_6 = []
    today = datetime.now()
    
    for i in range(6):
        # Ayın başlangıcını ve bitişini hesapla
        target_month_date = today.replace(day=1) - timedelta(days=i*30) # Yaklaşık hesaplama
        month_start = target_month_date.replace(day=1)
        
        # Bir sonraki ayın başlangıcını bul (ayın sonunu belirlemek için)
        next_month_start_year = month_start.year
        next_month_start_month = month_start.month + 1
        if next_month_start_month > 12:
            next_month_start_month = 1
            next_month_start_year += 1
        month_end = datetime(next_month_start_year, next_month_start_month, 1)

        # İlgili aydaki satış sayısı
        ay_satis_sayisi = Satis.query.filter(
            Satis.SatisTarihi >= month_start,
            Satis.SatisTarihi < month_end
        ).count()
        
        # Türkçe ay ismi ve yıl
        ay_ismi = calendar.month_name[month_start.month]
        ay_isimleri_son_6.append(f"{ay_ismi} {month_start.year}")
        aylik_satis_sayilari_son_6.append(ay_satis_sayisi)
        
    # Listeleri ters çevirerek kronolojik sıra elde et
    ay_isimleri_son_6.reverse()
    aylik_satis_sayilari_son_6.reverse()

    # Kategoriye göre satış adetleri (Son 6 ay)
    six_months_ago = datetime.now() - timedelta(days=180)
    kategori_satis_verileri = db.session.query(
        Kategori.Ad,
        func.sum(SatisDetay.Adet).label('toplam_adet')
    ).join(Kitap, Kitap.KategoriID == Kategori.KategoriID)\
     .join(SatisDetay, SatisDetay.KitapID == Kitap.KitapID)\
     .join(Satis, Satis.SatisID == SatisDetay.SatisID)\
     .filter(Satis.SatisTarihi >= six_months_ago)\
     .group_by(Kategori.Ad)\
     .order_by(desc('toplam_adet'))\
     .limit(7).all() # En çok satan 7 kategoriyi alalım (pasta grafikte daha iyi görünebilir)

    kategori_isimleri = [veri[0] for veri in kategori_satis_verileri]
    kategori_satis_adetleri = [int(veri[1]) for veri in kategori_satis_verileri] # Integer'a çevir
    
    return render_template('index.html', title='Ana Sayfa',
                           kitap_sayisi=kitap_sayisi, yazar_sayisi=yazar_sayisi,
                           musteri_sayisi=musteri_sayisi, satis_sayisi=satis_sayisi,
                           recent_sales=recent_sales, low_stock_books=low_stock_books,
                           latest_books=latest_books, top_selling_books=top_selling_books,
                           ay_isimleri=ay_isimleri_son_6, # Güncellendi
                           aylik_satis_sayilari=aylik_satis_sayilari_son_6, # Güncellendi
                           kategori_isimleri=kategori_isimleri, # Yeni veri
                           kategori_satis_adetleri=kategori_satis_adetleri) # Yeni veri