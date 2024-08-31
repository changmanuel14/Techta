from flask import Flask, render_template, request, url_for, redirect, session, flash, Blueprint
import pymysql
from datetime import datetime, date
from os import getcwd
from werkzeug.security import generate_password_hash, check_password_hash
from conexion import Conhost, Conuser, Conpassword, Condb

app = Flask(__name__)
app.secret_key = 'd589d3d0d15d764ed0a98ff5a37af547'

route_files = Blueprint("route_files", __name__)
mi_string = chr(92)
PATH_FILE = getcwd() +  r'/static/savedphotos/'

#General
@app.route('/', methods=['GET', 'POST'])
def home():
	return render_template('home.html', title="Inicio")

#Administrativo
@app.route('/admin', methods=['GET', 'POST'])
def admin():
	if 'usuario' in session and session['tipouser'] == 1:
		pass
	else:
		return redirect(url_for('loginadmin'))

	return render_template('admin.html', title="Portal Administrativo")

#Catedratico
@app.route('/catedraticos', methods=['GET', 'POST'])
def catedraticos():
	if 'usuario' in session and session['tipouser'] == 2:
		pass
	else:
		return redirect(url_for('logincatedratico'))

	return render_template('catedraticos.html', title="Portal de Catedraticos")

#Administrativo
@app.route('/catedratico', methods=['GET', 'POST'])
def catedratico():
	if 'usuario' in session and session['tipouser'] == 1:
		pass
	else:
		return redirect(url_for('loginadmin'))
	try:
		conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
		try:
			with conexion.cursor() as cursor:
				consulta = "SELECT c.idcatedratico, n.abreviatura, c.nombre1, c.nombre2, c.apellido1, c.apellido2, c.apellido3 FROM catedratico c inner join nivelacademico n on n.idnivelacademico = c.idnivelacademico order by nombre1 asc, nombre2 asc"
				cursor.execute(consulta)
				catedraticos = cursor.fetchall()
		finally:
			conexion.close()
	except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
		print("Ocurrió un error al conectar: ", e)
	return render_template('catedratico.html', title="Catedráticos", catedraticos = catedraticos)

#Administrativo
@app.route('/nuevocatedratico', methods=['GET', 'POST'])
def nuevocatedratico():
	if 'usuario' in session and session['tipouser'] == 1:
		pass
	else:
		return redirect(url_for('loginadmin'))
	try:
		conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
		try:
			with conexion.cursor() as cursor:
				consulta = "SELECT idnivelacademico, nombre, abreviatura FROM nivelacademico order by nombre asc"
				cursor.execute(consulta)
				niveles = cursor.fetchall()
		finally:
			conexion.close()
	except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
		print("Ocurrió un error al conectar: ", e)
	if request.method == 'POST':
		nombre1 = request.form['nombre1']
		nombre2 = request.form['nombre2']
		apellido1 = request.form['apellido1']
		apellido2 = request.form['apellido2']
		apellido3 = request.form['apellido3']
		telefono = request.form['telefono']
		celular = request.form['celular']
		correo = request.form['correo']
		genero = request.form['genero']
		fechanacimiento = request.form['fechanacimiento']
		nivelacademico = request.form['nivelacademico']
		try:
			conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
			try:
				with conexion.cursor() as cursor:
					consulta = "insert into catedratico(nombre1, nombre2, apellido1, apellido2, apellido3, telefono, celular, correo, idgenero, fechanacimiento, idnivelacademico) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
					cursor.execute(consulta, (nombre1, nombre2, apellido1, apellido2, apellido3, telefono, celular, correo, genero, fechanacimiento, nivelacademico))
					conexion.commit()
					consulta = 'select max(idcatedratico) from catedratico'
					cursor.execute(consulta)
					idcatedratico = cursor.fetchone()
					cont = 1
					salir = False
					while salir != True:
						usuario = nombre1.lower() + apellido1.lower() + str(cont)
						consulta = f"select count(iduser), usuario from user where usuario = '{usuario}'"
						cursor.execute(consulta)
						usuarios = cursor.fetchone()
						if int(usuarios[0]) < 1:
							fecha_objeto = datetime.strptime(fechanacimiento, "%Y-%m-%d")
							fecha_formateada = fecha_objeto.strftime("%d%m%Y")
							consulta = "insert into user(usuario, clave, idtipousuario, idconexion) values (%s,%s,%s,%s);"
							cursor.execute(consulta, (usuario, generate_password_hash(fecha_formateada), 2, idcatedratico))
							conexion.commit()
							salir = True
						else:
							cont = cont + 1
			finally:
				conexion.close()
		except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
			print("Ocurrió un error al conectar: ", e)
		return redirect(url_for('catedratico'))
	return render_template('nuevocatedratico.html', title="Nuevo Catedratico", niveles = niveles)

#Administrativo
@app.route('/editarcatedratico/<idcatedratico>', methods=['GET', 'POST'])
def editarcatedratico(idcatedratico):
	if 'usuario' in session and session['tipouser'] == 1 or session['tipouser'] == 2:
		pass
	else:
		return redirect(url_for('loginadmin'))
	try:
		conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
		try:
			with conexion.cursor() as cursor:
				consulta = "SELECT idnivelacademico, nombre, abreviatura FROM nivelacademico order by nombre asc"
				cursor.execute(consulta)
				niveles = cursor.fetchall()
				consulta = "SELECT nombre1, nombre2, apellido1, apellido2, apellido3, correo, idgenero, fechanacimiento, telefono, celular, idnivelacademico FROM catedratico where idcatedratico = %s"
				cursor.execute(consulta, idcatedratico)
				catedratico = cursor.fetchone()
		finally:
			conexion.close()
	except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
		print("Ocurrió un error al conectar: ", e)
	if request.method == 'POST':
		nombre1 = request.form['nombre1']
		nombre2 = request.form['nombre2']
		apellido1 = request.form['apellido1']
		apellido2 = request.form['apellido2']
		apellido3 = request.form['apellido3']
		telefono = request.form['telefono']
		celular = request.form['celular']
		correo = request.form['correo']
		genero = request.form['genero']
		fechanacimiento = request.form['fechanacimiento']
		nivelacademico = request.form['nivelacademico']
		try:
			conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
			try:
				with conexion.cursor() as cursor:
					consulta = "update catedratico set nombre1 = %s, nombre2 = %s, apellido1 = %s, apellido2 = %s, apellido3 = %s, telefono = %s, celular = %s, correo = %s, idgenero = %s, fechanacimiento = %s, idnivelacademico = %s where idcatedratico = %s"
					cursor.execute(consulta, (nombre1, nombre2, apellido1, apellido2, apellido3, telefono, celular, correo, genero, fechanacimiento, nivelacademico, idcatedratico))
				conexion.commit()
			finally:
				conexion.close()
		except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
			print("Ocurrió un error al conectar: ", e)
		return redirect(url_for('catedratico'))
	return render_template('editarcatedratico.html', title="Editar Catedratico", niveles = niveles, catedratico = catedratico)

#Estudiantes
@app.route('/estudiantes', methods=['GET', 'POST'])
def estudiantes():
	if 'usuario' in session and session['tipouser'] == 3:
		pass
	else:
		return redirect(url_for('loginestudiante'))

	return render_template('estudiantes.html', title="Portal de Estudiantes")

