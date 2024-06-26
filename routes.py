from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory
from werkzeug.utils import secure_filename
import os
from utils import (allowed_file, check_file_exists, generate_type_patient_csv, clear_tables, insert_csv_to_db, generate_type_paiement_csv, generate_type_jour_csv,
generate_annee_csv, generate_mois_csv, generate_semaine_csv, generate_date_csv, generate_fait_patient_csv, generate_fait_recettes_csv)
import pandas as pd


main = Blueprint('main', __name__)

@main.route('/')
def index():
    file_exists_type_patient = check_file_exists('bd_medical_table_type_patient.csv')
    file_exists_type_paiement = check_file_exists('bd_medical_table_type_paiement.csv')
    file_exists_type_jour = check_file_exists('bd_medical_table_type_jour.csv')
    file_exists_t_annee = check_file_exists('bd_medical_table_t_annee.csv')
    file_exists_t_mois = check_file_exists('bd_medical_table_t_mois.csv')
    file_exists_t_semaine = check_file_exists('bd_medical_table_t_semaine.csv')
    file_exists_t_date = check_file_exists('bd_medical_table_t_date.csv')
    file_exists_fait_patient = check_file_exists('bd_medical_table_fait_patient.csv')
    file_exists_fait_recettes = check_file_exists('bd_medical_table_fait_recettes.csv')
    return render_template('index.html', 
                           file_exists_type_patient=file_exists_type_patient, 
                           file_exists_type_paiement=file_exists_type_paiement,
                           file_exists_type_jour=file_exists_type_jour,
                           file_exists_t_annee=file_exists_t_annee,
                           file_exists_t_mois=file_exists_t_mois,
                           file_exists_t_semaine=file_exists_t_semaine,
                           file_exists_t_date=file_exists_t_date,
                           file_exists_fait_patient=file_exists_fait_patient,
                           file_exists_fait_recettes=file_exists_fait_recettes)

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
                generate_type_jour_csv(current_app.config['UPLOAD_FOLDER_OUT'])
                generate_annee_csv(filepath, current_app.config['UPLOAD_FOLDER_OUT'])
                generate_mois_csv(current_app.config['UPLOAD_FOLDER_OUT'])
                generate_semaine_csv(current_app.config['UPLOAD_FOLDER_OUT'])
                generate_date_csv(filepath)
                generate_fait_patient_csv(filepath)
                generate_fait_recettes_csv(filepath)
                
                # Vider les tables avant de charger les nouvelles données
                clear_tables()
                
                # Insertion des données dans la base de données
                insert_csv_to_db(os.path.join(current_app.config['UPLOAD_FOLDER_OUT'], 'bd_medical_table_type_patient.csv'), 'table_type_patient')
                insert_csv_to_db(os.path.join(current_app.config['UPLOAD_FOLDER_OUT'], 'bd_medical_table_type_paiement.csv'), 'table_type_paiement')
                insert_csv_to_db(os.path.join(current_app.config['UPLOAD_FOLDER_OUT'], 'bd_medical_table_type_jour.csv'), 'table_type_jour', column_mapping={'id_jour': 'id_t_jour'})
                insert_csv_to_db(os.path.join(current_app.config['UPLOAD_FOLDER_OUT'], 'bd_medical_table_t_annee.csv'), 'table_t_annee')
                insert_csv_to_db(os.path.join(current_app.config['UPLOAD_FOLDER_OUT'], 'bd_medical_table_t_mois.csv'), 'table_t_mois')
                insert_csv_to_db(os.path.join(current_app.config['UPLOAD_FOLDER_OUT'], 'bd_medical_table_t_semaine.csv'), 'table_t_semaine')
                insert_csv_to_db(os.path.join(current_app.config['UPLOAD_FOLDER_OUT'], 'bd_medical_table_t_date.csv'), 'table_t_date', column_mapping={'id_jour': 'id_t_jour'})
                insert_csv_to_db(os.path.join(current_app.config['UPLOAD_FOLDER_OUT'], 'bd_medical_table_fait_patient.csv'), 'faits_patient')
                insert_csv_to_db(os.path.join(current_app.config['UPLOAD_FOLDER_OUT'], 'bd_medical_table_fait_recettes.csv'), 'faits_recettes')
                
                
                # Message de réussite
                flash('Fichiers téléchargés avec succès, CSV générés et données insérées dans la base de données', 'success')
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
    file_exists_type_jour = check_file_exists('bd_medical_table_type_jour.csv')
    file_exists_t_annee = check_file_exists('bd_medical_table_t_annee.csv')
    file_exists_t_mois = check_file_exists('bd_medical_table_t_mois.csv')
    file_exists_t_semaine = check_file_exists('bd_medical_table_t_semaine.csv')
    file_exists_t_date = check_file_exists('bd_medical_table_t_date.csv')
    file_exists_fait_patient = check_file_exists('bd_medical_table_fait_patient.csv')
    file_exists_fait_recettes = check_file_exists('bd_medical_table_fait_recettes.csv')
    return render_template('upload.html', 
                           file_exists_type_patient=file_exists_type_patient, 
                           file_exists_type_paiement=file_exists_type_paiement,
                           file_exists_type_jour=file_exists_type_jour,
                           file_exists_t_annee=file_exists_t_annee,
                           file_exists_t_mois=file_exists_t_mois,
                           file_exists_t_semaine=file_exists_t_semaine,
                           file_exists_t_date=file_exists_t_date,
                           file_exists_fait_patient=file_exists_fait_patient,
                           file_exists_fait_recettes=file_exists_fait_recettes)
                          
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
                               file_exists_type_paiement=check_file_exists('bd_medical_table_type_paiement.csv'),
                               file_exists_type_jour=check_file_exists('bd_medical_table_type_jour.csv'),
                               file_exists_t_annee=check_file_exists('bd_medical_table_t_annee.csv'),
                               file_exists_t_mois=check_file_exists('bd_medical_table_t_mois.csv'),
                               file_exists_t_semaine=check_file_exists('bd_medical_table_t_semaine.csv'),
                               file_exists_t_date=check_file_exists('bd_medical_table_t_date.csv'),
                               file_exists_fait_patient=check_file_exists('bd_medical_table_fait_patient.csv'),
                               file_exists_fait_recettes=check_file_exists('bd_medical_table_fait_recettes.csv'))
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
                               file_exists_type_paiement=True,
                               file_exists_type_jour=check_file_exists('bd_medical_table_type_jour.csv'),
                               file_exists_t_annee=check_file_exists('bd_medical_table_t_annee.csv'),
                               file_exists_t_mois=check_file_exists('bd_medical_table_t_mois.csv'),
                               file_exists_t_semaine=check_file_exists('bd_medical_table_t_semaine.csv'),
                               file_exists_t_date=check_file_exists('bd_medical_table_t_date.csv'),
                               file_exists_fait_patient=check_file_exists('bd_medical_table_fait_patient.csv'),
                               file_exists_fait_recettes=check_file_exists('bd_medical_table_fait_recettes.csv'))
    except Exception as e:
        flash(f'Une erreur est survenue: {e}', 'danger')
        return redirect(url_for('main.index'))
        
