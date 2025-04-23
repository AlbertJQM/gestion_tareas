from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/tasks')
def list_tasks():
    return render_template('tasks.html')

@app.route('/task/<int:id>')
def view_task(id):
    return render_template('task.html')

@app.route('/task/create', methods=['GET', 'POST'])
def create_task():
    return render_template('create_task.html')

@app.route('/task/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    return render_template('edit_task.html')

@app.route('/task/delete/<int:id>', methods=['POST'])
def delete_task(id):
    redirect(url_for('list_tasks'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)