import os
import pandas as pd
from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import re

# Configuration de la base de données
DATABASE_URI = 'mysql+pymysql://root:@localhost/medicodentetl'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

def allowed_file(filename):
    """Vérifie si le fichier a une extension autorisée."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def check_file_exists(filename):
    """Vérifie si un fichier existe dans le dossier de sortie."""
    csv_path = os.path.join(current_app.config['UPLOAD_FOLDER_OUT'], filename)
    return os.path.exists(csv_path)

def clear_tables():
    """Exécute le script SQL pour recréer les tables spécifiées dans la base de données."""
    script_path = os.path.join(os.path.dirname(__file__), 'sql', 'medicodentetl.sql')
    
    with open(script_path, 'r') as file:
        sql_script = file.read()

    # Séparer les différentes commandes SQL
    sql_commands = sql_script.split(';')

    with engine.connect() as conn:
        trans = conn.begin()
        try:
            for command in sql_commands:
                if command.strip():  # Ignorer les commandes vides
                    conn.execute(text(command))
            trans.commit()
        except Exception as e:
            trans.rollback()
            print(f"Error executing script: {e}")
            raise

def generate_type_patient_csv(filepath, output_dir):
    df_patient = pd.read_excel(filepath, sheet_name='Type_Patient')
    df_patient.columns = ['id_patient', 'type_patient']
    df_patient['type_patient'] = df_patient['type_patient'].apply(lambda x: x.upper())
    df_patient['type_patient'] = df_patient['type_patient'].replace('SANS CMU', 'NON_CMU')
    output_csv_patient = os.path.join(output_dir, 'bd_medical_table_type_patient.csv')
    df_patient.to_csv(output_csv_patient, index=False, sep=';', quotechar='"', quoting=1)

def generate_type_paiement_csv(filepath, output_dir):
    df_paiement = pd.read_excel(filepath, sheet_name='Type_Paiement')
    df_paiement.columns = ['id_paiement', 'type_paiement']
    df_paiement['type_paiement'] = df_paiement['type_paiement'].apply(lambda x: x.upper())
    output_csv_paiement = os.path.join(output_dir, 'bd_medical_table_type_paiement.csv')
    df_paiement.to_csv(output_csv_paiement, index=False, sep=';', quotechar='"', quoting=1)

def generate_type_jour_csv(output_dir):
    data_jour = {
        'id_jour': [1, 2, 3],
        'type_jour': ['Travaille', 'Non Travaille', 'Férié']
    }
    df_jour = pd.DataFrame(data_jour)
    output_csv_jour = os.path.join(output_dir, 'bd_medical_table_type_jour.csv')
    df_jour.to_csv(output_csv_jour, index=False, sep=';', quotechar='"', quoting=1)

def generate_annee_csv(filepath, output_dir):
    sheet_names = pd.ExcelFile(filepath).sheet_names
    years = []
    for sheet in sheet_names:
        match = re.search(r'(19|20)\d{2}', sheet)
        if match:
            years.append(match.group(0))

    data_annee = {
        'id_A': list(range(17, 17 + len(years))),
        'annee': years
    }
    df_annee = pd.DataFrame(data_annee)
    output_csv_annee = os.path.join(output_dir, 'bd_medical_table_t_annee.csv')
    df_annee.to_csv(output_csv_annee, index=False, sep=';', quotechar='"', quoting=1)

def generate_mois_csv(output_dir):
    df_annee = pd.read_csv(os.path.join(output_dir, 'bd_medical_table_t_annee.csv'), sep=';', quotechar='"')
    data_mois = {
        'id_M': [],
        'mois': [],
        'id_A': []
    }
    id_M = 1
    for i, year in enumerate(df_annee['id_A']):
        for month in range(1, 13):
            data_mois['id_M'].append(id_M)
            data_mois['mois'].append(month)
            data_mois['id_A'].append(year)
            id_M += 1

    df_mois = pd.DataFrame(data_mois)
    output_csv_mois = os.path.join(output_dir, 'bd_medical_table_t_mois.csv')
    df_mois.to_csv(output_csv_mois, index=False, sep=';', quotechar='"', quoting=1)

def generate_semaine_csv(output_dir):
    df_annee = pd.read_csv(os.path.join(output_dir, 'bd_medical_table_t_annee.csv'), sep=';', quotechar='"')
    data_semaine = {
        'id_S': [],
        'semaine': [],
        'id_A': []
    }
    id_S = 1
    for i, year in enumerate(df_annee['id_A']):
        for week in range(1, 53):
            data_semaine['id_S'].append(id_S)
            data_semaine['semaine'].append(week)
            data_semaine['id_A'].append(year)
            id_S += 1

    df_semaine = pd.DataFrame(data_semaine)
    output_csv_semaine = os.path.join(output_dir, 'bd_medical_table_t_semaine.csv')
    df_semaine.to_csv(output_csv_semaine, index=False, sep=';', quotechar='"', quoting=1)

def generate_date_csv(filepath):
    """Génère le tableau des dates et l'exporte en CSV."""
    annee_df = pd.read_csv(os.path.join(current_app.config['UPLOAD_FOLDER_OUT'], 'bd_medical_table_t_annee.csv'), sep=';', quotechar='"')
    mois_df = pd.read_csv(os.path.join(current_app.config['UPLOAD_FOLDER_OUT'], 'bd_medical_table_t_mois.csv'), sep=';', quotechar='"')
    semaine_df = pd.read_csv(os.path.join(current_app.config['UPLOAD_FOLDER_OUT'], 'bd_medical_table_t_semaine.csv'), sep=';', quotechar='"')
    jour_df = pd.read_csv(os.path.join(current_app.config['UPLOAD_FOLDER_OUT'], 'bd_medical_table_type_jour.csv'), sep=';', quotechar='"')

    date_data = {
        'id_D': [],
        'date_R': [],
        'jour': [],
        'mois': [],
        'annee': [],
        'semaine': [],
        'id_t_jour': [],
        'id_M': [],
        'id_S': []
    }

    error_data = {
        'sheet_name': [],
        'row_number': [],
        'invalid_date': []
    }

    last_date = pd.Timestamp.min
    xls = pd.ExcelFile(filepath)

    for _, annee_row in annee_df.iterrows():
        year = annee_row['annee']
        id_A = annee_row['id_A']
        sheet_name = next(sheet for sheet in xls.sheet_names if str(year) in sheet)

        df = pd.read_excel(filepath, sheet_name=sheet_name, header=None)
        header_row = df.apply(lambda row: row.astype(str).str.contains('Date').any(), axis=1).idxmax()
        df.columns = df.iloc[header_row]
        df = df[header_row + 1:].reset_index(drop=True)

        if 'Date' not in df.columns:
            continue

        id_D = 1  # Réinitialiser le compteur pour chaque année

        for index, row in df.iterrows():
            date = row['Date']
            try:
                current_date = pd.to_datetime(date, errors='coerce')
                if pd.isna(current_date):
                    continue

                if current_date <= last_date:
                    error_data['sheet_name'].append(sheet_name)
                    error_data['row_number'].append(index + header_row + 2)  # +2 to account for header and 0-based index
                    error_data['invalid_date'].append(date)
                    continue

                last_date = current_date

                day = current_date.day
                month = current_date.month
                week_number = current_date.isocalendar()[1]
                year = current_date.year

                day_of_week = current_date.weekday() + 1
                id_t_jour = jour_df[jour_df['type_jour'].str.contains('Travaille', case=False)]['id_jour'].values[0]

                id_M = mois_df[(mois_df['mois'] == month) & (mois_df['id_A'] == id_A)]['id_M']
                id_S = semaine_df[(semaine_df['semaine'] == week_number) & (semaine_df['id_A'] == id_A)]['id_S']

                if id_M.empty or id_S.empty:
                    continue

                date_data['id_D'].append(f"{year}{str(id_D).zfill(4)}")
                date_data['date_R'].append(current_date.strftime("%d/%m/%Y"))
                date_data['jour'].append(day)
                date_data['mois'].append(month)
                date_data['annee'].append(year)
                date_data['semaine'].append(week_number)
                date_data['id_t_jour'].append(id_t_jour)
                date_data['id_M'].append(id_M.values[0])
                date_data['id_S'].append(id_S.values[0])

                id_D += 1
            except Exception as e:
                print(f"Error processing date {date}: {e}")
                continue

    df_date = pd.DataFrame(date_data)
    output_csv_date = os.path.join(current_app.config['UPLOAD_FOLDER_OUT'], 'bd_medical_table_t_date.csv')
    df_date.to_csv(output_csv_date, index=False, sep=';', quotechar='"', quoting=1)

    df_error = pd.DataFrame(error_data)
    if not df_error.empty:
        error_csv_path = os.path.join(current_app.config['UPLOAD_FOLDER_OUT'], 'date_errors.csv')
        df_error.to_csv(error_csv_path, index=False, sep=';', quotechar='"', quoting=1)

