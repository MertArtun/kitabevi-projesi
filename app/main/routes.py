from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from app.main import bp
from app.models import Kitap, Yazar, Yayinevi, Kategori, Musteri, Satis

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
    
    return render_template('index.html', 
                          title='Ana Sayfa',
                          kitap_sayisi=kitap_sayisi,
                          yazar_sayisi=yazar_sayisi,
                          musteri_sayisi=musteri_sayisi,
                          satis_sayisi=satis_sayisi,
                          recent_sales=recent_sales,
                          low_stock_books=low_stock_books)