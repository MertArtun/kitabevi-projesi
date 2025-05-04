from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import Personel

class LoginForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired()])
    password = PasswordField('Şifre', validators=[DataRequired()])
    remember_me = BooleanField('Beni Hatırla')
    submit = SubmitField('Giriş Yap')

class RegistrationForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired()])
    first_name = StringField('Ad', validators=[DataRequired()])
    last_name = StringField('Soyad', validators=[DataRequired()])
    password = PasswordField('Şifre', validators=[DataRequired()])
    password2 = PasswordField(
        'Şifreyi Tekrarla', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Rol', choices=[('Admin', 'Admin'), ('Kasiyer', 'Kasiyer')])
    submit = SubmitField('Kayıt Ol')

    def validate_username(self, username):
        user = Personel.query.filter_by(KullaniciAdi=username.data).first()
        if user is not None:
            raise ValidationError('Lütfen başka bir kullanıcı adı seçin.')