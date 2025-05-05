from flask import render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.kitaplar import bp
from app.kitaplar.forms import KitapForm, YazarForm, YayineviForm, KategoriForm
from app.models import Kitap, Yazar, Yayinevi, Kategori
from sqlalchemy import or_
import os
from werkzeug.utils import secure_filename
import uuid
import shutil
from PIL import Image

# Güvenli dosya adı oluşturma
def save_book_cover(kapak_resmi):
    if not kapak_resmi:
        return 'default_book_cover.jpg'
    
    # Benzersiz dosya adı oluştur
    _, ext = os.path.splitext(kapak_resmi.filename)
    filename = secure_filename(f"{uuid.uuid4()}{ext}")
    
    # Kapak resimleri klasörünü kontrol et/oluştur
    kapak_klasoru = os.path.join(current_app.root_path, 'static', 'img', 'kitap_kapaklari')
    if not os.path.exists(kapak_klasoru):
        os.makedirs(kapak_klasoru)
    
    # Dosyayı kaydet
    kapak_resmi_yolu = os.path.join(kapak_klasoru, filename)
    kapak_resmi.save(kapak_resmi_yolu)
    
    # Resim boyutunu kontrol et ve gerekirse yeniden boyutlandır (opsiyonel)
    try:
        with Image.open(kapak_resmi_yolu) as img:
            # Maksimum boyut: 800x1200
            max_size = (800, 1200)
            if img.width > max_size[0] or img.height > max_size[1]:
                img.thumbnail(max_size, Image.LANCZOS)
                img.save(kapak_resmi_yolu)
    except Exception as e:
        current_app.logger.error(f"Resim işleme hatası: {e}")
    
    return filename

# Varsayılan kapak resmini kontrol et/oluştur
def ensure_default_cover_exists():
    kapak_klasoru = os.path.join(current_app.root_path, 'static', 'img', 'kitap_kapaklari')
    default_kapak = os.path.join(kapak_klasoru, 'default_book_cover.jpg')
    
    # Klasörü kontrol et
    if not os.path.exists(kapak_klasoru):
        os.makedirs(kapak_klasoru)
    
    # Varsayılan kapak resmi yoksa, sistem varsayılanını kullan
    # NOT: Gerçek bir proje için, statik klasörünüzde bir varsayılan resim bulundurmalı ve
    # buraya kopyalamalısınız.
    if not os.path.exists(default_kapak):
        # Basit bir varsayılan resim oluştur (gerçek projede bu statik bir dosyadan kopyalanmalı)
        from PIL import Image, ImageDraw, ImageFont
        
        # 400x600 boyutunda gri bir resim oluştur
        img = Image.new('RGB', (400, 600), color=(240, 240, 240))
        d = ImageDraw.Draw(img)
        
        # Resmin ortasına metin ekle
        try:
            # Standart yazı tipi kullan (sisteme bağlıdır)
            d.text((200, 300), "Kapak Yok", fill=(80, 80, 80), anchor="mm")
        except Exception as e:
            current_app.logger.error(f"Font hatası: {e}")
            # Temel çizim ile basit bir çerçeve çiz
            d.rectangle([(20, 20), (380, 580)], outline=(80, 80, 80), width=2)
            
        # Resmi kaydet
        img.save(default_kapak)

# Uygulama başladığında varsayılan kapak resmini kontrol et
@bp.before_app_first_request
def setup_default_images():
    ensure_default_cover_exists()

@bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('q', '')
    kategori_id = request.args.get('kategori_id', type=int)
    yayinevi_id = request.args.get('yayinevi_id', type=int)
    
    # Temel sorgu
    query = Kitap.query.order_by(Kitap.Ad)
    
    # Arama filtresi
    if search_query:
        query = query.join(Kitap.yazarlar).join(Kitap.yayinevi).join(Kitap.kategori).filter(
            or_(
                Kitap.Ad.ilike(f'%{search_query}%'),
                Kitap.ISBN.ilike(f'%{search_query}%'),
                Yazar.Ad.ilike(f'%{search_query}%'),
                Yazar.Soyad.ilike(f'%{search_query}%'),
                Yayinevi.Ad.ilike(f'%{search_query}%'),
                Kategori.Ad.ilike(f'%{search_query}%')
            )
        ).distinct() # distinct() arama için önemli
        
    # Kategori filtresi
    if kategori_id:
        query = query.filter(Kitap.KategoriID == kategori_id)
        
    # Yayınevi filtresi
    if yayinevi_id:
        query = query.filter(Kitap.YayineviID == yayinevi_id)
        
    # Sayfalama
    kitaplar = query.paginate(page=page, per_page=10, error_out=False)
    
    # Filtreleme için kategorileri ve yayınevlerini al
    kategoriler = Kategori.query.order_by(Kategori.Ad).all()
    yayinevleri = Yayinevi.query.order_by(Yayinevi.Ad).all()
    
    return render_template('kitaplar/liste.html', title='Kitaplar',
                           kitaplar=kitaplar,
                           search_query=search_query,
                           kategoriler=kategoriler,
                           yayinevleri=yayinevleri,
                           selected_kategori=kategori_id,
                           selected_yayinevi=yayinevi_id)

@bp.route('/yeni', methods=['GET', 'POST'])
@login_required
def yeni_kitap():
    form = KitapForm()
    if form.validate_on_submit():
        # Kapak resmi yükleme işlemi
        kapak_resmi_dosyasi = form.kapak_resmi.data
        kapak_resmi_adi = 'default_book_cover.jpg'
        
        if kapak_resmi_dosyasi:
            kapak_resmi_adi = save_book_cover(kapak_resmi_dosyasi)
        
        kitap = Kitap(ISBN=form.isbn.data,
                     Ad=form.ad.data,
                     YayinYili=form.yayin_yili.data,
                     SayfaSayisi=form.sayfa_sayisi.data,
                     Fiyat=form.fiyat.data,
                     StokAdedi=form.stok_adedi.data,
                     YayineviID=form.yayinevi_id.data,
                     KategoriID=form.kategori_id.data,
                     KapakResmi=kapak_resmi_adi)
        
        for yazar_id in form.yazar_ids.data:
            yazar = Yazar.query.get(yazar_id)
            if yazar:
                kitap.yazarlar.append(yazar)
        
        db.session.add(kitap)
        db.session.commit()
        flash('Kitap başarıyla eklendi!')
        return redirect(url_for('kitaplar.index'))
    return render_template('kitaplar/form.html', title='Yeni Kitap', form=form)

@bp.route('/duzenle/<int:id>', methods=['GET', 'POST'])
@login_required
def duzenle_kitap(id):
    kitap = Kitap.query.get_or_404(id)
    form = KitapForm(obj=kitap)
    
    if request.method == 'GET':
        form.yayinevi_id.data = kitap.YayineviID
        form.kategori_id.data = kitap.KategoriID
        form.yazar_ids.data = [yazar.YazarID for yazar in kitap.yazarlar]
    
    if form.validate_on_submit():
        # Kapak resmi yükleme işlemi
        kapak_resmi_dosyasi = form.kapak_resmi.data
        
        if kapak_resmi_dosyasi:
            # Eski kapak resmini silme işlemi (varsayılan değilse)
            if kitap.KapakResmi != 'default_book_cover.jpg':
                eski_kapak_yolu = os.path.join(current_app.root_path, 'static', 'img', 'kitap_kapaklari', kitap.KapakResmi)
                if os.path.exists(eski_kapak_yolu):
                    os.remove(eski_kapak_yolu)
            
            # Yeni kapak resmini kaydet
            kitap.KapakResmi = save_book_cover(kapak_resmi_dosyasi)
        
        kitap.ISBN = form.isbn.data
        kitap.Ad = form.ad.data
        kitap.YayinYili = form.yayin_yili.data
        kitap.SayfaSayisi = form.sayfa_sayisi.data
        kitap.Fiyat = form.fiyat.data
        kitap.StokAdedi = form.stok_adedi.data
        kitap.YayineviID = form.yayinevi_id.data
        kitap.KategoriID = form.kategori_id.data
        
        # Yazarları temizle ve yeniden ekle
        kitap.yazarlar = []
        for yazar_id in form.yazar_ids.data:
            yazar = Yazar.query.get(yazar_id)
            if yazar:
                kitap.yazarlar.append(yazar)
        
        db.session.commit()
        flash('Kitap başarıyla güncellendi!')
        return redirect(url_for('kitaplar.index'))
    return render_template('kitaplar/form.html', title='Kitap Düzenle', form=form, kitap=kitap)

