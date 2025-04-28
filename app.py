from flask import Flask, render_template, redirect, url_for, request, session
from config import Config
from models import db, Usuario, Tarea
from functools import wraps
from datetime import datetime

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
    filtro = request.args.get('filtro', default='todas')
    tareas = Tarea.query.filter_by(usuario_id=session['usuario_id']).all()
    cantidad_tareas = {
        'todas': len(tareas),
        'pendientes': sum(1 for tarea in tareas if not tarea.completada),
        'completadas': sum(1 for tarea in tareas if tarea.completada)
    }
    if filtro == 'pendiente':
        tareas = Tarea.query.filter_by(usuario_id=session['usuario_id'], completada=False).all()
    elif filtro == 'completada':
        tareas = Tarea.query.filter_by(usuario_id=session['usuario_id'], completada=True).all()
    else:
        filtro = 'todas'
    
    print(filtro, cantidad_tareas)
    return render_template('tasks.html', tareas=tareas, filtro=filtro, cantidad_tareas=cantidad_tareas)

@app.route('/task/<int:id>')
@login_required
def view_task(id):
    tarea = Tarea.query.get_or_404(id)
    return render_template('task.html', tarea=tarea)

@app.route('/task/create', methods=['GET', 'POST'])
@login_required
def create_task():
    if request.method == 'POST':
        # Aquí iría la lógica para crear una nueva tarea
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        fecha_vencimiento = datetime.strptime(request.form['fecha'],'%Y-%m-%d')
        prioridad = request.form['prioridad']
        
        try:        
            nueva_tarea = Tarea(titulo=titulo, descripcion=descripcion, fecha_vencimiento=fecha_vencimiento, prioridad=prioridad, usuario_id=session['usuario_id'])
            db.session.add(nueva_tarea)
            db.session.commit()
            return redirect(url_for('list_tasks'))
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear la tarea: {e}")
    return render_template('create_task.html')

@app.route('/task/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    tarea = Tarea.query.get_or_404(id)
    if request.method == 'POST':
        # Aquí iría la lógica para editar una tarea existente
        tarea.titulo = request.form['titulo']
        tarea.descripcion = request.form['descripcion']
        tarea.fecha_vencimiento = request.form['fecha_vencimiento']
        tarea.prioridad = request.form['prioridad']
        
        try:
            db.session.commit()
            return redirect(url_for('list_tasks'))
        except Exception as e:
            db.session.rollback()
    return render_template('edit_task.html', tarea=tarea)

@app.route('/task/delete/<int:id>', methods=['POST'])
@login_required
def delete_task(id):
    tarea = Tarea.query.get_or_404(id)
    try:
        db.session.delete(tarea)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('list_tasks'))

@app.route('/task/complete/<int:id>', methods=['POST'])
@login_required
def complete_task(id):
    tarea = Tarea.query.get_or_404(id)
    try:
        tarea.completada = not tarea.completada    
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('list_tasks'))

def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.register_error_handler(404, not_found)
    app.run(debug=True, host='127.0.0.1', port=5000)