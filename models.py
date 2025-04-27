from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(150), unique=True, nullable=False)
    contrasena_hash = db.Column(db.String(256), nullable=False)
    tareas = db.relationship('Tarea', backref='usuario', lazy=True)
    
    def set_password(self, contrasena):
        self.contrasena_hash = generate_password_hash(contrasena)
    def check_password(self, contrasena):
        return check_password_hash(self.contrasena_hash, contrasena)
    def __repr__(self):
        return f'<Usuario {self.nombre}>'

class Tarea(db.Model):
    __tablename__ = 'tareas'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_vencimiento = db.Column(db.DateTime, nullable=False)
    completada = db.Column(db.Boolean, default=False)
    prioridad = db.Column(db.String(50), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)