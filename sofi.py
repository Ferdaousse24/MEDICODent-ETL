# -*- coding: utf-8 -*-
"""sofi.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VrOkOpO1rUFGbsGAIwp5JfTlJHufmej5
"""

!pip install flask pandas openpyxl sqlalchemy python-dotenv gunicorn
!sudo apt update
!sudo apt install nginx
!sudo apt install certbot python3-certbot-nginx
!pip install -r requirements.txt





#lancer l'app avec gunicorn qui est un serveur sécurisé
!gunicorn -b 127.0.0.1:8000 app:app

from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
from openpyxl import load_workbook
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

app = Flask(__name__)

# Configuration de la base de données MySQL
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(DATABASE_URI)

@app.route('/')
def index():
    # Page d'accueil avec le formulaire de téléversement
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Gestion du téléversement de fichier
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and file.filename.endswith('.xlsx'):
        filepath = os.path.join('uploads', file.filename)
        file.save(filepath)
        process_file(filepath)
        return redirect(url_for('process'))
    return 'Invalid file format'

def process_file(filepath):
    # Traitement du fichier téléversé
    wb = load_workbook(filepath)
    ws = wb.active
    data = ws.values
    columns = next(data)[0:]
    df = pd.DataFrame(data, columns=columns)
    csv_filepath = filepath.replace('.xlsx', '.csv')
    df.to_csv(csv_filepath, index=False)
    load_to_database(df)

def load_to_database(df):
    # Chargement des données dans la base de données
    df.to_sql('your_table', con=engine, if_exists='replace', index=False)

@app.route('/process')
def process():
    # Page de confirmation du traitement
    return render_template('process.html')

if __name__ == '__main__':
    app.run(debug=True)



