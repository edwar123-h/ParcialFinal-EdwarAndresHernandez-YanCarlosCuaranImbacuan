from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
db = sqlite3.connect('data.db', check_same_thread=False)

# Rutas
@app.route('/', methods=['GET']) # / significa la ruta raiz
def index():
    return render_template('index.html')

@app.route('/saludo/<nombre>/<int:edad>') # Nombre
def saludar(nombre, edad):
    numeros = [1,2,3,4,5,6,7,8,9]
    return render_template('saludo.html', name=nombre, age=edad, numbers=numeros)

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    #Obteniendo formulario de contacto
    if request.method == 'GET':
        return render_template('contacto.html')
    
    #Guardando la información de contacto
    nombres = request.form.get('nombres')
    email = request.form.get('email')
    celular = request.form.get('celular')
    observacion = request.form.get('observacion')

    

    return 'Guardando información ' + observacion
    
@app.route('/sumar')
def sumar():
    resultado = 2+2
    return 'la suma de 2+2=' + str(resultado)

@app.route('/usuarios')
def usuarios():
    usuarios = db.execute('select * from usuarios')

    usuarios = usuarios.fetchall()

    return render_template('usuarios/listar.html', usuarios=usuarios)

@app.route('/usuarios/crear', methods=['GET', 'POST'])
def crear_usuarios():
    if request.method == 'GET':
        return render_template('usuarios/crear.html')
    
    nombres = request.form.get('nombres')
    apellidos = request.form.get('apellidos')
    email = request.form.get('email')
    password = request.form.get('password')

    cursor = db.cursor()
    cursor.execute("""insert into usuarios(
            nombres,
            apellidos,
            email,
            password
        )values (?,?,?,?)
    """, (nombres, apellidos, email, password))

    db.commit()

    return redirect(url_for('usuarios'))

@app.route('/usuarios/actualizar<num>', methods=('GET', 'POST'))
def actualizar(num):
    return render_template('usuarios/actualizar.html', num=db.execute('select * from usuarios where id=?',(num,)).fetchone())

@app.route('/usuarios/<id>', methods=('GET', 'POST'))
def editar(id):
    cursor=db.cursor()
    nombres = request.form.get('nombres')    
    apellidos = request.form.get('apellidos')    
    email = request.form.get('email')    
    password = request.form.get('password')
    cursor.execute(' UPDATE usuarios SET nombres = ?, apellidos = ?, email = ?,password = ? WHERE id = ?',(nombres, apellidos, email, password, id)) 
    db.commit()
    return redirect(url_for('usuarios'))

@app.route('/usuarios/borrar<num>')
def borrar(num):
    cursor=db.cursor()
    cursor.execute('delete from usuarios where id=?',(num,))
    db.commit()
    return redirect(url_for('usuarios'))




app.run(debug=True)

