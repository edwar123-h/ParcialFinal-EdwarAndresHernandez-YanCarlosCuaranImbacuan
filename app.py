from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.secret_key = '8QRfaL38G5YglSFlEy35bBzWtAk12Kn0LF2zGUtB'

db = sqlite3.connect('data.db', check_same_thread=False)

# Rutas
@app.route('/', methods=['GET']) # / significa la ruta raiz
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET','POST']) # Ruta para LOGIN con metodo GET Y POST
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form.get('email')
    password = request.form.get('password')
    #PROCESO DE ENCRIPTACION DE CONTRASEÑA
    if request.method == 'POST':
        hashed_pw = generate_password_hash(request.form['password'], method="sha256")
        hashed_pw = password
    usuarios = db.execute (""" select * from usuarios where email =? and password =?""", (email,password,)).fetchone()
    
    if usuarios is None:
        flash('Las credencales no son válidas', 'error')
        return redirect(request.url)

    session ['usuarios'] = usuarios
    print(session['usuarios'])



    return redirect(url_for('index'))








@app.route('/logout') 
def logout():
    session.clear()
    return redirect(url_for('login'))
    









@app.route('/saludo/<nombre>/<int:edad>') # Nombre
def saludar(nombre, edad):
    numeros = [1,2,3,4,5,6,7,8,9]
    return render_template('saludo.html', name=nombre, age=edad, numbers=numeros)










@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    #VALIDACION DE LA RUTA PARA CONTACTO
    if not 'usuarios' in session:
        return redirect(url_for('login'))
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
    #VALIDACION DE LA RUTA PARA USUARIOS
    if not 'usuarios' in session:
        return redirect(url_for('login'))

   
    usuarios = db.execute('select * from usuarios')

    usuarios = usuarios.fetchall()
    
    return render_template('usuarios/listar.html', usuarios=usuarios)











@app.route('/usuarios/crear', methods=['GET', 'POST'])
def crear_usuarios():
    if request.method == 'GET':
        return render_template('/usuarios/crear.html')
    
    nombres = request.form.get('nombres')
    apellidos = request.form.get('apellidos')
    email = request.form.get('email')
    password = request.form.get('password')
    
    try:
        cursor = db.cursor()
        cursor.execute("""insert into usuarios(
                nombres,
                apellidos,
                email,
                password
            )values (?,?,?,?)
        """, (nombres, apellidos, email, password))
    except:
        flash('no se ha podido guardar el usuario', 'error')
        return redirect(url_for('usuarios'))
    db.commit()
    
    flash('usuario creado correctamente', 'success')

    return redirect(url_for('usuarios'))








@app.route('/categorias')

def categoria():
    
    if not 'usuarios' in session:
        return redirect(url_for('login'))

   
    categoria = db.execute('select * from categorias where idUsuario=?', (session['usuarios'][0],))

    categoria = categoria.fetchall()

    return render_template('usuarios/listar_categoria.html', categoria=categoria)








@app.route('/categorias/crear', methods=['GET','POST'])
def crear_categoria():
    if not 'usuarios' in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('usuarios/categorias.html')
   
    nombre = request.form.get('nombre')
    try:
        cursor = db.cursor()
        cursor.execute("""insert into categorias(
                nombre,
                idUsuario
                
            )values (?,?)
        """, (nombre,session['usuarios'][0],))
    except:
        flash('no se ha podido guardar la categoria', 'error')
        return redirect(url_for('categoria'))
    db.commit()
    
    flash('categoria creada correctamente', 'success')

    return redirect(url_for('categoria'))




# RUTAS PARA ACTUALIZAR, EDITAR Y ELIMINAR (CATEGORIAS)


@app.route('/usuarios/actualizar_categoria<num>', methods=('GET', 'POST'))
def actualizar_categoria(num):
    return render_template('usuarios/actualizar_categoria.html', num=db.execute('select * from categorias where id=?',(num,)).fetchone())



@app.route('/categorias/<id>', methods=('GET', 'POST'))
def editar_categoria(id):
    cursor=db.cursor()
    nombre = request.form.get('nombre')   
    cursor.execute(' UPDATE categorias SET nombre = ? WHERE id = ?',(nombre,id)) 
    db.commit()

    flash('categoria editada correctamente', 'success')

    return redirect(url_for('categoria'))




@app.route('/categorias/borrar<num>')
def borrar_categoria(num):
    cursor=db.cursor()
    cursor.execute('delete from categorias where id=?',(num,))
    db.commit()

    flash('categoria eliminada correctamente', 'success')

    return redirect(url_for('categoria'))


# RUTAS PARA ACTUALIZAR, EDITAR Y ELIMINAR (PRODUCTOS)

@app.route('/productos/actualizar_producto<num>', methods=('GET', 'POST'))
def actualizar_producto(num):
    return render_template('usuarios/actualizar_producto.html', num=db.execute('select * from productos where id=?',(num,)).fetchone())




@app.route('/productos/<id>', methods=('GET', 'POST'))
def editar_producto(id):
    cursor=db.cursor()
    nombre = request.form.get('nombre')
    precio = request.form.get('precio')
    categoria = request.form.get('categoria')   
    cursor.execute(' UPDATE productos SET nombre = ?, precio = ?, categoria = ? WHERE id = ?',(nombre,precio,categoria,id)) 
    db.commit()

    flash('producto editado correctamente', 'success')

    return redirect(url_for('producto'))


@app.route('/productos/borrar<num>')
def borrar_producto(num):
    cursor=db.cursor()
    cursor.execute('delete from productos where id=?',(num,))
    db.commit()

    flash('producto eliminado correctamente', 'success')

    return redirect(url_for('producto'))





@app.route('/productos')

def producto():
    
    if not 'usuarios' in session:
        return redirect(url_for('login'))

   
    producto = db.execute('select * from productos where idUsuario=?', (session['usuarios'][0],))

    producto = producto.fetchall()

    return render_template('usuarios/listar_producto.html', producto=producto)







@app.route('/productos/crear', methods=['GET','POST'])
def crear_producto():
    if not 'usuarios' in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('usuarios/crear_producto.html')
   
    nombre = request.form.get('nombre')
    precio = request.form.get('precio')
    categoria = request.form.get('categoria')
    try:
        cursor = db.cursor()
        cursor.execute("""insert into productos(
                nombre,
                precio,
                categoria,
                idUsuario
            )values (?,?,?,?)
        """, (nombre,precio,categoria, session['usuarios'][0]))
    except:
        flash('no se ha podido guardar el producto', 'error')
        return redirect(url_for('producto'))
    db.commit()
    
    flash('producto creado correctamente', 'success')

    return redirect(url_for('producto'))
    










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

    flash('usuario editado correctamente', 'success')

    return redirect(url_for('usuarios'))










@app.route('/usuarios/borrar<num>')
def borrar(num):
    cursor=db.cursor()
    cursor.execute('delete from usuarios where id=?',(num,))
    db.commit()

    flash('usuario eliminado correctamente', 'success')

    return redirect(url_for('usuarios'))









app.run(debug=True)

