from flask import current_app

def allowed_file(filename):
    """Vérifie si le fichier a une extension autorisée."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']