from flask import render_template, redirect, url_for, flash, request, session, make_response
from flask_login import login_required, current_user
from flask_weasyprint import HTML, render_pdf
from app import db
from app.satis import bp
from app.satis.forms import MusteriSecForm, YeniMusteriForm, SepeteEkleForm, SatisTamamlaForm
from app.models import Kitap, Musteri, Satis, SatisDetay
from datetime import datetime

@bp.route('/yeni', methods=['GET', 'POST'])
@login_required
def yeni():
    form = MusteriSecForm()
    if form.validate_on_submit():
        if form.misafir.data == 1:
            session['musteri_id'] = None
            return redirect(url_for('satis.sepet'))
        elif form.musteri_id.data > 0:
            session['musteri_id'] = form.musteri_id.data
            return redirect(url_for('satis.sepet'))
        else:
            flash('Lütfen bir müşteri seçin veya misafir satışı yapın.')
    return render_template('satis/musteri_sec.html', title='Müşteri Seç', form=form)

@bp.route('/yeni_musteri', methods=['GET', 'POST'])
@login_required
def yeni_musteri():
    form = YeniMusteriForm()
    if form.validate_on_submit():
        musteri = Musteri(Ad=form.ad.data,
                         Soyad=form.soyad.data,
                         Email=form.email.data,
                         Telefon=form.telefon.data)
        db.session.add(musteri)
        db.session.commit()
        session['musteri_id'] = musteri.MusteriID
        flash('Yeni müşteri başarıyla eklendi!')
        return redirect(url_for('satis.sepet'))
    return render_template('satis/yeni_musteri.html', title='Yeni Müşteri', form=form)

@bp.route('/sepet', methods=['GET', 'POST'])
@login_required
def sepet():
    if 'sepet' not in session:
        session['sepet'] = []
    
    form = SepeteEkleForm()
    
    if form.validate_on_submit():
        kitap = Kitap.query.get(form.kitap_id.data)
        if kitap and kitap.StokAdedi >= form.adet.data:
            # Kitap zaten sepette var mı kontrol et
            sepet_kitap = next((item for item in session['sepet'] if item['kitap_id'] == kitap.KitapID), None)
            if sepet_kitap:
                sepet_kitap['adet'] += form.adet.data
                sepet_kitap['toplam'] = float(sepet_kitap['adet'] * sepet_kitap['birim_fiyat'])
            else:
                session['sepet'].append({
                    'kitap_id': kitap.KitapID,
                    'baslik': kitap.Ad,
                    'birim_fiyat': float(kitap.Fiyat),
                    'adet': form.adet.data,
                    'toplam': float(kitap.Fiyat * form.adet.data)
                })
            session.modified = True
            flash(f'"{kitap.Ad}" sepete eklendi!')
        else:
            flash('Yetersiz stok!')
    
    # Sepet toplamını hesapla
    toplam_tutar = sum(item['toplam'] for item in session['sepet'])
    
    tamamla_form = SatisTamamlaForm()
    tamamla_form.musteri_id.data = session.get('musteri_id')
    
    return render_template('satis/sepet.html', title='Sepet', 
                          form=form, tamamla_form=tamamla_form,
                          sepet=session['sepet'], toplam=toplam_tutar)

@bp.route('/sepetten_cikar/<int:kitap_id>', methods=['POST'])
@login_required
def sepetten_cikar(kitap_id):
    if 'sepet' in session:
        session['sepet'] = [item for item in session['sepet'] if item['kitap_id'] != kitap_id]
        session.modified = True
        flash('Ürün sepetten çıkarıldı!')
    return redirect(url_for('satis.sepet'))

@bp.route('/tamamla', methods=['POST'])
@login_required
def tamamla():
    if 'sepet' not in session or not session['sepet']:
        flash('Sepetiniz boş!')
        return redirect(url_for('satis.sepet'))
    
    form = SatisTamamlaForm()
    if form.validate_on_submit():
        musteri_id = form.musteri_id.data if form.musteri_id.data else None
        toplam_tutar = sum(item['toplam'] for item in session['sepet'])
        
        # Satış oluştur
        satis = Satis(MusteriID=musteri_id,
                     ToplamTutar=toplam_tutar,
                     PersonelID=current_user.PersonelID)
        db.session.add(satis)
        db.session.flush()  # ID'yi almak için veritabanını güncelle
        
        # Satış detayları oluştur
        for item in session['sepet']:
            detay = SatisDetay(SatisID=satis.SatisID,
                             KitapID=item['kitap_id'],
                             Adet=item['adet'],
                             BirimFiyat=item['birim_fiyat'])
            db.session.add(detay)
        
        try:
            db.session.commit()
            flash('Satış başarıyla tamamlandı!')
            # Sepeti temizle
            session.pop('sepet', None)
            session.pop('musteri_id', None)
            return redirect(url_for('satis.detay', id=satis.SatisID))
        except Exception as e:
            db.session.rollback()
            flash(f'Hata oluştu: {str(e)}')
            return redirect(url_for('satis.sepet'))
    
    return redirect(url_for('satis.sepet'))

@bp.route('/detay/<int:id>')
@login_required
def detay(id):
    satis = Satis.query.get_or_404(id)
    return render_template('satis/detay.html', title='Satış Detayı', satis=satis)

@bp.route('/detay/<int:id>/pdf')
@login_required
def detay_pdf(id):
    satis = Satis.query.get_or_404(id)
    
    # PDF şablonunu oluştur
    html = render_template('satis/pdf_rapor.html', 
                          satis=satis,
                          tarih=datetime.now().strftime('%d.%m.%Y %H:%M'))
    
    # PDF dosyasını oluştur
    response = make_response(render_pdf(HTML(string=html)))
    
    # Dosya adı belirle
    filename = f"satis_rapor_{satis.SatisID}_{datetime.now().strftime('%Y%m%d%H%M')}.pdf"
    
    # Tarayıcıya indirilecek dosya olarak belirt
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response

@bp.route('/listele')
@login_required
def listele():
    page = request.args.get('page', 1, type=int)
    satislar = Satis.query.order_by(Satis.SatisTarihi.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('satis/liste.html', title='Satışlar', satislar=satislar)