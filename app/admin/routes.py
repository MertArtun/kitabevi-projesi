from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.admin import bp
# Henüz oluşturmadık ama buraya ekleyeceğiz:
# from app.decorators import admin_required
from app.decorators import admin_required
from app import db
from app.models import Personel, Kitap, Musteri, Satis, Kategori, Yayinevi, Yazar
from app.admin.forms import PersonelForm, KategoriForm
from flask_login import current_user

@bp.route('/')
@admin_required
@login_required
def index():
    # İlk başta basit bir admin ana sayfası gösterelim
    personel_sayisi = Personel.query.count()
    kitap_sayisi = Kitap.query.count()
    musteri_sayisi = Musteri.query.count()
    satis_sayisi = Satis.query.count()
    return render_template('admin/index.html', title='Admin Paneli',
                           personel_sayisi=personel_sayisi,
                           kitap_sayisi=kitap_sayisi,
                           musteri_sayisi=musteri_sayisi,
                           satis_sayisi=satis_sayisi)

@bp.route('/personel')
@admin_required
def personel_listesi():
    personeller = Personel.query.order_by(Personel.PersonelID).all()
    return render_template('admin/personel_listesi.html', title='Personel Yönetimi', personeller=personeller)

@bp.route('/personel/ekle', methods=['GET', 'POST'])
@admin_required
def personel_ekle():
    form = PersonelForm()
    if form.validate_on_submit():
        yeni_personel = Personel(
            KullaniciAdi=form.KullaniciAdi.data,
            Ad=form.Ad.data,
            Soyad=form.Soyad.data,
            Rol=form.Rol.data
        )
        yeni_personel.set_password(form.Sifre.data)
        db.session.add(yeni_personel)
        db.session.commit()
        flash('Yeni personel başarıyla eklendi.', 'success')
        return redirect(url_for('admin.personel_listesi'))
    return render_template('admin/personel_form.html', title='Yeni Personel Ekle', form=form)

@bp.route('/personel/duzenle/<int:personel_id>', methods=['GET', 'POST'])
@admin_required
def personel_duzenle(personel_id):
    personel = Personel.query.get_or_404(personel_id)
    form = PersonelForm()
    # Kullanıcı adı doğrulamasını atlamak için orijinal kullanıcı adını forma ata
    form.original_username = personel.KullaniciAdi

    if form.validate_on_submit():
        personel.KullaniciAdi = form.KullaniciAdi.data
        personel.Ad = form.Ad.data
        personel.Soyad = form.Soyad.data
        personel.Rol = form.Rol.data
        # Eğer yeni şifre girildiyse güncelle
        if form.Sifre.data:
            personel.set_password(form.Sifre.data)
        db.session.commit()
        flash('Personel bilgileri başarıyla güncellendi.', 'success')
        return redirect(url_for('admin.personel_listesi'))
    elif request.method == 'GET':
        # Formu mevcut personel bilgileriyle doldur
        form.KullaniciAdi.data = personel.KullaniciAdi
        form.Ad.data = personel.Ad
        form.Soyad.data = personel.Soyad
        form.Rol.data = personel.Rol
        # Şifre alanları boş bırakılır

    return render_template('admin/personel_form.html', title='Personel Düzenle', form=form)

@bp.route('/personel/sil/<int:personel_id>', methods=['POST'])
@admin_required
def personel_sil(personel_id):
    personel = Personel.query.get_or_404(personel_id)

    # Kendini silmeyi engelle
    if personel.PersonelID == current_user.PersonelID:
        flash('Kendinizi silemezsiniz.', 'danger')
        return redirect(url_for('admin.personel_listesi'))

    # Ana admini (varsa, ID=1) silmeyi engelle (isteğe bağlı, güvenlik için)
    if personel.KullaniciAdi == 'admin': # veya if personel.PersonelID == 1:
        flash('Ana admin kullanıcısı silinemez.', 'danger')
        return redirect(url_for('admin.personel_listesi'))

    db.session.delete(personel)
    db.session.commit()
    flash('Personel başarıyla silindi.', 'success')
    return redirect(url_for('admin.personel_listesi'))

@bp.route('/kitap')
@admin_required
def kitap_listesi():
    kitaplar = Kitap.query.order_by(Kitap.KitapID).all()
    return render_template('admin/kitap_listesi.html', title='Kitap Yönetimi', kitaplar=kitaplar)

@bp.route('/kategori')
@admin_required
def kategori_listesi():
    kategoriler = Kategori.query.order_by(Kategori.KategoriID).all()
    form = KategoriForm()
    return render_template('admin/kategori_listesi.html', title='Kategori Yönetimi', kategoriler=kategoriler, form=form)

@bp.route('/kategori/ekle', methods=['GET', 'POST'])
@admin_required
def kategori_ekle():
    form = KategoriForm()
    if form.validate_on_submit():
        yeni_kategori = Kategori(Ad=form.Ad.data)
        db.session.add(yeni_kategori)
        db.session.commit()
        flash('Yeni kategori başarıyla eklendi.', 'success')
        return redirect(url_for('admin.kategori_listesi'))
    return render_template('admin/kategori_form.html', title='Yeni Kategori Ekle', form=form)

@bp.route('/kategori/duzenle/<int:kategori_id>', methods=['GET', 'POST'])
@admin_required
def kategori_duzenle(kategori_id):
    kategori = Kategori.query.get_or_404(kategori_id)
    form = KategoriForm(original_category_name=kategori.Ad)
    if form.validate_on_submit():
        kategori.Ad = form.Ad.data
        db.session.commit()
        flash('Kategori başarıyla güncellendi.', 'success')
        return redirect(url_for('admin.kategori_listesi'))
    elif request.method == 'GET':
        form.Ad.data = kategori.Ad
    return render_template('admin/kategori_form.html', title='Kategori Düzenle', form=form, kategori=kategori)

@bp.route('/kategori/sil/<int:kategori_id>', methods=['POST'])
@admin_required
def kategori_sil(kategori_id):
    kategori = Kategori.query.get_or_404(kategori_id)
    if kategori.kitaplar.count() > 0:
        flash('Bu kategoriye ait kitaplar olduğu için silinemez. Önce ilgili kitapları başka bir kategoriye taşıyın veya silin.', 'danger')
        return redirect(url_for('admin.kategori_listesi'))
    db.session.delete(kategori)
    db.session.commit()
    flash('Kategori başarıyla silindi.', 'success')
    return redirect(url_for('admin.kategori_listesi'))

@bp.route('/yayinevi')
@admin_required
def yayinevi_listesi():
    yayinevleri = Yayinevi.query.order_by(Yayinevi.YayineviID).all()
    return render_template('admin/yayinevi_listesi.html', title='Yayınevi Yönetimi', yayinevleri=yayinevleri)

@bp.route('/musteri')
@admin_required
def musteri_listesi():
    musteriler = Musteri.query.order_by(Musteri.MusteriID).all()
    return render_template('admin/musteri_listesi.html', title='Müşteri Yönetimi', musteriler=musteriler)

@bp.route('/raporlar')
@admin_required
def satis_raporlari():
    toplam_satis = Satis.query.count()
    toplam_tutar = db.session.query(db.func.sum(Satis.ToplamTutar)).scalar() or 0
    return render_template('admin/satis_raporlari.html', title='Satış Raporları', toplam_satis=toplam_satis, toplam_tutar=toplam_tutar) 