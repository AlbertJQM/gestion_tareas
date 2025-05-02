import os
from urllib.parse import urlparse

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    
    # Configuración para desarrollo/producción
    if os.environ.get('DATABASE_URL'):  # Entorno de producción (Heroku)
        uri = os.environ['DATABASE_URL']
        if uri.startswith("postgres://"):
            uri = uri.replace("postgres://", "postgresql://", 1)  # Solución para Heroku
        SQLALCHEMY_DATABASE_URI = uri
    else:  # Entorno local
        SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:muyiga128@localhost:5432/app_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mi-clave-secreta'

    """
    # Configuración de SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    # Para usar PostgreSQL, cambiar a:
    # SQLALCHEMY_DATABASE_URI = 'postgresql://usuario:contraseña@localhost/nombre_base_datos'
    # Para usar MySQL, cambiar a:
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://usuario:contraseña@localhost/nombre_base_datos'
    # Configuración de conexión a la base de datos
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Clave secreta para sesiones (crear una única para producción)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mi-clave-secreta'
    """