#Estudiantes
@app.route('/asignacionesestudiante', methods=['GET', 'POST'])
def asignacionesestudiante():
	if 'usuario' in session and session['tipouser'] == 3:
		pass
	else:
		return redirect(url_for('loginestudiante'))
	hoy = date.today()
	try:
		conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
		try:
			with conexion.cursor() as cursor:
				consulta = "select idconexion from user where iduser = %s"
				cursor.execute(consulta, session["idusuario"])
				idestudiante = cursor.fetchone()
				idestudiante = idestudiante[0]
				consulta = f"Select c.idclase from clase c inner join claseestudiante ce on c.idclase = ce.idclase where ce.idestudiante = {idestudiante} and c.fechafin >= '{hoy}'"
				cursor.execute(consulta)
				idcursos = cursor.fetchall()
				clases = []
				for i in idcursos:
					consulta = f"SELECT c.nombre, CONCAT(d.nombre1,' ',d.nombre2,' ',d.apellido1,' ',d.apellido2,' ',d.apellido3), p.plan, DATE_FORMAT(l.fechainicio,'%d/%m/%Y'), DATE_FORMAT(l.fechafin,'%d/%m/%Y'), l.idclase from clase l inner join plan p on p.idplan = l.idplan inner join curso c on c.idcurso = l.idcurso inner join catedratico d on d.idcatedratico = l.idcatedratico where l.idclase = {i[0]} order by c.nombre asc"
					cursor.execute(consulta)
					curso = cursor.fetchone()
					clases.append(curso)
		finally:
			conexion.close()
	except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
		print("Ocurrió un error al conectar: ", e)
	return render_template('asignacionesestudiante.html', title="Clases Actuales", clases = clases)

#Estudiantes
@app.route('/historialestudiante', methods=['GET', 'POST'])
def historialestudiante():
	if 'usuario' in session and session['tipouser'] == 3:
		pass
	else:
		return redirect(url_for('loginestudiante'))
	hoy = date.today()
	try:
		conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
		try:
			with conexion.cursor() as cursor:
				consulta = "select idconexion from user where iduser = %s"
				cursor.execute(consulta, session["idusuario"])
				idestudiante = cursor.fetchone()
				idestudiante = idestudiante[0]
				consulta = f"Select c.idclase from clase c inner join claseestudiante ce on c.idclase = ce.idclase where ce.idestudiante = {idestudiante} and c.fechafin < '{hoy}'"
				cursor.execute(consulta)
				idcursos = cursor.fetchall()
				clases = []
				for i in idcursos:
					consulta = f"SELECT c.nombre, CONCAT(d.nombre1,' ',d.nombre2,' ',d.apellido1,' ',d.apellido2,' ',d.apellido3), p.plan, DATE_FORMAT(l.fechainicio,'%d/%m/%Y'), DATE_FORMAT(l.fechafin,'%d/%m/%Y'), l.idclase from clase l inner join plan p on p.idplan = l.idplan inner join curso c on c.idcurso = l.idcurso inner join catedratico d on d.idcatedratico = l.idcatedratico where l.idclase = {i[0]} order by c.nombre asc"
					cursor.execute(consulta)
					curso = cursor.fetchone()
					print(curso)
					clases.append(curso)
		finally:
			conexion.close()
	except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
		print("Ocurrió un error al conectar: ", e)
	return render_template('historialestudiante.html', title="Clases Actuales", clases = clases)

#Estudiantes
@app.route('/vertareasest/<idclase>', methods=['GET', 'POST'])
def vertareasest(idclase):
	if 'usuario' in session and session['tipouser'] == 3:
		pass
	else:
		return redirect(url_for('loginestudiante'))
	hoy = date.today()
	try:
		conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
		try:
			with conexion.cursor() as cursor:
				consulta = "select idconexion from user where iduser = %s"
				cursor.execute(consulta, session["idusuario"])
				idestudiante = cursor.fetchone()
				idestudiante = idestudiante[0]
				consulta = f"SELECT c.nombre, CONCAT(d.nombre1,' ',d.nombre2,' ',d.apellido1,' ',d.apellido2,' ',d.apellido3), p.plan, DATE_FORMAT(l.fechainicio,'%d/%m/%Y'), DATE_FORMAT(l.fechafin,'%d/%m/%Y'), l.idclase from clase l inner join plan p on p.idplan = l.idplan inner join curso c on c.idcurso = l.idcurso inner join catedratico d on d.idcatedratico = l.idcatedratico where l.idclase = {idclase} order by c.nombre asc"
				cursor.execute(consulta)
				datacurso = cursor.fetchone()
				consulta = f"Select t.concepto, DATE_FORMAT(t.fecha,'%d/%m/%Y'), te.nota from zona t inner join zonaestudiante te on te.idzona = t.idzona where te.idestudiante = {idestudiante} and t.idcurso = {idclase} group by t.idzona order by t.fecha asc"
				cursor.execute(consulta)
				tareas = cursor.fetchall()
				print(consulta)
				suma = 0
				for i in tareas:
					suma = suma + float(i[2])
		finally:
			conexion.close()
	except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
		print("Ocurrió un error al conectar: ", e)
	return render_template('vertareasest.html', title="Visualizacion de Nota", tareas = tareas, suma = suma, datacurso=datacurso)

#Administrativo
@app.route('/estudiante', methods=['GET', 'POST'])
def estudiante():
	if 'usuario' in session and session['tipouser'] == 1:
		pass
	else:
		return redirect(url_for('loginadmin'))
	try:
		conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
		try:
			with conexion.cursor() as cursor:
				consulta = "SELECT e.idestudiante, e.nombre1, e.nombre2, e.apellido1, e.apellido2, e.apellido3, e.carnet FROM estudiante e order by e.nombre1 asc, e.nombre2 asc"
				cursor.execute(consulta)
				estudiantes = cursor.fetchall()
		finally:
			conexion.close()
	except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
		print("Ocurrió un error al conectar: ", e)
	return render_template('estudiante.html', title="Estudiantes", estudiantes = estudiantes)

#Administrativo
@app.route('/nuevoestudiante', methods=['GET', 'POST'])
def nuevoestudiante():
	if 'usuario' in session and session['tipouser'] == 1:
		pass
	else:
		return redirect(url_for('loginadmin'))
	try:
		conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
		try:
			with conexion.cursor() as cursor:
				consulta = "SELECT idcurso, nombre FROM curso order by nombre asc"
				cursor.execute(consulta)
				cursos = cursor.fetchall()
		finally:
			conexion.close()
	except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
		print("Ocurrió un error al conectar: ", e)
	if request.method == 'POST':
		nombre1 = request.form['nombre1']
		nombre2 = request.form['nombre2']
		apellido1 = request.form['apellido1']
		apellido2 = request.form['apellido2']
		apellido3 = request.form['apellido3']
		telefono = request.form['telefono']
		celular = request.form['celular']
		correo = request.form['correo']
		genero = request.form['genero']
		fechanacimiento = request.form['fechanacimiento']
		curso = request.form['curso']
		current_year = datetime.now().year
		precarnet = str(current_year) + curso.rjust(2, '0')
		try:
			conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
			try:
				with conexion.cursor() as cursor:
					consulta = f"Select max(carnet) from estudiante where carnet like '%{precarnet}%'"
					cursor.execute(consulta)
					maxcarnet = cursor.fetchall()
					try:
						maxcarnet = str(maxcarnet[0][0])
						carnet = int(maxcarnet[6:]) + 1
					except:
						carnet = 1
					carnet = precarnet + str(carnet).rjust(3, '0')
					try:
						if 'foto' in request.files:
							foto = request.files['foto']
							data = foto.filename.split('.')
							aux = carnet + "." + data[1]
							foto.save(PATH_FILE + aux)
					except:
						aux = ""
					consulta = "insert into estudiante(nombre1, nombre2, apellido1, apellido2, apellido3, telefono, celular, correo, idgenero, fechanacimiento, carnet, foto) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
					cursor.execute(consulta, (nombre1, nombre2, apellido1, apellido2, apellido3, telefono, celular, correo, genero, fechanacimiento, carnet, aux))
					conexion.commit()
					consulta = 'select max(idestudiante) from estudiante'
					cursor.execute(consulta)
					idestudiante = cursor.fetchone()
					fecha_objeto = datetime.strptime(fechanacimiento, "%Y-%m-%d")
					fecha_formateada = fecha_objeto.strftime("%d%m%Y")
					print(fecha_formateada)
					consulta = "insert into user(usuario, clave, idtipousuario, idconexion) values (%s,%s,%s,%s);"
					cursor.execute(consulta, (carnet, generate_password_hash(fecha_formateada), 3, idestudiante))
					conexion.commit()
			finally:
				conexion.close()
		except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
			print("Ocurrió un error al conectar: ", e)
		return redirect(url_for('perfilestudiante', id=idestudiante))
	return render_template('nuevoestudiante.html', title="Nuevo Estudiante", cursos = cursos)

