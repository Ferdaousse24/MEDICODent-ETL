from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import os
import pandas as pd

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
    """Vide les tables spécifiées dans la base de données."""
    tables = [
        'table_type_paiement',
        'table_type_patient'
    ]
    
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            for table in tables:
                conn.execute(text(f"DELETE FROM {table};"))
            trans.commit()
        except Exception as e:
            trans.rollback()
            print(f"Error clearing tables: {e}")
            raise
   
def generate_type_patient_csv(filepath, output_dir):
    # Lire la feuille "Type_Patient" du fichier Excel
    df_patient = pd.read_excel(filepath, sheet_name='Type_Patient')    
    # Nommer les colonnes
    df_patient.columns = ['id_patient', 'type_patient']    
    # Mettre en majuscule les types de patients et remplacer "SANS CMU" par "NON_CMU"
    df_patient['type_patient'] = df_patient['type_patient'].apply(lambda x: x.upper().replace('SANS CMU', 'NON_CMU'))    
    # Assurez-vous que les types de patients correspondent exactement à "CMU" ou "NON_CMU"
    df_patient['type_patient'] = df_patient['type_patient'].replace('NON_CMU', 'non_CMU')    
    # Enregistrer le fichier CSV
    output_csv_patient = os.path.join(output_dir, 'bd_medical_table_type_patient.csv')
    df_patient.to_csv(output_csv_patient, index=False, sep=';', quotechar='"', quoting=1)
   
def generate_type_paiement_csv(filepath, output_dir):
    df_paiement = pd.read_excel(filepath, sheet_name='Type_Paiement')
    df_paiement.columns = ['id_paiement', 'type_paiement']
    df_paiement['type_paiement'] = df_paiement['type_paiement'].apply(lambda x: x.upper())
    output_csv_paiement = os.path.join(output_dir, 'bd_medical_table_type_paiement.csv')
    df_paiement.to_csv(output_csv_paiement, index=False, sep=';', quotechar='"', quoting=1)

def insert_csv_to_db(csv_file, table_name, column_mapping=None):
    """Insère les données d'un fichier CSV dans une table de la base de données."""
    df = pd.read_csv(csv_file, sep=';', quotechar='"')
    if column_mapping:
        df = df.rename(columns=column_mapping)
    df.to_sql(table_name, con=engine, if_exists='append', index=False)