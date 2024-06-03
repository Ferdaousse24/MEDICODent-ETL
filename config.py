import os

class Config:
    SECRET_KEY = '123abc'
    UPLOAD_FOLDER_IN = os.path.join('uploads', 'in')
    UPLOAD_FOLDER_OUT = os.path.join('uploads', 'out')
    ALLOWED_EXTENSIONS = {'xlsx'}