#Administrativo
@app.route('/editarestudiante/<id>', methods=['GET', 'POST'])
def editarestudiante(id):
	if 'usuario' in session and session['tipouser'] == 1:
		pass
	else:
		return redirect(url_for('loginadmin'))
	try:
		conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
		try:
			with conexion.cursor() as cursor:
				consulta = "SELECT idcurso, nombre FROM curso order by nombre asc"
				cursor.execute(consulta)
				cursos = cursor.fetchall()
				consulta = "Select nombre1, nombre2, apellido1, apellido2, apellido3, telefono, celular, correo, idgenero, fechanacimiento, carnet, foto from estudiante where idestudiante = %s"
				cursor.execute(consulta, id)
				estudiante = cursor.fetchone()
		finally:
			conexion.close()
	except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
		print("Ocurrió un error al conectar: ", e)
	if request.method == 'POST':
		nombre1 = request.form['nombre1']
		nombre2 = request.form['nombre2']
		apellido1 = request.form['apellido1']
		apellido2 = request.form['apellido2']
		apellido3 = request.form['apellido3']
		telefono = request.form['telefono']
		celular = request.form['celular']
		correo = request.form['correo']
		genero = request.form['genero']
		fechanacimiento = request.form['fechanacimiento']
		try:
			foto = request.files['foto']
			print(PATH_FILE)
			data = foto.filename.split('.')
			aux = estudiante[10] + "." + data[1]
			foto.save(PATH_FILE + aux)
		except:
			aux = estudiante[11]
		try:
			conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
			try:
				with conexion.cursor() as cursor:
					consulta = "update estudiante set nombre1 = %s, nombre2 = %s, apellido1 = %s, apellido2 = %s, apellido3 = %s, telefono = %s, celular = %s, correo = %s, idgenero = %s, fechanacimiento = %s, foto = %s where idestudiante = %s;"
					cursor.execute(consulta, (nombre1, nombre2, apellido1, apellido2, apellido3, telefono, celular, correo, genero, fechanacimiento, aux, id))
					conexion.commit()
			finally:
				conexion.close()
		except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
			print("Ocurrió un error al conectar: ", e)
		return redirect(url_for('perfilestudiante', id=id))
	return render_template('editarestudiante.html', title="Editar Estudiante", cursos = cursos, estudiante = estudiante)

#Administrativo
@app.route('/buscarestudiante', methods=['GET', 'POST'])
def buscarestudiante():
	if 'usuario' in session and session['tipouser'] == 1:
		pass
	else:
		return redirect(url_for('home'))
	estudiantes = []
	carreras = []
	cantidad = 0
	nombre = ""
	carnet = ""
	if request.method == 'POST':
		carnet = request.form['carnet']
		nombre = request.form['nombre']
		try:
			conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
			try:
				with conexion.cursor() as cursor:
					nombre = nombre.replace(" ", "%")
					consulta = f"select idestudiante, nombre1, nombre2, apellido1, apellido2, apellido3, carnet, foto from estudiante where CONCAT(nombre1,' ',nombre2,' ',apellido1,' ',apellido2,' ',apellido3) LIKE '%{nombre}%' and carnet like '%{carnet}%'"
					cursor.execute(consulta)
					estudiantes = cursor.fetchall()
					cantidad = len(estudiantes)
					carreras = []
					for i in estudiantes:
						carn = i[6]
						idcarrera = int(carn[4:6])
						consulta = "select abreviatura from curso where idcurso = %s"
						cursor.execute(consulta, idcarrera)
						carrera = cursor.fetchone()
						carreras.append(carrera)
			finally:
				conexion.close()
		except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
			print("Ocurrió un error al conectar: ", e)
	nombre = nombre.replace("%", " ")
	return render_template('buscarestudiante.html', title="Busqueda de Estudiante", estudiantes = estudiantes, carreras = carreras, cantidad = cantidad, nombre = nombre, carnet = carnet)

#Administrativo
@app.route('/perfilestudiante/<id>', methods=['GET', 'POST'])
def perfilestudiante(id):
	if 'usuario' in session and session['tipouser'] == 1:
		pass
	else:
		return redirect(url_for('home'))
	hoy = date.today()
	try:
		conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
		try:
			with conexion.cursor() as cursor:
				consulta = f"select idestudiante, nombre1, nombre2, apellido1, apellido2, apellido3, carnet, foto from estudiante where idestudiante = {id}"
				cursor.execute(consulta)
				estudiante = cursor.fetchone()
				carnet = estudiante[6]
				idcarrera = int(carnet[4:6])
				consulta = "select abreviatura, nombre from curso where idcurso = %s"
				cursor.execute(consulta, idcarrera)
				carrera = cursor.fetchone()
				consulta = f"select count(e.idestudiante) from claseestudiante e inner join clase c on c.idclase = e.idclase where e.idestudiante = {id} and c.fechafin > '{hoy}'"
				cursor.execute(consulta)
				cantidad = cursor.fetchone()
				if int(cantidad[0]) < 1:
					estado = "No inscrito"
				else:
					estado = "Inscrito"
		finally:
			conexion.close()
	except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
		print("Ocurrió un error al conectar: ", e)
	return render_template('perfilestudiante.html', title="Perfil de Estudiante", estudiante = estudiante, carrera = carrera, estado = estado)