@bp.route('/sil/<int:id>', methods=['POST'])
@login_required
def sil_kitap(id):
    kitap = Kitap.query.get_or_404(id)
    
    # Kapak resmini sil (varsayılan değilse)
    if kitap.KapakResmi and kitap.KapakResmi != 'default_book_cover.jpg':
        kapak_yolu = os.path.join(current_app.root_path, 'static', 'img', 'kitap_kapaklari', kitap.KapakResmi)
        if os.path.exists(kapak_yolu):
            os.remove(kapak_yolu)
    
    db.session.delete(kitap)
    db.session.commit()
    flash('Kitap başarıyla silindi!')
    return redirect(url_for('kitaplar.index'))

# Yazar işlemleri
@bp.route('/yazarlar')
@login_required
def yazarlar():
    yazarlar = Yazar.query.order_by(Yazar.Ad).all()
    return render_template('kitaplar/yazarlar.html', title='Yazarlar', yazarlar=yazarlar)

@bp.route('/yazarlar/yeni', methods=['GET', 'POST'])
@login_required
def yeni_yazar():
    form = YazarForm()
    if form.validate_on_submit():
        yazar = Yazar(Ad=form.ad.data,
                     Soyad=form.soyad.data,
                     Biyografi=form.biyografi.data)
        db.session.add(yazar)
        db.session.commit()
        flash('Yazar başarıyla eklendi!')
        return redirect(url_for('kitaplar.yazarlar'))
    return render_template('kitaplar/yazar_form.html', title='Yeni Yazar Ekle', form=form)

@bp.route('/yazarlar/duzenle/<int:id>', methods=['GET', 'POST'])
@login_required
def duzenle_yazar(id):
    yazar = Yazar.query.get_or_404(id)
    form = YazarForm(obj=yazar)
    
    if form.validate_on_submit():
        yazar.Ad = form.ad.data
        yazar.Soyad = form.soyad.data
        yazar.Biyografi = form.biyografi.data
        
        db.session.commit()
        flash('Yazar başarıyla güncellendi!')
        return redirect(url_for('kitaplar.yazarlar'))
    
    return render_template('kitaplar/yazar_form.html', title=f'Yazar Düzenle: {yazar.Ad} {yazar.Soyad}', form=form)

@bp.route('/yazarlar/sil/<int:id>', methods=['POST'])
@login_required
def sil_yazar(id):
    yazar = Yazar.query.get_or_404(id)
    try:
        db.session.delete(yazar)
        db.session.commit()
        flash('Yazar başarıyla silindi!')
    except Exception as e:
        db.session.rollback()
        flash(f'Hata: Bu yazar bir veya daha fazla kitapla ilişkilendirilmiş olabilir. {str(e)}', 'danger')
    
    return redirect(url_for('kitaplar.yazarlar'))

# Yayınevi işlemleri
@bp.route('/yayinevleri')
@login_required
def yayinevleri():
    yayinevleri = Yayinevi.query.order_by(Yayinevi.Ad).all()
    return render_template('kitaplar/yayinevleri.html', title='Yayınevleri', yayinevleri=yayinevleri)

@bp.route('/yayinevleri/yeni', methods=['GET', 'POST'])
@login_required
def yeni_yayinevi():
    form = YayineviForm()
    if form.validate_on_submit():
        yayinevi = Yayinevi(Ad=form.ad.data,
                          Adres=form.adres.data,
                          Telefon=form.telefon.data)
        db.session.add(yayinevi)
        db.session.commit()
        flash('Yayınevi başarıyla eklendi!')
        return redirect(url_for('kitaplar.yayinevleri'))
    return render_template('kitaplar/yayinevi_form.html', title='Yeni Yayınevi Ekle', form=form)

@bp.route('/yayinevleri/duzenle/<int:id>', methods=['GET', 'POST'])
@login_required
def duzenle_yayinevi(id):
    yayinevi = Yayinevi.query.get_or_404(id)
    form = YayineviForm(obj=yayinevi)
    
    if form.validate_on_submit():
        yayinevi.Ad = form.ad.data
        yayinevi.Adres = form.adres.data
        yayinevi.Telefon = form.telefon.data
        
        db.session.commit()
        flash('Yayınevi başarıyla güncellendi!')
        return redirect(url_for('kitaplar.yayinevleri'))
    
    return render_template('kitaplar/yayinevi_form.html', title=f'Yayınevi Düzenle: {yayinevi.Ad}', form=form)