def generate_fait_patient_csv(filepath):
    """Génère le tableau fait_patient et l'exporte en CSV."""
    # Lire les fichiers CSV nécessaires
    date_df = pd.read_csv(os.path.join(current_app.config['UPLOAD_FOLDER_OUT'], 'bd_medical_table_t_date.csv'), sep=';', quotechar='"')
    patient_df = pd.read_csv(os.path.join(current_app.config['UPLOAD_FOLDER_OUT'], 'bd_medical_table_type_patient.csv'), sep=';', quotechar='"')

    # Initialiser les données pour le tableau fait_patient
    fait_patient_data = {
        'id_D': [],
        'nb_patient': [],
        'id_patient': []
    }

    xls = pd.ExcelFile(filepath)
    for sheet_name in xls.sheet_names:
        match = re.search(r'(19|20)\d{2}', sheet_name)
        if not match:
            continue

        df = pd.read_excel(filepath, sheet_name=sheet_name, header=None)
        header_row = df.apply(lambda row: row.astype(str).str.contains('Date').any(), axis=1).idxmax()
        df.columns = df.iloc[header_row]
        df = df[header_row + 1:].reset_index(drop=True)

        if 'Date' not in df.columns or 'Nb patients' not in df.columns or 'Nb CMU' not in df.columns:
            continue

        # Remplacer les valeurs NaN dans 'Nb CMU' par 0
        df['Nb CMU'] = df['Nb CMU'].fillna(0)

        for index, row in df.iterrows():
            try:
                current_date = pd.to_datetime(row['Date'], errors='coerce')
                if pd.isna(current_date) or pd.isna(row['Nb patients']):
                    continue

                # Rechercher l'id_D correspondant dans le fichier des dates
                id_D_row = date_df[date_df['date_R'] == current_date.strftime("%d/%m/%Y")]
                if id_D_row.empty:
                    continue

                id_D = id_D_row['id_D'].values[0]
                nb_patient_non_cmu = int(row['Nb patients'] - row['Nb CMU'])
                nb_patient_cmu = int(row['Nb CMU'])

                # Ajouter les données pour les patients non-CMU
                fait_patient_data['id_D'].append(id_D)
                fait_patient_data['nb_patient'].append(nb_patient_non_cmu)
                fait_patient_data['id_patient'].append(patient_df[patient_df['type_patient'] == 'NON_CMU']['id_patient'].values[0])

                # Ajouter les données pour les patients CMU
                fait_patient_data['id_D'].append(id_D)
                fait_patient_data['nb_patient'].append(nb_patient_cmu)
                fait_patient_data['id_patient'].append(patient_df[patient_df['type_patient'] == 'CMU']['id_patient'].values[0])
            except Exception as e:
                print(f"Error processing row {index}: {e}")
                continue

    # Créer le DataFrame et sauvegarder le fichier CSV
    df_fait_patient = pd.DataFrame(fait_patient_data)
    output_csv_fait_patient = os.path.join(current_app.config['UPLOAD_FOLDER_OUT'], 'bd_medical_table_fait_patient.csv')
    df_fait_patient.to_csv(output_csv_fait_patient, index=False, sep=';', quotechar='"', quoting=1)

def insert_csv_to_db(csv_file, table_name, column_mapping=None):
    """Insère les données d'un fichier CSV dans une table de la base de données."""
    df = pd.read_csv(csv_file, sep=';', quotechar='"')
    if column_mapping:
        df = df.rename(columns=column_mapping)
    df.to_sql(table_name, con=engine, if_exists='append', index=False)