#Administrativo
@app.route('/inscripcion/<id>', methods=['GET', 'POST'])
def inscripcion(id):
	if 'usuario' in session and session['tipouser'] == 1:
		pass
	else:
		return redirect(url_for('home'))
	hoy = date.today()
	mensaje = ""
	condicional = 0
	try:
		conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
		try:
			with conexion.cursor() as cursor:
				consulta = f"select idestudiante, nombre1, nombre2, apellido1, apellido2, apellido3, carnet, foto from estudiante where idestudiante = {id}"
				cursor.execute(consulta)
				estudiante = cursor.fetchone()
				consulta = f"SELECT c.nombre, CONCAT(d.nombre1,' ',d.nombre2,' ',d.apellido1,' ',d.apellido2,' ',d.apellido3), p.plan, DATE_FORMAT(l.fechainicio,'%d/%m/%Y'), DATE_FORMAT(l.fechafin,'%d/%m/%Y'), l.idclase from clase l inner join plan p on p.idplan = l.idplan inner join curso c on c.idcurso = l.idcurso inner join catedratico d on d.idcatedratico = l.idcatedratico where l.fechafin >= '{hoy}' order by c.nombre asc"
				cursor.execute(consulta)
				clases = cursor.fetchall()
				cant = len(clases)
				cantidades = []
				for i in clases:
					consulta = f"select count(idestudiante) from claseestudiante where idclase = {i[5]}"
					cursor.execute(consulta)
					cantidad = cursor.fetchone()
					cantidades.append(cantidad[0])
		finally:
			conexion.close()
	except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
		print("Ocurrió un error al conectar: ", e)
	if request.method == 'POST':
		for i in clases:
			try:
				aux = f"check{i[5]}"
				curso = request.form[aux]
				try:
					conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
					try:
						with conexion.cursor() as cursor:
							consulta = f"select * from claseestudiante where idclase = {i[5]} and idestudiante = {id}"
							cursor.execute(consulta)
							cantidadinscrito = cursor.fetchall()
							if len(cantidadinscrito) > 0:
								mensaje = 1
								condicional = 1
							else:
								consulta = "insert into claseestudiante(idclase, idestudiante, idestado, nota) values (%s,%s,1,0)"
								cursor.execute(consulta, (curso, id))
								conexion.commit()
								mensaje = 0
								consulta = "select idzona from zona where idcurso = %s"
								cursor.execute(consulta, (curso))
								tareas = cursor.fetchall()
								for i in tareas:
									consulta = "insert into zonaestudiante(idzona, idestudiante, nota) values(%s, %s, 0)"
									cursor.execute(consulta, (i[0], id))
									conexion.commit()
					finally:
						conexion.close()
				except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
					print("Ocurrió un error al conectar: ", e)
			except:
				pass
		if condicional == 0:
			return redirect(url_for('perfilestudiante', id=id))
	return render_template('inscripcion.html', title="Inscripción", estudiante = estudiante, clases = clases, cantidades = cantidades, cant = cant, mensaje=mensaje)

#Administrativo
@app.route('/curso', methods=['GET', 'POST'])
def curso():
	if 'usuario' in session and session['tipouser'] == 1:
		pass
	else:
		return redirect(url_for('loginadmin'))
	try:
		conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
		try:
			with conexion.cursor() as cursor:
				consulta = "SELECT c.nombre, i.nombre, c.idcurso, c.abreviatura from curso c inner join institucion i on i.idinstitucion = c.idinstitucion order by c.nombre asc"
				cursor.execute(consulta)
				cursos = cursor.fetchall()
		finally:
			conexion.close()
	except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
		print("Ocurrió un error al conectar: ", e)
	return render_template('curso.html', title="Cursos", cursos = cursos)

#Administrativo
@app.route('/nuevocurso', methods=['GET', 'POST'])
def nuevocurso():
	if 'usuario' in session and session['tipouser'] == 1:
		pass
	else:
		return redirect(url_for('loginadmin'))
	curso = ["", "", ""]
	mensaje = ""
	try:
		conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
		try:
			with conexion.cursor() as cursor:
				consulta = "SELECT idinstitucion, nombre, abreviatura FROM institucion order by nombre asc"
				cursor.execute(consulta)
				instituciones = cursor.fetchall()
		finally:
			conexion.close()
	except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
		print("Ocurrió un error al conectar: ", e)
	if request.method == 'POST':
		nombre = request.form['nombre']
		institucion = request.form['institucion']
		abreviatura = request.form['abreviatura']
		try:
			conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
			try:
				with conexion.cursor() as cursor:
					consulta = "select count(idcurso) from curso where abreviatura = %s"
					cursor.execute(consulta, abreviatura)
					numcurso = cursor.fetchone()
					numcurso = numcurso[0]
					if numcurso < 1:
						consulta = "insert into curso(nombre, idinstitucion, abreviatura) values (%s,%s,%s);"
						cursor.execute(consulta, (nombre, institucion, abreviatura))
						conexion.commit()
					else:
						mensaje = "Ya se ha creado un curso con esa abreviatura, intente nuevamente"
						curso = [nombre, int(institucion), abreviatura]
						return render_template('nuevocurso.html', title="Nuevo Curso", instituciones = instituciones, curso = curso, nuevo = 1, mensaje = mensaje)
			finally:
				conexion.close()
		except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
			print("Ocurrió un error al conectar: ", e)
		return redirect(url_for('curso'))
	return render_template('nuevocurso.html', title="Nuevo Curso", instituciones = instituciones, curso = curso, nuevo = 1, mensaje = mensaje)

#Administrativo
@app.route('/editarcurso/<idcurso>', methods=['GET', 'POST'])
def editarcurso(idcurso):
	if 'usuario' in session and session['tipouser'] == 1:
		pass
	else:
		return redirect(url_for('loginadmin'))
	mensaje = ""
	try:
		conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
		try:
			with conexion.cursor() as cursor:
				consulta = "SELECT idinstitucion, nombre, abreviatura FROM institucion order by nombre asc"
				cursor.execute(consulta)
				instituciones = cursor.fetchall()
				consulta = "SELECT nombre, idinstitucion, abreviatura FROM curso where idcurso = %s"
				cursor.execute(consulta, idcurso)
				curso = cursor.fetchone()
		finally:
			conexion.close()
	except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
		print("Ocurrió un error al conectar: ", e)
	if request.method == 'POST':
		nombre = request.form['nombre']
		institucion = request.form['institucion']
		abreviatura = request.form['abreviatura']
		try:
			conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
			try:
				with conexion.cursor() as cursor:
					consulta = "update curso set nombre = %s, idinstitucion = %s, abreviatura = %s where idcurso = %s;"
					cursor.execute(consulta, (nombre, institucion, abreviatura, idcurso))
					conexion.commit()
			finally:
				conexion.close()
		except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
			print("Ocurrió un error al conectar: ", e)
		return redirect(url_for('curso'))
	return render_template('nuevocurso.html', title="Editar Curso", instituciones = instituciones, curso = curso, nuevo = 0, mensaje = mensaje)

#Administrativo
@app.route('/clase', methods=['GET', 'POST'])
def clase():
	if 'usuario' in session and session['tipouser'] == 1:
		pass
	else:
		return redirect(url_for('loginadmin'))
	hoy = date.today()
	try:
		conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
		try:
			with conexion.cursor() as cursor:
				consulta = f"SELECT c.nombre, CONCAT(d.nombre1,' ',d.nombre2,' ',d.apellido1,' ',d.apellido2,' ',d.apellido3), p.plan, DATE_FORMAT(l.fechainicio,'%d/%m/%Y'), DATE_FORMAT(l.fechafin,'%d/%m/%Y'), l.idclase from clase l inner join plan p on p.idplan = l.idplan inner join curso c on c.idcurso = l.idcurso inner join catedratico d on d.idcatedratico = l.idcatedratico where l.fechafin >= '{hoy}' order by c.nombre asc"
				cursor.execute(consulta)
				clases = cursor.fetchall()
		finally:
			conexion.close()
	except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
		print("Ocurrió un error al conectar: ", e)
	return render_template('clase.html', title="Clases Activas", clases = clases)

#Administrativo
@app.route('/clasehistoricoadmin', methods=['GET', 'POST'])
def clasehistoricoadmin():
	if 'usuario' in session and session['tipouser'] == 1:
		pass
	else:
		return redirect(url_for('loginadmin'))
	hoy = date.today()
	try:
		conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
		try:
			with conexion.cursor() as cursor:
				consulta = f"SELECT c.nombre, CONCAT(d.nombre1,' ',d.nombre2,' ',d.apellido1,' ',d.apellido2,' ',d.apellido3), p.plan, DATE_FORMAT(l.fechainicio,'%d/%m/%Y'), DATE_FORMAT(l.fechafin,'%d/%m/%Y'), l.idclase from clase l inner join plan p on p.idplan = l.idplan inner join curso c on c.idcurso = l.idcurso inner join catedratico d on d.idcatedratico = l.idcatedratico where l.fechafin < '{hoy}' order by c.nombre asc"
				cursor.execute(consulta)
				clases = cursor.fetchall()
		finally:
			conexion.close()
	except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
		print("Ocurrió un error al conectar: ", e)
	return render_template('clase.html', title="Historico de Clases", clases = clases)

