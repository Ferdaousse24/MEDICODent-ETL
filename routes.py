from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory
from werkzeug.utils import secure_filename
import os
from utils import allowed_file, check_file_exists, generate_type_patient_csv, clear_tables, insert_csv_to_db, generate_type_paiement_csv
import pandas as pd

main = Blueprint('main', __name__)

@main.route('/')
def index():
    file_exists_type_patient = check_file_exists('bd_medical_table_type_patient.csv')
    file_exists_type_paiement = check_file_exists('bd_medical_table_type_paiement.csv')
    return render_template('index.html', 
                           file_exists_type_patient=file_exists_type_patient, 
                           file_exists_type_paiement=file_exists_type_paiement)

@main.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Aucune partie de fichier', 'danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Aucun fichier sélectionné', 'danger')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER_IN'], filename)

            # Vérifier si le répertoire existe, sinon le créer
            os.makedirs(current_app.config['UPLOAD_FOLDER_IN'], exist_ok=True)

            try:
                # Enregistrer le fichier téléchargé
                file.save(filepath)
                
                # Génération des fichiers CSV
                generate_type_patient_csv(filepath, current_app.config['UPLOAD_FOLDER_OUT'])
                generate_type_paiement_csv(filepath, current_app.config['UPLOAD_FOLDER_OUT'])
                
                # Vider les tables avant de charger les nouvelles données
                clear_tables()
                
                # Insertion des données dans la base de données
                insert_csv_to_db(os.path.join(current_app.config['UPLOAD_FOLDER_OUT'], 'bd_medical_table_type_patient.csv'), 'table_type_patient')
                insert_csv_to_db(os.path.join(current_app.config['UPLOAD_FOLDER_OUT'], 'bd_medical_table_type_paiement.csv'), 'table_type_paiement')
                
                # Message de réussite
                flash('Fichiers téléchargés avec succès, CSV générés et données insérées dans la base de données')
            except Exception as e:
                flash(f'Une erreur est survenue: {e}', 'danger')
                return redirect(request.url)

            return redirect(url_for('main.index'))
        else:
            flash('Les types de fichiers autorisés sont .xlsx', 'danger')
            return redirect(request.url)
    
    #request.method == 'GET'
    file_exists_type_patient = check_file_exists('bd_medical_table_type_patient.csv')
    file_exists_type_paiement = check_file_exists('bd_medical_table_type_paiement.csv')
    return render_template('upload.html', 
                           file_exists_type_patient=file_exists_type_patient, 
                           file_exists_type_paiement=file_exists_type_paiement)
                          
@main.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER_OUT'], filename)

@main.route('/type_patient')
def type_patient():
    try:
        csv_path = os.path.join(current_app.config['UPLOAD_FOLDER_OUT'], 'bd_medical_table_type_patient.csv')
        df = pd.read_csv(csv_path, sep=';', quotechar='"')
        table_html = df.to_html(classes='table table-striped table-bordered', index=False)
        return render_template('type_patient.html', table=table_html, 
                               file_exists_type_patient=True, 
                               file_exists_type_paiement=check_file_exists('bd_medical_table_type_paiement.csv'))
    except Exception as e:
        flash(f'Une erreur est survenue: {e}', 'danger')
        return redirect(url_for('main.index'))

@main.route('/type_paiement')
def type_paiement():
    try:
        csv_path = os.path.join(current_app.config['UPLOAD_FOLDER_OUT'], 'bd_medical_table_type_paiement.csv')
        df = pd.read_csv(csv_path, sep=';', quotechar='"')
        table_html = df.to_html(classes='table table-striped table-bordered', index=False)
        return render_template('type_paiement.html', table=table_html, 
                               file_exists_type_patient=check_file_exists('bd_medical_table_type_patient.csv'), 
                               file_exists_type_paiement=True)
    except Exception as e:
        flash(f'Une erreur est survenue: {e}', 'danger')
        return redirect(url_for('main.index'))