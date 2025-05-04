from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.kitaplar import bp
from app.kitaplar.forms import KitapForm, YazarForm, YayineviForm, KategoriForm
from app.models import Kitap, Yazar, Yayinevi, Kategori

@bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    kitaplar = Kitap.query.order_by(Kitap.Ad).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('kitaplar/liste.html', title='Kitaplar', 
                           kitaplar=kitaplar)

@bp.route('/yeni', methods=['GET', 'POST'])
@login_required
def yeni_kitap():
    form = KitapForm()
    if form.validate_on_submit():
        kitap = Kitap(ISBN=form.isbn.data,
                     Ad=form.ad.data,
                     YayinYili=form.yayin_yili.data,
                     SayfaSayisi=form.sayfa_sayisi.data,
                     Fiyat=form.fiyat.data,
                     StokAdedi=form.stok_adedi.data,
                     YayineviID=form.yayinevi_id.data,
                     KategoriID=form.kategori_id.data)
        
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
    return render_template('kitaplar/form.html', title='Kitap Düzenle', form=form)

@bp.route('/sil/<int:id>', methods=['POST'])
@login_required
def sil_kitap(id):
    kitap = Kitap.query.get_or_404(id)
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
    return render_template('kitaplar/yazar_form.html', title='Yeni Yazar', form=form)

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
    
    return render_template('kitaplar/yazar_form.html', title='Yazar Düzenle', form=form)

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
    return render_template('kitaplar/yayinevi_form.html', title='Yeni Yayınevi', form=form)

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
    
    return render_template('kitaplar/yayinevi_form.html', title='Yayınevi Düzenle', form=form)

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
    return render_template('kitaplar/kategori_form.html', title='Yeni Kategori', form=form)

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
    
    return render_template('kitaplar/kategori_form.html', title='Kategori Düzenle', form=form)

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