#Administrativo
@app.route('/nuevaclase', methods=['GET', 'POST'])
def nuevaclase():
	if 'usuario' in session and session['tipouser'] == 1:
		pass
	else:
		return redirect(url_for('loginadmin'))
	clase = ["", "", "", "", ""]
	try:
		conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
		try:
			with conexion.cursor() as cursor:
				consulta = "SELECT idcurso, nombre FROM curso order by nombre asc"
				cursor.execute(consulta)
				cursos = cursor.fetchall()
				consulta = "SELECT idplan, plan FROM plan order by plan asc"
				cursor.execute(consulta)
				planes = cursor.fetchall()
				consulta = "SELECT d.idcatedratico, n.abreviatura, CONCAT(d.nombre1,' ',d.nombre2,' ',d.apellido1,' ',d.apellido2,' ',d.apellido3) FROM catedratico d inner join nivelacademico n on n.idnivelacademico = d.idnivelacademico order by n.abreviatura asc, d.nombre1 asc, d.nombre2 asc, d.apellido1 asc, d.apellido2 asc, d.apellido3 asc"
				cursor.execute(consulta)
				catedraticos = cursor.fetchall()
		finally:
			conexion.close()
	except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
		print("Ocurrió un error al conectar: ", e)
	if request.method == 'POST':
		curso = request.form['curso']
		plan = request.form['plan']
		catedratico = request.form['catedratico']
		fechainicio = request.form['fechainicio']
		fechafin = request.form['fechafin']
		try:
			conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
			try:
				with conexion.cursor() as cursor:
					consulta = "insert into clase(idcurso, idcatedratico, idplan, fechainicio, fechafin) values (%s,%s,%s,%s,%s);"
					cursor.execute(consulta, (curso, catedratico, plan ,fechainicio, fechafin))
					conexion.commit()
			finally:
				conexion.close()
		except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
			print("Ocurrió un error al conectar: ", e)
		return redirect(url_for('clase'))
	return render_template('nuevaclase.html', title="Nueva Clase", cursos = cursos, clase = clase, planes = planes, catedraticos = catedraticos, nuevo = 1)

#Administrativo
@app.route('/editarclase/<idclase>', methods=['GET', 'POST'])
def editarclase(idclase):
	if 'usuario' in session and session['tipouser'] == 1:
		pass
	else:
		return redirect(url_for('loginadmin'))
	try:
		conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
		try:
			with conexion.cursor() as cursor:
				consulta = "SELECT idcurso, nombre FROM curso order by nombre asc"
				cursor.execute(consulta)
				cursos = cursor.fetchall()
				consulta = "SELECT idplan, plan FROM plan order by plan asc"
				cursor.execute(consulta)
				planes = cursor.fetchall()
				consulta = "SELECT d.idcatedratico, n.abreviatura, CONCAT(d.nombre1,' ',d.nombre2,' ',d.apellido1,' ',d.apellido2,' ',d.apellido3) FROM catedratico d inner join nivelacademico n on n.idnivelacademico = d.idnivelacademico order by n.abreviatura asc, d.nombre1 asc, d.nombre2 asc, d.apellido1 asc, d.apellido2 asc, d.apellido3 asc"
				cursor.execute(consulta)
				catedraticos = cursor.fetchall()
				consulta = f"select idcurso, idcatedratico, idplan, fechainicio, fechafin from clase where idclase = {idclase}"
				cursor.execute(consulta)
				clase = cursor.fetchone()
		finally:
			conexion.close()
	except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
		print("Ocurrió un error al conectar: ", e)
	if request.method == 'POST':
		curso = request.form['curso']
		plan = request.form['plan']
		catedratico = request.form['catedratico']
		fechainicio = request.form['fechainicio']
		fechafin = request.form['fechafin']
		try:
			conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
			try:
				with conexion.cursor() as cursor:
					consulta = "update clase set idcurso = %s, idcatedratico = %s, idplan =%s, fechainicio =%s, fechafin=%s where idclase = %s"
					cursor.execute(consulta, (curso, catedratico, plan ,fechainicio, fechafin, idclase))
					conexion.commit()
			finally:
				conexion.close()
		except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
			print("Ocurrió un error al conectar: ", e)
		return redirect(url_for('clase'))
	return render_template('nuevaclase.html', title="Editar Clase", cursos = cursos, clase = clase, planes = planes, catedraticos = catedraticos, nuevo = 0)

#Administrativo y Catedratico
@app.route('/claseestudiantes/<idclase>', methods=['GET', 'POST'])
def claseestudiantes(idclase):
	if 'usuario' in session and (session['tipouser'] == 2 or session['tipouser'] == 1):
		pass
	else:
		return redirect(url_for('home'))
	hoy = date.today()
	try:
		conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
		try:
			with conexion.cursor() as cursor:
				consulta = "select e.idestudiante, e.nombre1, e.nombre2, e.apellido1, e.apellido2, e.apellido3, e.carnet from estudiante e inner join claseestudiante ce on ce.idestudiante = e.idestudiante where ce.idclase = %s and ce.idestado = 1 order by e.nombre1, e.nombre2, e.apellido1, e.apellido2, e.apellido3"
				cursor.execute(consulta, idclase)
				estudiantes = cursor.fetchall()
				notas = []
				for i in estudiantes:
					consulta = "select COALESCE(sum(ze.nota), 0) from zonaestudiante ze inner join zona z on z.idzona = ze.idzona where ze.idestudiante = %s and z.idcurso = %s"
					cursor.execute(consulta, (i[0], idclase))
					nota = cursor.fetchone()
					notas.append(nota[0])
		finally:
			conexion.close()
	except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
		print("Ocurrió un error al conectar: ", e)
	return render_template('claseestudiantes.html', title="Estudiantes por Curso", estudiantes = estudiantes, notas = notas, idclase = idclase)

#Administrativo y Catedratico
@app.route('/notas/<idestudiante>', methods=['GET', 'POST'])
def notas(idestudiante):
	if 'usuario' in session and session['tipouser'] == 1:
		pass
	else:
		return redirect(url_for('home'))
	hoy = date.today()
	try:
		conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
		try:
			with conexion.cursor() as cursor:
				consulta = f"select idestudiante, nombre1, nombre2, apellido1, apellido2, apellido3, carnet, foto from estudiante where idestudiante = {idestudiante}"
				cursor.execute(consulta)
				estudiante = cursor.fetchone()
				consulta = "select cu.nombre, cl.fechainicio, cl.fechafin, cl.idclase from curso cu inner join clase cl on cl.idcurso = cu.idcurso inner join claseestudiante ce on ce.idclase = cl.idclase where ce.idestudiante = %s order by cl.fechainicio desc;"
				cursor.execute(consulta, idestudiante)
				clases = cursor.fetchall()
				notas = []
				for i in clases:
					consulta = "select COALESCE(sum(ze.nota), 0) from zonaestudiante ze inner join zona z on z.idzona = ze.idzona where ze.idestudiante = %s and z.idcurso = %s"
					cursor.execute(consulta, (idestudiante, i[3]))
					nota = cursor.fetchone()
					notas.append(nota[0])
		finally:
			conexion.close()
	except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
		print("Ocurrió un error al conectar: ", e)
	return render_template('notas.html', title="Notas de Estudiante", clases = clases, notas = notas, idestudiante = idestudiante, estudiante = estudiante)

