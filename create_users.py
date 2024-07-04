# create_users.py

from app import create_app, db
from app.models import User

def create_users():
    app = create_app()

    # Contexte de l'application pour les commandes SQLAlchemy
    with app.app_context():
        # Création de deux utilisateurs pour les tests
        user_patient = User(
            username='die',
            email='d@example.com',
            role='patient'
        )
        user_patient.set_password('password')  # Définir le mot de passe
        db.session.add(user_patient)

        user_doctor = User(
            username='dr_mane1',
            email='dr_mane1@example.com',
            role='doctor'
        )
        user_doctor.set_password('password')  # Définir le mot de passe
        db.session.add(user_doctor)

        # Committer les changements à la base de données
        db.session.commit()

        print('Utilisateurs créés avec succès!')

if __name__ == '__main__':
    create_users()



