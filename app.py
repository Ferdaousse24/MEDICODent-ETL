from flask import Flask
from routes import main

app = Flask(__name__)

# Enregistre le blueprint pour les routes principales
app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)