@main.route('/type_jour')
def type_jour():
    try:
        csv_path = os.path.join(current_app.config['UPLOAD_FOLDER_OUT'], 'bd_medical_table_type_jour.csv')
        df = pd.read_csv(csv_path, sep=';', quotechar='"')
        table_html = df.to_html(classes='table table-striped table-bordered', index=False)
        return render_template('type_jour.html', table=table_html, 
                               file_exists_type_patient=check_file_exists('bd_medical_table_type_patient.csv'), 
                               file_exists_type_paiement=check_file_exists('bd_medical_table_type_paiement.csv'),
                               file_exists_type_jour=True,
                               file_exists_t_annee=check_file_exists('bd_medical_table_t_annee.csv'),
                               file_exists_t_mois=check_file_exists('bd_medical_table_t_mois.csv'),
                               file_exists_t_semaine=check_file_exists('bd_medical_table_t_semaine.csv'),
                               file_exists_t_date=check_file_exists('bd_medical_table_t_date.csv'),
                               file_exists_fait_patient=check_file_exists('bd_medical_table_fait_patient.csv'),
                               file_exists_fait_recettes=check_file_exists('bd_medical_table_fait_recettes.csv'))
    except Exception as e:
        flash(f'Une erreur est survenue: {e}', 'danger')
        return redirect(url_for('main.index'))
        
