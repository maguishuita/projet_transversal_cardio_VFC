from app import create_app, db
from app.models import User  # Importez votre modèle utilisateur

app = create_app()

with app.app_context():
    db.create_all()
    print("Database initialized!")
