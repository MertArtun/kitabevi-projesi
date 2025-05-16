from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Optional
from app.models import Personel, Kategori

class PersonelForm(FlaskForm):
    KullaniciAdi = StringField('Kullanıcı Adı', validators=[DataRequired(), Length(min=4, max=50)])
    Ad = StringField('Ad', validators=[DataRequired(), Length(max=100)])
    Soyad = StringField('Soyad', validators=[DataRequired(), Length(max=100)])
    Rol = SelectField('Rol', choices=[('Personel', 'Personel'), ('Admin', 'Admin')], validators=[DataRequired()])
    Sifre = PasswordField('Şifre', validators=[DataRequired(), Length(min=6)])
    SifreTekrar = PasswordField('Şifre Tekrar', validators=[DataRequired(), EqualTo('Sifre', message='Şifreler eşleşmiyor.')])
    Sifre = PasswordField('Yeni Şifre (Değiştirmek istemiyorsanız boş bırakın)', validators=[Optional(), Length(min=6)])
    SifreTekrar = PasswordField('Yeni Şifre Tekrar', validators=[EqualTo('Sifre', message='Şifreler eşleşmiyor.')])
    submit = SubmitField('Kaydet')

    # Düzenleme sırasında orijinal kullanıcı adını tutmak için
    original_username = None

    # Kullanıcı adı doğrulamasını düzenlemeye uygun hale getir
    def validate_KullaniciAdi(self, KullaniciAdi):
        # Eğer kullanıcı adı değişmediyse veya orijinali atanmadıysa kontrole gerek yok
        if self.original_username and KullaniciAdi.data == self.original_username:
            return
        personel = Personel.query.filter_by(KullaniciAdi=KullaniciAdi.data).first()
        if personel:
            raise ValidationError('Bu kullanıcı adı zaten kullanılıyor. Lütfen farklı bir kullanıcı adı seçin.')

class KategoriForm(FlaskForm):
    Ad = StringField('Kategori Adı', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Kaydet')

    # Kategori adının benzersizliğini kontrol et (düzenleme için id hariç)
    def __init__(self, original_category_name=None, *args, **kwargs):
        super(KategoriForm, self).__init__(*args, **kwargs)
        self.original_category_name = original_category_name

    def validate_Ad(self, Ad):
        if self.original_category_name and self.original_category_name.lower() == Ad.data.lower():
            return
        kategori = Kategori.query.filter(Kategori.Ad.ilike(Ad.data)).first()
        if kategori:
            raise ValidationError('Bu kategori adı zaten mevcut. Lütfen farklı bir ad seçin.') 