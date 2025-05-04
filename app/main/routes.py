from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from app.main import bp
from app.models import Kitap, Yazar, Yayinevi, Kategori, Musteri, Satis
import calendar
from datetime import datetime, timedelta
from sqlalchemy import func

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
    
    # Son 6 ayın satış istatistikleri
    son_6_ay = []
    ay_isimleri = []
    aylik_satis_sayilari = []
    
    # Şu anki aydan geriye doğru 6 ay
    suanki_tarih = datetime.now()
    
    for i in range(5, -1, -1):
        # İlgili ayın başlangıç ve bitiş tarihleri
        tarih = (suanki_tarih.replace(day=1) - timedelta(days=1)).replace(day=1)
        tarih = tarih.replace(month=((suanki_tarih.month - i - 1) % 12) + 1)
        
        # Eğer yıl değişiyorsa yılı güncelle
        if suanki_tarih.month - i <= 0:
            tarih = tarih.replace(year=suanki_tarih.year - 1)
        else:
            tarih = tarih.replace(year=suanki_tarih.year)
            
        sonraki_ay = tarih.replace(month=tarih.month % 12 + 1)
        if tarih.month == 12:
            sonraki_ay = sonraki_ay.replace(year=tarih.year + 1)
        
        # İlgili aydaki satış sayısı
        ay_satis_sayisi = Satis.query.filter(
            Satis.SatisTarihi >= tarih,
            Satis.SatisTarihi < sonraki_ay
        ).count()
        
        # Türkçe ay ismi
        ay_ismi = calendar.month_name[tarih.month]
        ay_isimleri.append(f"{ay_ismi[:3]} {tarih.year}")
        aylik_satis_sayilari.append(ay_satis_sayisi)
    
    return render_template('index.html', 
                          title='Ana Sayfa',
                          kitap_sayisi=kitap_sayisi,
                          yazar_sayisi=yazar_sayisi,
                          musteri_sayisi=musteri_sayisi,
                          satis_sayisi=satis_sayisi,
                          recent_sales=recent_sales,
                          low_stock_books=low_stock_books,
                          ay_isimleri=ay_isimleri,
                          aylik_satis_sayilari=aylik_satis_sayilari)