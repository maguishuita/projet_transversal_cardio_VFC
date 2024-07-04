# Cardio-App

## Description
Cardio-App est une application intelligente pour l'acquisition, le traitement et l'analyse de la variabilité de la fréquence cardiaque.

## Installation

1. Créez un environnement virtuel :
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # Pour Unix
   venv\Scripts\activate  # Pour Windows
   pip install -r requirements.txt
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   python create_database.py
   python create_users.py
   flask run