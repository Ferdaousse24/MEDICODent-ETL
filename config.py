import os

class Config:
    SECRET_KEY = '123abc'
    UPLOAD_FOLDER_IN = os.path.join('uploads', 'in')
    ALLOWED_EXTENSIONS = {'xlsx'}