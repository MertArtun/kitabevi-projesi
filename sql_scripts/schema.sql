-- Yazarlar tablosu
CREATE TABLE "Yazarlar" (
    "YazarID" SERIAL PRIMARY KEY,
    "Ad" VARCHAR(100) NOT NULL,
    "Soyad" VARCHAR(100) NOT NULL,
    "Biyografi" TEXT
);

-- Yayinevleri tablosu
CREATE TABLE "Yayinevleri" (
    "YayineviID" SERIAL PRIMARY KEY,
    "Ad" VARCHAR(255) NOT NULL UNIQUE,
    "Adres" TEXT,
    "Telefon" VARCHAR(20)
);

-- Kategoriler tablosu
CREATE TABLE "Kategoriler" (
    "KategoriID" SERIAL PRIMARY KEY,
    "Ad" VARCHAR(100) NOT NULL UNIQUE
);

-- Kitaplar tablosu
CREATE TABLE "Kitaplar" (
    "KitapID" SERIAL PRIMARY KEY,
    "ISBN" VARCHAR(13) NOT NULL UNIQUE,
    "Ad" VARCHAR(255) NOT NULL,
    "YayinYili" INTEGER,
    "SayfaSayisi" INTEGER,
    "Fiyat" DECIMAL(10, 2) NOT NULL,
    "StokAdedi" INTEGER NOT NULL DEFAULT 0,
    "YayineviID" INTEGER NOT NULL REFERENCES "Yayinevleri"("YayineviID"),
    "KategoriID" INTEGER NOT NULL REFERENCES "Kategoriler"("KategoriID")
);

-- KitapYazarlari tablosu (Çoka Çok İlişki Tablosu)
CREATE TABLE "KitapYazarlari" (
    "KitapID" INTEGER NOT NULL REFERENCES "Kitaplar"("KitapID") ON DELETE CASCADE,
    "YazarID" INTEGER NOT NULL REFERENCES "Yazarlar"("YazarID") ON DELETE CASCADE,
    PRIMARY KEY ("KitapID", "YazarID")
);

-- Musteriler tablosu
CREATE TABLE "Musteriler" (
    "MusteriID" SERIAL PRIMARY KEY,
    "Ad" VARCHAR(100) NOT NULL,
    "Soyad" VARCHAR(100) NOT NULL,
    "Email" VARCHAR(255) UNIQUE,
    "Telefon" VARCHAR(20),
    "KayitTarihi" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Personeller tablosu
CREATE TABLE "Personeller" (
    "PersonelID" SERIAL PRIMARY KEY,
    "KullaniciAdi" VARCHAR(50) NOT NULL UNIQUE,
    "SifreHash" VARCHAR(255) NOT NULL,
    "Ad" VARCHAR(100) NOT NULL,
    "Soyad" VARCHAR(100) NOT NULL,
    "Rol" VARCHAR(50) NOT NULL
);

-- Satislar tablosu
CREATE TABLE "Satislar" (
    "SatisID" SERIAL PRIMARY KEY,
    "MusteriID" INTEGER REFERENCES "Musteriler"("MusteriID"),
    "SatisTarihi" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "ToplamTutar" DECIMAL(10, 2) NOT NULL,
    "PersonelID" INTEGER NOT NULL REFERENCES "Personeller"("PersonelID")
);

-- SatisDetaylari tablosu
CREATE TABLE "SatisDetaylari" (
    "SatisDetayID" SERIAL PRIMARY KEY,
    "SatisID" INTEGER NOT NULL REFERENCES "Satislar"("SatisID") ON DELETE CASCADE,
    "KitapID" INTEGER NOT NULL REFERENCES "Kitaplar"("KitapID"),
    "Adet" INTEGER NOT NULL,
    "BirimFiyat" DECIMAL(10, 2) NOT NULL
);

-- Indexler
CREATE INDEX idx_kitap_ad ON "Kitaplar"("Ad");
CREATE INDEX idx_kitap_isbn ON "Kitaplar"("ISBN");
CREATE INDEX idx_musteri_soyad ON "Musteriler"("Soyad");
CREATE INDEX idx_satis_tarih ON "Satislar"("SatisTarihi");

-- View oluşturma
CREATE VIEW vw_KitapDetaylari AS
SELECT
    k."KitapID",
    k."ISBN",
    k."Ad" AS "KitapAdi",
    k."YayinYili",
    k."Fiyat",
    k."StokAdedi",
    ka."Ad" AS "KategoriAdi",
    y."Ad" AS "YayineviAdi",
    STRING_AGG(DISTINCT ya."Ad" || ' ' || ya."Soyad", ', ') AS "Yazarlar"
FROM "Kitaplar" k
JOIN "Kategoriler" ka ON k."KategoriID" = ka."KategoriID"
JOIN "Yayinevleri" y ON k."YayineviID" = y."YayineviID"
LEFT JOIN "KitapYazarlari" ky ON k."KitapID" = ky."KitapID"
LEFT JOIN "Yazarlar" ya ON ky."YazarID" = ya."YazarID"
GROUP BY k."KitapID", k."ISBN", k."Ad", k."YayinYili", k."Fiyat", k."StokAdedi", ka."Ad", y."Ad";

-- Trigger oluşturma
CREATE OR REPLACE FUNCTION update_stock_after_sale()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE "Kitaplar"
    SET "StokAdedi" = "StokAdedi" - NEW."Adet"
    WHERE "KitapID" = NEW."KitapID";

    IF (SELECT "StokAdedi" FROM "Kitaplar" WHERE "KitapID" = NEW."KitapID") < 0 THEN
        RAISE EXCEPTION 'Yetersiz stok! KitapID: %, İstenen Adet: %, Kalan Stok: %',
                        NEW."KitapID", NEW."Adet", (SELECT "StokAdedi" + NEW."Adet" FROM "Kitaplar" WHERE "KitapID" = NEW."KitapID");
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_AfterSaleDetailInsert
AFTER INSERT ON "SatisDetaylari"
FOR EACH ROW
EXECUTE FUNCTION update_stock_after_sale();