#Catedratico
@app.route('/vertareas/<idclase>', methods=['GET', 'POST'])
def vertareas(idclase):
	if 'usuario' in session and session['tipouser'] == 2:
		pass
	else:
		return redirect(url_for('home'))
	hoy = date.today()
	try:
		conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
		try:
			with conexion.cursor() as cursor:
				consulta = f'select idzona, concepto, DATE_FORMAT(fecha,"%d/%m/%Y"), ponderacion from zona where idcurso = {idclase}'
				cursor.execute(consulta)
				tareas = cursor.fetchall()
				consulta = f'select IF("{hoy}" < DATE_ADD(fechafin, INTERVAL 1 MONTH), 1, 0) from clase where idclase = {idclase}'
				print(consulta)
				cursor.execute(consulta)
				condicional = cursor.fetchone()
				condicional = condicional[0]
		finally:
			conexion.close()
	except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
		print("Ocurrió un error al conectar: ", e)
	return render_template('vertareas.html', title="Tareas del Curso", tareas = tareas, idclase = idclase, condicional = condicional)

#Catedratico
@app.route('/nuevatarea/<idclase>', methods=['GET', 'POST'])
def nuevatarea(idclase):
	if 'usuario' in session and session['tipouser'] == 2:
		pass
	else:
		return redirect(url_for('home'))
	hoy = date.today()
	tarea = ["", ""]
	if request.method == 'POST':
		concepto = request.form['concepto']
		ponderacion = request.form['ponderacion']
		try:
			conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
			try:
				with conexion.cursor() as cursor:
					consulta = "insert into zona(idcurso, concepto, ponderacion, fecha) values (%s,%s,%s,%s);"
					cursor.execute(consulta, (idclase, concepto, ponderacion, hoy))
					conexion.commit()
					consulta = "Select MAX(idzona) from zona;"
					cursor.execute(consulta)
					idtarea = cursor.fetchone()
					idtarea = idtarea[0]
					consulta = "Select idestudiante from claseestudiante where idclase = %s;"
					cursor.execute(consulta, idclase)
					estudiantes = cursor.fetchall()
					for i in estudiantes:
						consulta = "insert into zonaestudiante(idzona, idestudiante, nota) values (%s,%s,0);"
						cursor.execute(consulta, (idtarea, i[0]))
						conexion.commit()
			finally:
				conexion.close()
		except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
			print("Ocurrió un error al conectar: ", e)
		return redirect(url_for('vertareas', idclase = idclase))
	return render_template('nuevatarea.html', title="Nueva Tarea", idclase = idclase, nuevo = 1, tarea = tarea)

#Catedratico
@app.route('/editartarea/<idtarea>', methods=['GET', 'POST'])
def editartarea(idtarea):
	if 'usuario' in session and session['tipouser'] == 2:
		pass
	else:
		return redirect(url_for('home'))
	hoy = date.today()
	tarea = ["", "", ""]
	try:
		conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
		try:
			with conexion.cursor() as cursor:
				consulta = "SELECT concepto, ponderacion, idcurso FROM zona where idzona = %s"
				cursor.execute(consulta, idtarea)
				tarea = cursor.fetchone()
				idcurso = tarea[2]
				consulta = "select idcatedratico from clase where idclase = %s"
				cursor.execute(consulta, idcurso)
				idcatedratico = cursor.fetchone()
				idcatedratico = idcatedratico[0]
				consulta = "select idconexion from user where iduser = %s"
				cursor.execute(consulta, session['idusuario'])
				idconexion = cursor.fetchone()
				idconexion = idconexion[0]
				if idconexion != idcatedratico:
					return redirect(url_for('clasesactuales'))
		finally:
			conexion.close()
	except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
		print("Ocurrió un error al conectar: ", e)
	if request.method == 'POST':
		concepto = request.form['concepto']
		ponderacion = request.form['ponderacion']
		try:
			conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
			try:
				with conexion.cursor() as cursor:
					consulta = "update zona set concepto = %s, ponderacion = %s where idzona = %s;"
					cursor.execute(consulta, (concepto, ponderacion, idtarea))
					conexion.commit()
			finally:
				conexion.close()
		except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
			print("Ocurrió un error al conectar: ", e)
		return redirect(url_for('vertareas', idclase = tarea[2]))
	return render_template('nuevatarea.html', title="Nueva Tarea", nuevo = 0, tarea = tarea)

#Catedratico
@app.route('/calificartarea/<idtarea>', methods=['GET', 'POST'])
def calificartarea(idtarea):
	if 'usuario' in session and session['tipouser'] == 2:
		pass
	else:
		return redirect(url_for('home'))
	hoy = date.today()
	try:
		conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
		try:
			with conexion.cursor() as cursor:
				consulta = "SELECT concepto, ponderacion, idcurso FROM zona where idzona = %s"
				cursor.execute(consulta, idtarea)
				tarea = cursor.fetchone()
				idclase = tarea[2]
				consulta = "select idcatedratico from clase where idclase = %s"
				cursor.execute(consulta, idclase)
				idcatedratico = cursor.fetchone()
				idcatedratico = idcatedratico[0]
				consulta = "select idconexion from user where iduser = %s"
				cursor.execute(consulta, session['idusuario'])
				idconexion = cursor.fetchone()
				idconexion = idconexion[0]
				if idconexion != idcatedratico:
					return redirect(url_for('clasesactuales'))
				consulta = f"SELECT c.nombre, CONCAT(d.nombre1,' ',d.nombre2,' ',d.apellido1,' ',d.apellido2,' ',d.apellido3) from clase l inner join curso c on c.idcurso = l.idcurso inner join catedratico d on d.idcatedratico = l.idcatedratico where l.idclase = {idclase} order by c.nombre asc"
				cursor.execute(consulta)
				dataclase = cursor.fetchone()
				consulta = f"select e.idestudiante, e.nombre1, e.nombre2, e.apellido1, e.apellido2, e.apellido3, e.carnet from estudiante e inner join claseestudiante ce on ce.idestudiante = e.idestudiante where ce.idclase = {idclase} and ce.idestado = 1 order by e.nombre1, e.nombre2, e.apellido1, e.apellido2, e.apellido3"
				cursor.execute(consulta)
				estudiantes = cursor.fetchall()
				notas = []
				for i in estudiantes:
					consulta = f"Select nota from zonaestudiante where idzona = {idtarea} and idestudiante = {i[0]}"
					cursor.execute(consulta)
					nota = cursor.fetchone()
					nota = nota[0]
					notas.append(nota)
		finally:
			conexion.close()
	except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
		print("Ocurrió un error al conectar: ", e)
	if request.method == 'POST':
		try:
			conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
			try:
				with conexion.cursor() as cursor:
					for i in estudiantes:
						aux = f"calificacion{i[0]}"
						nota = request.form[aux]
						consulta = "update zonaestudiante set nota = %s where idzona = %s and idestudiante = %s;"
						cursor.execute(consulta, (nota, idtarea, i[0]))
					conexion.commit()
			finally:
				conexion.close()
		except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
			print("Ocurrió un error al conectar: ", e)
		return redirect(url_for('vertareas', idclase = tarea[2]))
	return render_template('calificartarea.html', title="Calificar Tarea", tarea = tarea, dataclase = dataclase, estudiantes = estudiantes, notas = notas)

