# app/models.py

from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'doctor' or 'patient'
    active = db.Column(db.Boolean(), default=True)  # Column for active status
    # Relationships
    diagnostics = db.relationship('Diagnostic', backref='patient', foreign_keys='Diagnostic.patient_id', lazy=True)
    given_diagnostics = db.relationship('Diagnostic', backref='doctor', foreign_keys='Diagnostic.doctor_id', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_active(self):
        return self.active


class Diagnostic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ecg_data = db.Column(db.Text, nullable=False)  # Données ECG sous forme de texte (JSON)
    diagnosis = db.Column(db.String)  # Rapport écrit du médecin
    requested_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    responded_at = db.Column(db.DateTime)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Lien vers le médecin qui a fait le diagnostic
    patient_notes = db.Column(db.Text)  # Notes additionnelles du patient

    def __repr__(self):
        return '<Diagnostic {}>'.format(self.id)
