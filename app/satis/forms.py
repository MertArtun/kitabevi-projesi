from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Optional, NumberRange
from app.models import Musteri, Kitap

class MusteriSecForm(FlaskForm):
    musteri_id = SelectField('Müşteri', coerce=int, validators=[Optional()])
    misafir = SelectField('Misafir Satışı', choices=[(0, 'Hayır'), (1, 'Evet')], coerce=int, default=0)
    submit = SubmitField('Devam Et')

    def __init__(self, *args, **kwargs):
        super(MusteriSecForm, self).__init__(*args, **kwargs)
        self.musteri_id.choices = [(0, 'Müşteri Seçin')] + [(m.MusteriID, f"{m.Ad} {m.Soyad}") for m in Musteri.query.order_by(Musteri.Ad).all()]

class YeniMusteriForm(FlaskForm):
    ad = StringField('Ad', validators=[DataRequired()])
    soyad = StringField('Soyad', validators=[DataRequired()])
    email = StringField('Email')
    telefon = StringField('Telefon')
    submit = SubmitField('Kaydet')

class SepeteEkleForm(FlaskForm):
    kitap_id = SelectField('Kitap', coerce=int, validators=[DataRequired()])
    adet = IntegerField('Adet', validators=[DataRequired(), NumberRange(min=1)], default=1)
    submit = SubmitField('Sepete Ekle')

    def __init__(self, *args, **kwargs):
        super(SepeteEkleForm, self).__init__(*args, **kwargs)
        self.kitap_id.choices = [(k.KitapID, f"{k.Ad} - {k.Fiyat} TL") for k in Kitap.query.filter(Kitap.StokAdedi > 0).order_by(Kitap.Ad)]

class SatisTamamlaForm(FlaskForm):
    musteri_id = HiddenField('Müşteri ID')
    submit = SubmitField('Satışı Tamamla')