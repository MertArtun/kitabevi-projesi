from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login

# Yazar-Kitap ilişki tablosu (Çoka çok ilişki)
kitap_yazar = db.Table('KitapYazarlari',
    db.Column('KitapID', db.Integer, db.ForeignKey('Kitaplar.KitapID'), primary_key=True),
    db.Column('YazarID', db.Integer, db.ForeignKey('Yazarlar.YazarID'), primary_key=True)
)

class Yazar(db.Model):
    __tablename__ = 'Yazarlar'
    YazarID = db.Column(db.Integer, primary_key=True)
    Ad = db.Column(db.String(100), nullable=False)
    Soyad = db.Column(db.String(100), nullable=False)
    Biyografi = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<Yazar {self.Ad} {self.Soyad}>'

class Yayinevi(db.Model):
    __tablename__ = 'Yayinevleri'
    YayineviID = db.Column(db.Integer, primary_key=True)
    Ad = db.Column(db.String(255), nullable=False, unique=True)
    Adres = db.Column(db.Text, nullable=True)
    Telefon = db.Column(db.String(20), nullable=True)
    
    kitaplar = db.relationship('Kitap', backref='yayinevi', lazy='dynamic')
    
    def __repr__(self):
        return f'<Yayinevi {self.Ad}>'

class Kategori(db.Model):
    __tablename__ = 'Kategoriler'
    KategoriID = db.Column(db.Integer, primary_key=True)
    Ad = db.Column(db.String(100), nullable=False, unique=True)
    
    kitaplar = db.relationship('Kitap', backref='kategori', lazy='dynamic')
    
    def __repr__(self):
        return f'<Kategori {self.Ad}>'

class Kitap(db.Model):
    __tablename__ = 'Kitaplar'
    KitapID = db.Column(db.Integer, primary_key=True)
    ISBN = db.Column(db.String(13), nullable=False, unique=True)
    Ad = db.Column(db.String(255), nullable=False)
    YayinYili = db.Column(db.Integer, nullable=True)
    SayfaSayisi = db.Column(db.Integer, nullable=True)
    Fiyat = db.Column(db.Numeric(10, 2), nullable=False)
    StokAdedi = db.Column(db.Integer, nullable=False, default=0)
    YayineviID = db.Column(db.Integer, db.ForeignKey('Yayinevleri.YayineviID'), nullable=False)
    KategoriID = db.Column(db.Integer, db.ForeignKey('Kategoriler.KategoriID'), nullable=False)
    
    yazarlar = db.relationship('Yazar', secondary=kitap_yazar, lazy='subquery',
        backref=db.backref('kitaplar', lazy=True))
    satis_detaylari = db.relationship('SatisDetay', backref='kitap', lazy='dynamic')
    
    def __repr__(self):
        return f'<Kitap {self.Ad}>'

class Musteri(db.Model):
    __tablename__ = 'Musteriler'
    MusteriID = db.Column(db.Integer, primary_key=True)
    Ad = db.Column(db.String(100), nullable=False)
    Soyad = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(255), nullable=True, unique=True)
    Telefon = db.Column(db.String(20), nullable=True)
    KayitTarihi = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    satislar = db.relationship('Satis', backref='musteri', lazy='dynamic')
    
    def __repr__(self):
        return f'<Musteri {self.Ad} {self.Soyad}>'

class Personel(UserMixin, db.Model):
    __tablename__ = 'Personeller'
    PersonelID = db.Column(db.Integer, primary_key=True)
    KullaniciAdi = db.Column(db.String(50), nullable=False, unique=True)
    SifreHash = db.Column(db.String(255), nullable=False)
    Ad = db.Column(db.String(100), nullable=False)
    Soyad = db.Column(db.String(100), nullable=False)
    Rol = db.Column(db.String(50), nullable=False)
    
    satislar = db.relationship('Satis', backref='personel', lazy='dynamic')
    
    def get_id(self):
        return str(self.PersonelID)
    
    def set_password(self, password):
        self.SifreHash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.SifreHash, password)
    
    def __repr__(self):
        return f'<Personel {self.KullaniciAdi}>'

@login.user_loader
def load_user(id):
    return Personel.query.get(int(id))

class Satis(db.Model):
    __tablename__ = 'Satislar'
    SatisID = db.Column(db.Integer, primary_key=True)
    MusteriID = db.Column(db.Integer, db.ForeignKey('Musteriler.MusteriID'), nullable=True)
    SatisTarihi = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ToplamTutar = db.Column(db.Numeric(10, 2), nullable=False)
    PersonelID = db.Column(db.Integer, db.ForeignKey('Personeller.PersonelID'), nullable=False)
    
    detaylar = db.relationship('SatisDetay', backref='satis', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Satis {self.SatisID}>'

class SatisDetay(db.Model):
    __tablename__ = 'SatisDetaylari'
    SatisDetayID = db.Column(db.Integer, primary_key=True)
    SatisID = db.Column(db.Integer, db.ForeignKey('Satislar.SatisID'), nullable=False)
    KitapID = db.Column(db.Integer, db.ForeignKey('Kitaplar.KitapID'), nullable=False)
    Adet = db.Column(db.Integer, nullable=False)
    BirimFiyat = db.Column(db.Numeric(10, 2), nullable=False)
    
    def __repr__(self):
        return f'<SatisDetay {self.SatisDetayID}>'