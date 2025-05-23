from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from werkzeug.urls import url_parse
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import Personel

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Personel.query.filter_by(KullaniciAdi=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Geçersiz kullanıcı adı veya şifre')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Giriş', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated and current_user.Rol != 'Admin':
        flash('Yeni personel kaydı oluşturma yetkiniz yok!')
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Personel(KullaniciAdi=form.username.data, 
                       Ad=form.first_name.data,
                       Soyad=form.last_name.data,
                       Rol=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Tebrikler, yeni personel kaydı oluşturuldu!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Kayıt', form=form)