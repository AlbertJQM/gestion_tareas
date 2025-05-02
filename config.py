import os
from urllib.parse import urlparse

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Configuración general
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mi-clave-secreta')
    
    # Configuración de PostgreSQL
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        # Obtener DATABASE_URL de Railway
        db_url = os.environ.get('DATABASE_URL')
        
        if db_url:
            # Railway usa formato postgresql:// directamente
            if db_url.startswith("postgres://"):
                db_url = db_url.replace("postgres://", "postgresql://", 1)
            return db_url
        else:
            # Configuración local de desarrollo
            return 'postgresql://postgres:muyiga128@localhost:5432/app_db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración adicional para producción
    @property
    def POSTGRES_CONFIG(self):
        """Extrae componentes individuales de la conexión para otros usos"""
        if not hasattr(self, '_postgres_config'):
            db_url = self.SQLALCHEMY_DATABASE_URI
            if db_url:
                result = urlparse(db_url)
                self._postgres_config = {
                    'host': result.hostname,
                    'port': result.port,
                    'user': result.username,
                    'password': result.password,
                    'database': result.path[1:]  # Elimina el / inicial
                }
            else:
                self._postgres_config = None
        return self._postgres_config

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