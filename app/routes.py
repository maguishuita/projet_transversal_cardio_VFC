# app/main/routes.py

from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Diagnostic
from . import db
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG)

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        email = data.get('email')
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash('Utilisateur déjà existant', 'danger')
            return redirect(url_for('main.register'))

        role = data.get('role', 'patient')

        new_user = User(
            username=data.get('username'),
            email=email,
            password=generate_password_hash(data.get('password')),
            role=role
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)

        flash('Inscription réussie', 'success')

        if new_user.role == 'doctor':
            return redirect(url_for('main.doctor_dashboard'))
        elif new_user.role == 'patient':
            return redirect(url_for('main.patient_dashboard'))
        else:
            return redirect(url_for('main.index'))

    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Connexion réussie', 'success')
            logging.debug(f"User {user.email} logged in with role {user.role}")

            if user.role == 'doctor':
                logging.debug("Redirecting to doctor_dashboard")
                return redirect(url_for('main.doctor_dashboard'))
            elif user.role == 'patient':
                logging.debug("Redirecting to patient_dashboard")
                return redirect(url_for('main.patient_dashboard'))
            else:
                logging.debug("Redirecting to index")
                return redirect(url_for('main.index'))
        else:
            flash('Échec de la connexion. Veuillez vérifier vos informations.', 'danger')
            logging.debug(f"Login failed for user {email}")

    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/doctor_dashboard')
@login_required
def doctor_dashboard():
    if current_user.role != 'doctor':
        flash('Accès interdit', 'danger')
        return redirect(url_for('main.index'))

    pending_diagnostics = Diagnostic.query.filter(Diagnostic.diagnosis == None).all()
    treated_diagnostics = Diagnostic.query.filter(Diagnostic.diagnosis != None, Diagnostic.doctor_id == current_user.id).all()
    
    return render_template('doctor_dashboard.html', pending_diagnostics=pending_diagnostics, treated_diagnostics=treated_diagnostics)

@bp.route('/patient_dashboard')
@login_required
def patient_dashboard():
    if current_user.role != 'patient':
        flash('Accès interdit', 'danger')
        return redirect(url_for('main.index'))

    diagnostics = Diagnostic.query.filter_by(patient_id=current_user.id).all()
    return render_template('patient_dashboard.html', diagnostics=diagnostics)

@bp.route('/request_diagnostic', methods=['POST'])
@login_required
def request_diagnostic():
    ecg_data = request.form.get('ecg_data')
    patient_notes = request.form.get('patient_notes')

    if not ecg_data:
        flash('Les données ECG sont requises', 'danger')
        return redirect(url_for('main.patient_dashboard'))

    new_diagnostic = Diagnostic(
        patient_id=current_user.id,
        ecg_data=ecg_data,
        patient_notes=patient_notes,
        requested_at=datetime.utcnow()
    )
    db.session.add(new_diagnostic)
    db.session.commit()
    flash('Demande de diagnostic envoyée avec succès', 'success')
    return redirect(url_for('main.patient_dashboard'))

@bp.route('/respond_diagnostic/<int:diagnostic_id>', methods=['GET', 'POST'])
@login_required
def respond_diagnostic(diagnostic_id):
    diagnostic = Diagnostic.query.get(diagnostic_id)

    if request.method == 'POST':
        diagnosis = request.form.get('diagnosis')

        diagnostic.diagnosis = diagnosis
        diagnostic.doctor_id = current_user.id
        diagnostic.responded_at = datetime.utcnow()

        db.session.commit()
        flash('Diagnostic envoyé', 'success')
        return redirect(url_for('main.doctor_dashboard'))

    return render_template('respond_diagnostic.html', diagnostic=diagnostic)

@bp.route('/edit_diagnostic/<int:diagnostic_id>', methods=['GET', 'POST'])
@login_required
def edit_diagnostic(diagnostic_id):
    diagnostic = Diagnostic.query.get(diagnostic_id)

    if request.method == 'POST':
        diagnosis = request.form.get('diagnosis')

        diagnostic.diagnosis = diagnosis
        diagnostic.responded_at = datetime.utcnow()

        db.session.commit()
        flash('Diagnostic modifié', 'success')
        return redirect(url_for('main.doctor_dashboard'))

    return render_template('edit_diagnostic.html', diagnostic=diagnostic)
