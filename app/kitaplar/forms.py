from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, TextAreaField, SelectField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length
from app.models import Yayinevi, Kategori, Yazar

class KitapForm(FlaskForm):
    isbn = StringField('ISBN', validators=[DataRequired(), Length(min=10, max=13)])
    ad = StringField('Kitap Adı', validators=[DataRequired(), Length(max=255)])
    yayin_yili = IntegerField('Yayın Yılı', validators=[NumberRange(min=1000, max=2100)], default=2023)
    sayfa_sayisi = IntegerField('Sayfa Sayısı', validators=[NumberRange(min=1)])
    fiyat = DecimalField('Fiyat (TL)', validators=[DataRequired(), NumberRange(min=0)], places=2)
    stok_adedi = IntegerField('Stok Adedi', validators=[DataRequired(), NumberRange(min=0)], default=0)
    yayinevi_id = SelectField('Yayınevi', coerce=int, validators=[DataRequired()])
    kategori_id = SelectField('Kategori', coerce=int, validators=[DataRequired()])
    yazar_ids = SelectMultipleField('Yazarlar', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Kaydet')

    def __init__(self, *args, **kwargs):
        super(KitapForm, self).__init__(*args, **kwargs)
        self.yayinevi_id.choices = [(y.YayineviID, y.Ad) for y in Yayinevi.query.order_by(Yayinevi.Ad).all()]
        self.kategori_id.choices = [(k.KategoriID, k.Ad) for k in Kategori.query.order_by(Kategori.Ad).all()]
        self.yazar_ids.choices = [(y.YazarID, f"{y.Ad} {y.Soyad}") for y in Yazar.query.order_by(Yazar.Ad).all()]

class YazarForm(FlaskForm):
    ad = StringField('Ad', validators=[DataRequired(), Length(max=100)])
    soyad = StringField('Soyad', validators=[DataRequired(), Length(max=100)])
    biyografi = TextAreaField('Biyografi')
    submit = SubmitField('Kaydet')

class YayineviForm(FlaskForm):
    ad = StringField('Ad', validators=[DataRequired(), Length(max=255)])
    adres = TextAreaField('Adres')
    telefon = StringField('Telefon', validators=[Length(max=20)])
    submit = SubmitField('Kaydet')

class KategoriForm(FlaskForm):
    ad = StringField('Ad', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Kaydet')