@bp.route('/yayinevleri/sil/<int:id>', methods=['POST'])
@login_required
def sil_yayinevi(id):
    yayinevi = Yayinevi.query.get_or_404(id)
    try:
        db.session.delete(yayinevi)
        db.session.commit()
        flash('Yayınevi başarıyla silindi!')
    except Exception as e:
        db.session.rollback()
        flash(f'Hata: Bu yayınevi bir veya daha fazla kitapla ilişkilendirilmiş olabilir. {str(e)}', 'danger')
    
    return redirect(url_for('kitaplar.yayinevleri'))

# Kategori işlemleri
@bp.route('/kategoriler')
@login_required
def kategoriler():
    kategoriler = Kategori.query.order_by(Kategori.Ad).all()
    return render_template('kitaplar/kategoriler.html', title='Kategoriler', kategoriler=kategoriler)

@bp.route('/kategoriler/yeni', methods=['GET', 'POST'])
@login_required
def yeni_kategori():
    form = KategoriForm()
    if form.validate_on_submit():
        kategori = Kategori(Ad=form.ad.data)
        db.session.add(kategori)
        db.session.commit()
        flash('Kategori başarıyla eklendi!')
        return redirect(url_for('kitaplar.kategoriler'))
    return render_template('kitaplar/kategori_form.html', title='Yeni Kategori Ekle', form=form)

@bp.route('/kategoriler/duzenle/<int:id>', methods=['GET', 'POST'])
@login_required
def duzenle_kategori(id):
    kategori = Kategori.query.get_or_404(id)
    form = KategoriForm(obj=kategori)
    
    if form.validate_on_submit():
        kategori.Ad = form.ad.data
        
        db.session.commit()
        flash('Kategori başarıyla güncellendi!')
        return redirect(url_for('kitaplar.kategoriler'))
    
    return render_template('kitaplar/kategori_form.html', title=f'Kategori Düzenle: {kategori.Ad}', form=form)

@bp.route('/kategoriler/sil/<int:id>', methods=['POST'])
@login_required
def sil_kategori(id):
    kategori = Kategori.query.get_or_404(id)
    try:
        db.session.delete(kategori)
        db.session.commit()
        flash('Kategori başarıyla silindi!')
    except Exception as e:
        db.session.rollback()
        flash(f'Hata: Bu kategori bir veya daha fazla kitapla ilişkilendirilmiş olabilir. {str(e)}', 'danger')
    
    return redirect(url_for('kitaplar.kategoriler'))

@bp.route('/api/arama')
@login_required
def api_arama():
    search_query = request.args.get('q', '')
    if not search_query or len(search_query) < 2:
        return jsonify([])
    
    # Kitapları sorgula
    kitaplar = Kitap.query.join(Kitap.yazarlar).join(Kitap.yayinevi).join(Kitap.kategori).filter(
        or_(
            Kitap.Ad.ilike(f'%{search_query}%'),
            Kitap.ISBN.ilike(f'%{search_query}%'),
            Yazar.Ad.ilike(f'%{search_query}%'),
            Yazar.Soyad.ilike(f'%{search_query}%'),
            Yayinevi.Ad.ilike(f'%{search_query}%'),
            Kategori.Ad.ilike(f'%{search_query}%')
        )
    ).distinct().limit(10).all()
    
    results = []
    for kitap in kitaplar:
        yazarlar = [f"{yazar.Ad} {yazar.Soyad}" for yazar in kitap.yazarlar]
        results.append({
            'id': kitap.KitapID,
            'title': kitap.Ad,
            'isbn': kitap.ISBN,
            'authors': ', '.join(yazarlar),
            'publisher': kitap.yayinevi.Ad if kitap.yayinevi else '',
            'category': kitap.kategori.Ad if kitap.kategori else '',
            'price': str(kitap.Fiyat),
            'stock': kitap.StokAdedi
        })
    
    return jsonify(results)