#Catedratico
@app.route('/eliminartarea/<idtarea>', methods=['GET', 'POST'])
def eliminartarea(idtarea):
	if 'usuario' in session and session['tipouser'] == 2:
		pass
	else:
		return redirect(url_for('home'))
	try:
		conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
		try:
			with conexion.cursor() as cursor:
				consulta = "select idcurso from zona where idzona = %s"
				cursor.execute(consulta, idtarea)
				tarea = cursor.fetchone()
				idclase = tarea[0]
				consulta = "select idcatedratico from clase where idclase = %s"
				cursor.execute(consulta, idclase)
				idcatedratico = cursor.fetchone()
				idcatedratico = idcatedratico[0]
				consulta = "select idconexion from user where iduser = %s"
				cursor.execute(consulta, session['idusuario'])
				idconexion = cursor.fetchone()
				idconexion = idconexion[0]
				if idconexion != idcatedratico:
					return redirect(url_for('clasesactuales'))
				consulta = "delete FROM zona where idzona = %s"
				cursor.execute(consulta, idtarea)
				consulta = "delete FROM zonaestudiante where idzona = %s"
				cursor.execute(consulta, idtarea)
				conexion.commit()
		finally:
			conexion.close()
	except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
		print("Ocurrió un error al conectar: ", e)
	return redirect(url_for('vertareas', idclase = idclase))

#Catedratico
@app.route('/clasesactuales', methods=['GET', 'POST'])
def clasesactuales():
	if 'usuario' in session and session['tipouser'] == 2:
		pass
	else:
		return redirect(url_for('logincatedratico'))
	hoy = date.today()
	try:
		conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
		try:
			with conexion.cursor() as cursor:
				consulta = "select idconexion from user where iduser = %s"
				cursor.execute(consulta, session["idusuario"])
				idcatedratico = cursor.fetchone()
				idcatedratico = idcatedratico[0]
				consulta = f"SELECT c.nombre, CONCAT(d.nombre1,' ',d.nombre2,' ',d.apellido1,' ',d.apellido2,' ',d.apellido3), p.plan, DATE_FORMAT(l.fechainicio,'%d/%m/%Y'), DATE_FORMAT(l.fechafin,'%d/%m/%Y'), l.idclase from clase l inner join plan p on p.idplan = l.idplan inner join curso c on c.idcurso = l.idcurso inner join catedratico d on d.idcatedratico = l.idcatedratico where l.fechafin >= '{hoy}' and l.idcatedratico = {idcatedratico} order by c.nombre asc"
				cursor.execute(consulta)
				clases = cursor.fetchall()
		finally:
			conexion.close()
	except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
		print("Ocurrió un error al conectar: ", e)
	return render_template('clasesactuales.html', title="Clases Actuales", clases = clases)

#Catedratico
@app.route('/claseshistorico', methods=['GET', 'POST'])
def claseshistorico():
	if 'usuario' in session and session['tipouser'] == 2:
		pass
	else:
		return redirect(url_for('logincatedratico'))
	hoy = date.today()
	try:
		conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
		try:
			with conexion.cursor() as cursor:
				consulta = "select idconexion from user where iduser = %s"
				cursor.execute(consulta, session["idusuario"])
				idcatedratico = cursor.fetchone()
				idcatedratico = idcatedratico[0]
				consulta = f"SELECT c.nombre, CONCAT(d.nombre1,' ',d.nombre2,' ',d.apellido1,' ',d.apellido2,' ',d.apellido3), p.plan, DATE_FORMAT(l.fechainicio,'%d/%m/%Y'), DATE_FORMAT(l.fechafin,'%d/%m/%Y'), l.idclase from clase l inner join plan p on p.idplan = l.idplan inner join curso c on c.idcurso = l.idcurso inner join catedratico d on d.idcatedratico = l.idcatedratico where l.fechafin < '{hoy}' and l.idcatedratico = {idcatedratico} order by c.nombre asc"
				cursor.execute(consulta)
				clases = cursor.fetchall()
		finally:
			conexion.close()
	except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
		print("Ocurrió un error al conectar: ", e)
	return render_template('claseshistorico.html', title="Historico", clases = clases)

#General
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    session.pop('idusuario', None)
    session.pop('nombre', None)
    session.pop('tipouser', None)
    return redirect(url_for('home'))

#Administrativo
@app.route('/crearusuario', methods=['GET', 'POST'])
def crearusuario():
	if 'usuario' in session and session['tipouser'] == 1:
		pass
	else:
		return redirect(url_for('loginadmin'))
	if request.method == 'POST':
		usuario = request.form['usuario']
		password = request.form['password']
		nombre1 = request.form['nombre1']
		nombre2 = request.form['nombre2']
		apellido1 = request.form['apellido1']
		apellido2 = request.form['apellido2']
		apellido3 = request.form['apellido3']
		telefono = request.form['telefono']
		celular = request.form['celular']
		correo = request.form['correo']
		genero = request.form['genero']
		fechanacimiento = request.form['fechanacimiento']
		try:
			conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
			try:
				with conexion.cursor() as cursor:
					consulta = "insert into administrativo(nombre1, nombre2, apellido1, apellido2, apellido3, telefono, celular, correo, idgenero, fechanacimiento) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
					cursor.execute(consulta, (nombre1, nombre2, apellido1, apellido2, apellido3, telefono, celular, correo, genero, fechanacimiento))
					conexion.commit()
					consulta = 'select max(idadministrativo) from administrativo'
					cursor.execute(consulta)
					idadministrativo = cursor.fetchone()
					consulta = "insert into user(usuario, clave, idtipousuario, idconexion) values (%s,%s,%s,%s);"
					cursor.execute(consulta, (usuario, generate_password_hash(password), 1, idadministrativo))
					conexion.commit()
			finally:
				conexion.close()
		except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
			print("Ocurrió un error al conectar: ", e)
		return redirect(url_for('admin'))
	return render_template('crearusuario.html', title="Crear Usuario")

#Catedratico y Estudiante
@app.route('/cambioclave', methods=['GET', 'POST'])
def cambioclave():
	if 'usuario' in session:
		pass
	else:
		return redirect(url_for('home'))
	if request.method == 'POST':
		password = request.form['password']
		try:
			conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
			try:
				with conexion.cursor() as cursor:
					consulta = "update user set clave = %s, logedin = 1 where iduser = %s"
					cursor.execute(consulta, (generate_password_hash(password), session['idusuario']))
					conexion.commit()
			finally:
				conexion.close()
		except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
			print("Ocurrió un error al conectar: ", e)
		return redirect(url_for('catedraticos'))
	return render_template('cambioclave.html', title="Actualización de contraseña")

#Administrativo
@app.route('/loginadmin', methods=['GET', 'POST'])
def loginadmin():
	try:
		print(session['tipouser'])
	except:
		session['tipouser'] = 0
	if session['tipouser'] == 1:
		return redirect(url_for('admin'))
	elif session['tipouser'] == 2:
		return redirect(url_for('catedraticos'))
	elif session['tipouser'] == 3:
		return redirect(url_for('estudiantes'))
	else:
		pass
	if request.method == 'POST':
		usuario = request.form['usuario']
		password = request.form['clave']
		print(usuario, password)
		try:
			conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
			try:
				with conexion.cursor() as cursor:
					consulta = "SELECT usuario, clave, idconexion, iduser FROM user WHERE usuario = %s and idtipousuario = 1"
					cursor.execute(consulta, (usuario))
					user = cursor.fetchone()
					if user and check_password_hash(user[1], password):
						consulta = "SELECT nombre1, nombre2, apellido1, apellido2, apellido3 FROM administrativo WHERE idadministrativo = %s"
						cursor.execute(consulta, (user[2]))
						data = cursor.fetchone()
						session['usuario'] = usuario
						session['idusuario'] = user[3]
						nombre = f"{data[0]} {data[1]} {data[2]} {data[3]} {data[4]}"
						session['nombre'] =  nombre
						session['tipouser'] = 1
						flash('Inicio de sesión exitoso')
						return redirect(url_for('admin'))
					else:
						flash('Credenciales Invalidas, intente nuevamente', 'error')
			finally:
				conexion.close()
		except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
			print("Ocurrió un error al conectar: ", e)
		return redirect(url_for('admin'))
	return render_template('login.html', title="Inicio de Sesión", tipo = 1)

