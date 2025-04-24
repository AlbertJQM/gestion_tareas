from flask import Flask, render_template, redirect, url_for, request, session
from config import Config
from models import db, Usuario, Tarea
from functools import wraps

app = Flask(__name__)
app.config.from_object(Config)

# Inicializa la base de datos
db.init_app(app)
# Crea las tablas en la base de datos si no existen
with app.app_context():
    db.create_all()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Aquí iría la lógica de autenticación
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        
        usuario = Usuario.query.filter_by(correo=correo).first()
        
        if usuario and usuario.check_password(contrasena):
            # Aquí iría la lógica para iniciar sesión
            session['usuario_id'] = usuario.id
            session['usuario_nombre'] = usuario.nombre
            return redirect(url_for('list_tasks'))
        
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    # Elimina la sesión del usuario
    session.clear()
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Aquí iría la lógica para registrar un nuevo usuario
        nombre = request.form['nombre']
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        
        nuevo_usuario = Usuario(nombre=nombre, correo=correo)
        nuevo_usuario.set_password(contrasena)
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/tasks')
@login_required
def list_tasks():
    filtro = request.args.get('filtro')
    if filtro == 'pendiente':
        tareas = Tarea.query.filter_by(usuario_id=session['usuario_id'], completada=False).all()
    elif filtro == 'completada':
        tareas = Tarea.query.filter_by(usuario_id=session['usuario_id'], completada=True).all()
    else:
        filtro = ''
        tareas = Tarea.query.filter_by(usuario_id=session['usuario_id']).all()
    
    cantidad_tareas = {
        'todas': len(tareas),
        'pendientes': sum(1 for tarea in tareas if not tarea.completada),
        'completadas': sum(1 for tarea in tareas if tarea.completada)
    }
    return render_template('tasks.html', tareas=tareas, filtro=filtro, cantidad_tareas=cantidad_tareas)

@app.route('/task/<int:id>')
@login_required
def view_task(id):
    return render_template('task.html')

@app.route('/task/create', methods=['GET', 'POST'])
@login_required
def create_task():
    return render_template('create_task.html')

@app.route('/task/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    return render_template('edit_task.html')

@app.route('/task/delete/<int:id>', methods=['POST'])
@login_required
def delete_task(id):
    redirect(url_for('list_tasks'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)