@main.route('/type_annee')
def type_annee():
    try:
        csv_path = os.path.join(current_app.config['UPLOAD_FOLDER_OUT'], 'bd_medical_table_t_annee.csv')
        df = pd.read_csv(csv_path, sep=';', quotechar='"')
        table_html = df.to_html(classes='table table-striped table-bordered', index=False)
        return render_template('type_annee.html', table=table_html, 
                               file_exists_type_patient=check_file_exists('bd_medical_table_type_patient.csv'), 
                               file_exists_type_paiement=check_file_exists('bd_medical_table_type_paiement.csv'),
                               file_exists_type_jour=check_file_exists('bd_medical_table_type_jour.csv'),
                               file_exists_t_annee=True,
                               file_exists_t_mois=check_file_exists('bd_medical_table_t_mois.csv'),
                               file_exists_t_semaine=check_file_exists('bd_medical_table_t_semaine.csv'),
                               file_exists_t_date=check_file_exists('bd_medical_table_t_date.csv'),
                               file_exists_fait_patient=check_file_exists('bd_medical_table_fait_patient.csv'),
                               file_exists_fait_recettes=check_file_exists('bd_medical_table_fait_recettes.csv'))
    except Exception as e:
        flash(f'Une erreur est survenue: {e}', 'danger')
        return redirect(url_for('main.index'))
        
@main.route('/type_mois')
def type_mois():
    try:
        csv_path = os.path.join(current_app.config['UPLOAD_FOLDER_OUT'], 'bd_medical_table_t_mois.csv')
        df = pd.read_csv(csv_path, sep=';', quotechar='"')
        table_html = df.to_html(classes='table table-striped table-bordered', index=False)
        return render_template('type_mois.html', table=table_html, 
                               file_exists_type_patient=check_file_exists('bd_medical_table_type_patient.csv'), 
                               file_exists_type_paiement=check_file_exists('bd_medical_table_type_paiement.csv'),
                               file_exists_type_jour=check_file_exists('bd_medical_table_type_jour.csv'),
                               file_exists_t_annee=check_file_exists('bd_medical_table_t_annee.csv'),
                               file_exists_t_mois=True,
                               file_exists_t_semaine=check_file_exists('bd_medical_table_t_semaine.csv'),
                               file_exists_t_date=check_file_exists('bd_medical_table_t_date.csv'),
                               file_exists_fait_patient=check_file_exists('bd_medical_table_fait_patient.csv'),
                               file_exists_fait_recettes=check_file_exists('bd_medical_table_fait_recettes.csv'))
    except Exception as e:
        flash(f'Une erreur est survenue: {e}', 'danger')
        return redirect(url_for('main.index'))

@main.route('/type_semaine')
def type_semaine():
    try:
        csv_path = os.path.join(current_app.config['UPLOAD_FOLDER_OUT'], 'bd_medical_table_t_semaine.csv')
        df = pd.read_csv(csv_path, sep=';', quotechar='"')
        table_html = df.to_html(classes='table table-striped table-bordered', index=False)
        return render_template('type_semaine.html', table=table_html, 
                               file_exists_type_patient=check_file_exists('bd_medical_table_type_patient.csv'), 
                               file_exists_type_paiement=check_file_exists('bd_medical_table_type_paiement.csv'),
                               file_exists_type_jour=check_file_exists('bd_medical_table_type_jour.csv'),
                               file_exists_t_annee=check_file_exists('bd_medical_table_t_annee.csv'),
                               file_exists_t_mois=check_file_exists('bd_medical_table_t_mois.csv'),
                               file_exists_t_semaine=True,
                               file_exists_t_date=check_file_exists('bd_medical_table_t_date.csv'),
                               file_exists_fait_patient=check_file_exists('bd_medical_table_fait_patient.csv'),
                               file_exists_fait_recettes=check_file_exists('bd_medical_table_fait_recettes.csv'))
    except Exception as e:
        flash(f'Une erreur est survenue: {e}', 'danger')
        return redirect(url_for('main.index'))