#Catedratico
@app.route('/logincatedratico', methods=['GET', 'POST'])
def logincatedratico():
	try:
		print(session['tipouser'])
	except:
		session['tipouser'] = 0
	if session['tipouser'] == 1:
		return redirect(url_for('admin'))
	elif session['tipouser'] == 2:
		return redirect(url_for('catedraticos'))
	elif session['tipouser'] == 3:
		return redirect(url_for('estudiantes'))
	else:
		pass
	if request.method == 'POST':
		usuario = request.form['usuario']
		password = request.form['clave']
		try:
			conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
			try:
				with conexion.cursor() as cursor:
					consulta = "SELECT usuario, clave, idconexion, logedin, iduser FROM user WHERE usuario = %s and idtipousuario = 2"
					cursor.execute(consulta, (usuario))
					user = cursor.fetchone()
					if user and check_password_hash(user[1], password):
						consulta = "SELECT nombre1, nombre2, apellido1, apellido2, apellido3 FROM catedratico WHERE idcatedratico = %s"
						cursor.execute(consulta, (user[2]))
						data = cursor.fetchone()
						session['usuario'] = usuario
						session['idusuario'] = user[4]
						nombre = f"{data[0]} {data[1]} {data[2]} {data[3]} {data[4]}"
						session['tipouser'] = 2
						session['nombre'] =  nombre
						flash('Inicio de sesión exitoso')
						if user[3] == 0:
							return redirect(url_for('cambioclave'))
						else:
							return redirect(url_for('catedraticos'))
					else:
						flash('Credenciales Invalidas, intente nuevamente', 'error')
			finally:
				conexion.close()
		except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
			print("Ocurrió un error al conectar: ", e)
		return redirect(url_for('catedraticos'))
	return render_template('login.html', title="Inicio de Sesión", tipo = 2)

#Estudiantes
@app.route('/loginestudiante', methods=['GET', 'POST'])
def loginestudiante():
	try:
		print(session['tipouser'])
	except:
		session['tipouser'] = 0
	if session['tipouser'] == 1:
		return redirect(url_for('admin'))
	elif session['tipouser'] == 2:
		return redirect(url_for('catedraticos'))
	elif session['tipouser'] == 3:
		return redirect(url_for('estudiantes'))
	else:
		pass
	print(generate_password_hash("14052000"))
	if request.method == 'POST':
		usuario = request.form['usuario']
		password = request.form['clave']
		try:
			conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
			try:
				with conexion.cursor() as cursor:
					consulta = "SELECT usuario, clave, idconexion, logedin, iduser FROM user WHERE usuario = %s and idtipousuario = 3"
					cursor.execute(consulta, (usuario))
					user = cursor.fetchone()
					if user and check_password_hash(user[1], password):
						consulta = "SELECT nombre1, nombre2, apellido1, apellido2, apellido3 FROM estudiante WHERE idestudiante = %s"
						cursor.execute(consulta, (user[2]))
						data = cursor.fetchone()
						session['usuario'] = usuario
						session['idusuario'] = user[4]
						nombre = f"{data[0]} {data[1]} {data[2]} {data[3]} {data[4]}"
						session['tipouser'] = 3
						session['nombre'] =  nombre
						flash('Inicio de sesión exitoso')
						if user[3] == 0:
							return redirect(url_for('cambioclave'))
						else:
							return redirect(url_for('estudiantes'))
					else:
						flash('Credenciales Invalidas, intente nuevamente', 'error')
			finally:
				conexion.close()
		except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
			print("Ocurrió un error al conectar: ", e)
		return redirect(url_for('estudiantes'))
	return render_template('login.html', title="Inicio de Sesión", tipo = 3)

@app.route('/guardarcongreso/<nombre>&<carnet>&<descripcion>&<idpago>', methods=['GET', 'POST'])
def guardarcongreso(nombre, carnet, descripcion, idpago):
	try:
		conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
		try:
			with conexion.cursor() as cursor:
				consulta = "insert into congreso(nombre, carnet, descripcion, idpago, fecha) values (%s, %s, %s, %s, CURDATE());"
				cursor.execute(consulta, (nombre, carnet, descripcion, idpago))
				conexion.commit()
		finally:
			conexion.close()
	except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
		print("Ocurrió un error al conectar: ", e)
	return redirect(url_for('estudiantes'))

@app.route('/verentradascongreso', methods=['GET', 'POST'])
def verentradascongreso():
	if 'usuario' in session and session['tipouser'] == 1:
		pass
	else:
		return redirect(url_for('loginadmin'))
	try:
		conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
		try:
			with conexion.cursor() as cursor:
				consulta = "select nombre, carnet, descripcion, fecha, idpago, ingreso from congreso where year(fecha) = year(CURDATE());"
				cursor.execute(consulta)
				pagoscongreso = cursor.fetchall()
		finally:
			conexion.close()
	except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
		print("Ocurrió un error al conectar: ", e)
	return render_template('verentradascongreso.html', title="Pagos de Congreso", pagoscongreso=pagoscongreso)

@app.route('/registrarentradacongreso', methods=['GET', 'POST'])
def registrarentradacongreso():
	if 'usuario' in session and session['tipouser'] == 1:
		pass
	else:
		return redirect(url_for('loginadmin'))
	mensaje = ""
	color = "red"
	if request.method == 'POST':
		codigo = request.form["codigo"]
		codigo = int(codigo)
		try:
			conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
			try:
				with conexion.cursor() as cursor:
					consulta = "select ingreso from congreso where idpago = %s and ingreso = '0';"
					cursor.execute(consulta, codigo)
					entradas0 = cursor.fetchall()
					consulta = "select ingreso from congreso where idpago = %s and ingreso != '0';"
					cursor.execute(consulta, codigo)
					entradas1 = cursor.fetchall()
					if len(entradas0) == 0:
						if len(entradas1) == 0:
							mensaje = "El código no es válido"
						else:
							ingreso = entradas1[0][0]
							mensaje = f"El usuario ya ingresó: {ingreso}"
					else:
						text = f"%d/%m/%Y %H:%M"
						horaactual = datetime.now().strftime(text)
						consulta = "update congreso set ingreso = %s where idpago = %s"
						cursor.execute(consulta, (horaactual, codigo))
						mensaje = "La entrada se ha registrado correctamente"
						color = "green"
						conexion.commit()
			finally:
				conexion.close()
		except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
			print("Ocurrió un error al conectar: ", e)
	return render_template('registrarentradacongreso.html', title="Entrada a Congreso", mensaje = mensaje, color=color)

@app.route('/congreso', methods=['GET', 'POST'])
def congreso():
	if 'usuario' in session and session['tipouser'] == 1:
		pass
	else:
		return redirect(url_for('loginadmin'))
	try:
		conexion = pymysql.connect(host=Conhost, user=Conuser, password=Conpassword, db=Condb)
		try:
			with conexion.cursor() as cursor:
				consulta = "SELECT c.nombre, i.nombre, c.idcurso, c.abreviatura from curso c inner join institucion i on i.idinstitucion = c.idinstitucion order by c.nombre asc"
				cursor.execute(consulta)
				cursos = cursor.fetchall()
		finally:
			conexion.close()
	except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
		print("Ocurrió un error al conectar: ", e)
	return render_template('congreso.html', title="Congreso")

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5005, threaded=True, debug=True)