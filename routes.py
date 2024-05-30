from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
import os
from utils import allowed_file

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

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
                
                # Message de réussite
                flash('Fichiers téléchargés avec succès', 'success')
            except Exception as e:
                flash(f'Une erreur est survenue: {e}', 'danger')
                return redirect(request.url)

            return redirect(url_for('main.index'))
        else:
            flash('Les types de fichiers autorisés sont .xlsx', 'danger')
            return redirect(request.url)
    
    #request.method == 'GET'
    return render_template('upload.html')