@main.route('/type_date')
def type_date():
    try:
        csv_path = os.path.join(current_app.config['UPLOAD_FOLDER_OUT'], 'bd_medical_table_t_date.csv')
        df = pd.read_csv(csv_path, sep=';', quotechar='"')
        table_html = df.to_html(classes='table table-striped table-bordered', index=False)
        return render_template('type_date.html', table=table_html, 
                               file_exists_type_patient=check_file_exists('bd_medical_table_type_patient.csv'), 
                               file_exists_type_paiement=check_file_exists('bd_medical_table_type_paiement.csv'),
                               file_exists_type_jour=check_file_exists('bd_medical_table_type_jour.csv'),
                               file_exists_t_annee=check_file_exists('bd_medical_table_t_annee.csv'),
                               file_exists_t_mois=check_file_exists('bd_medical_table_t_mois.csv'),
                               file_exists_t_semaine=check_file_exists('bd_medical_table_t_semaine.csv'),
                               file_exists_t_date=True,
                               file_exists_fait_patient=check_file_exists('bd_medical_table_fait_patient.csv'),
                               file_exists_fait_recettes=check_file_exists('bd_medical_table_fait_recettes.csv'))
    except Exception as e:
        flash(f'Une erreur est survenue: {e}', 'danger')
        return redirect(url_for('main.index'))

@main.route('/fait_patient')
def fait_patient():
    try:
        csv_path = os.path.join(current_app.config['UPLOAD_FOLDER_OUT'], 'bd_medical_table_fait_patient.csv')
        df = pd.read_csv(csv_path, sep=';', quotechar='"')
        table_html = df.to_html(classes='table table-striped table-bordered', index=False)
        return render_template('fait_patient.html', table=table_html, 
                               file_exists_type_patient=check_file_exists('bd_medical_table_type_patient.csv'), 
                               file_exists_type_paiement=check_file_exists('bd_medical_table_type_paiement.csv'),
                               file_exists_type_jour=check_file_exists('bd_medical_table_type_jour.csv'),
                               file_exists_t_annee=check_file_exists('bd_medical_table_t_annee.csv'),
                               file_exists_t_mois=check_file_exists('bd_medical_table_t_mois.csv'),
                               file_exists_t_semaine=check_file_exists('bd_medical_table_t_semaine.csv'),
                               file_exists_t_date=check_file_exists('bd_medical_table_t_date.csv'),
                               file_exists_fait_patient=True,
                               file_exists_fait_recettes=check_file_exists('bd_medical_table_fait_recettes.csv'))
    except Exception as e:
        flash(f'Une erreur est survenue: {e}', 'danger')
        return redirect(url_for('main.index'))

@main.route('/fait_recettes')
def fait_recettes():
    try:
        csv_path = os.path.join(current_app.config['UPLOAD_FOLDER_OUT'], 'bd_medical_table_fait_recettes.csv')
        df = pd.read_csv(csv_path, sep=';', quotechar='"')
        table_html = df.to_html(classes='table table-striped table-bordered', index=False)
        return render_template('fait_recettes.html', table=table_html, 
                               file_exists_type_patient=check_file_exists('bd_medical_table_type_patient.csv'), 
                               file_exists_type_paiement=check_file_exists('bd_medical_table_type_paiement.csv'),
                               file_exists_type_jour=check_file_exists('bd_medical_table_type_jour.csv'),
                               file_exists_t_annee=check_file_exists('bd_medical_table_t_annee.csv'),
                               file_exists_t_mois=check_file_exists('bd_medical_table_t_mois.csv'),
                               file_exists_t_semaine=check_file_exists('bd_medical_table_t_semaine.csv'),
                               file_exists_t_date=check_file_exists('bd_medical_table_t_date.csv'),
                               file_exists_fait_patient=check_file_exists('bd_medical_table_fait_patient.csv'),
                               file_exists_fait_recettes=True)
    except Exception as e:
        flash(f'Une erreur est survenue: {e}', 'danger')
        return redirect(url_for('main.index'))