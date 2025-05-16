# filepath: /Users/halitartun/Desktop/kitabevi-projesi/run.py
import sys
print(f"SYS.PATH: {sys.path}")
from app import create_app, db
# from app.ilk_veriler import ekle_veriler # Bu satırı değiştirin
from ilk_veriler import ekle_veriler      # Bu şekilde değiştirin
import click

app = create_app()

@app.cli.command("seed-db")
def seed_db_command():
    """Veritabanını örnek verilerle doldurur."""
    with app.app_context():
        ekle_veriler()
    click.echo("Veritabanı örnek verilerle dolduruldu.")

if __name__ == '__main__':
    app.run(debug=True, port=5001)