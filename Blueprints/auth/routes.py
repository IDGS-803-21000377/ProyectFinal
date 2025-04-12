from datetime import datetime, timedelta
from functools import wraps
from flask import Blueprint, make_response, render_template, redirect, session, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import CodigoVerificacionForm, LoginForm, RegistroUsuarioForm
from models import User, db
from wtforms.validators import Optional
from flask_mail import Message
import random

auth_bp = Blueprint('auth', __name__, url_prefix='')

intentos_fallidos = {}

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    return no_cache

@auth_bp.route('/inicio')
@login_required
@nocache
def inicio():
    return render_template("index.html")

@auth_bp.route('/index')
@login_required
@nocache
def index():
    return render_template("index.html")

@auth_bp.route('/login', methods=['GET', 'POST'])
@nocache
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            user = User.query.filter_by(username=username).first()
            intento = intentos_fallidos.get(username, {'intentos': 0, 'bloqueado_hasta': None})

            if intento['bloqueado_hasta'] and intento['bloqueado_hasta'] > datetime.now():
                tiempo_restante = (intento['bloqueado_hasta'] - datetime.now()).seconds // 60 + 1
                flash(f"Cuenta bloqueada. Intenta de nuevo en {tiempo_restante} minutos.", "login_error")
                return render_template("login/login.html", form=form, login_message=True)

            if user and user.check_password(form.password.data):
                last_login_msg = user.last_login.strftime('%d/%m/%Y %H:%M:%S') if user.last_login else "Este es tu primer inicio de sesión"
                user.last_login = datetime.utcnow()
                db.session.commit()
                login_user(user)
                session['login_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                flash(f"Último inicio de sesión: {last_login_msg}", "login_success")
                intentos_fallidos.pop(username, None)

                if user.role == 'empleado':
                    return redirect(url_for('auth.index'))
                elif user.role == 'cliente':
                    return redirect(url_for('pedidos.save'))
            else:
                intento['intentos'] += 1
                if intento['intentos'] >= 3:
                    intento['bloqueado_hasta'] = datetime.now() + timedelta(minutes=1)
                    flash("Cuenta bloqueada por múltiples intentos fallidos. Intenta en 1 minuto.", "login_error")
                else:
                    restantes = 3 - intento['intentos']
                    flash(f"Usuario o contraseña incorrectos. Intentos restantes: {restantes}", "login_error")
                intentos_fallidos[username] = intento

    return render_template("login/login.html", form=form, login_message=True)

@auth_bp.route('/logout')
@login_required
@nocache
def logout():
    logout_user()
    session.clear()
    flash("Has cerrado sesión correctamente.", "info")
    return redirect(url_for('auth.login'))

@auth_bp.route('/usuarios')
@login_required
@nocache
def listar_usuarios():
    if current_user.role != 'empleado':
        flash("Acceso no autorizado", "error_usuarios")
        return redirect(url_for('auth.login'))
    usuarios = User.query.all()
    form = RegistroUsuarioForm()
    return render_template('login/listar_usuarios.html', usuarios=usuarios, form=form)

@auth_bp.route('/usuarios/crear', methods=['GET', 'POST'])
@login_required
@nocache
def crear_usuario():
    if current_user.role != 'empleado':
        flash("Acceso no autorizado", "error_usuarios")
        return redirect(url_for('auth.login'))

    form = RegistroUsuarioForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('El nombre de usuario ya está en uso', "usuario_error")
            return redirect(url_for('auth.crear_usuario'))

        nuevo_usuario = User(
            username=form.username.data,
            name=form.name.data,
            last_name=form.last_name.data,
            address=form.address.data,
            phone_number=form.phone_number.data,
            email=form.email.data,
            role=form.role.data
        )
        nuevo_usuario.set_password(form.password.data)

        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash("Usuario creado exitosamente", "usuario_success")
            return redirect(url_for('auth.listar_usuarios'))
        except Exception as e:
            db.session.rollback()
            flash("Error al crear el usuario", "usuario_error")
            current_app.logger.error(f"Error al crear usuario: {str(e)}")

    return render_template('login/registro.html', form=form)

@auth_bp.route('/registro-cliente', methods=['GET', 'POST'])
@nocache
def registro_cliente():
    form = RegistroUsuarioForm()

    if request.method == 'GET' and hasattr(form, 'role'):
        form.role.data = 'cliente'

    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("El correo electrónico ya está registrado.", "usuario_error_cliente")
            return redirect(url_for('auth.registro_cliente'))

        session['nuevo_usuario'] = {
            'username': form.username.data.strip(),
            'nombre': form.name.data.strip(),
            'apellido': form.last_name.data.strip(),
            'email': form.email.data.strip(),
            'password': form.password.data.strip(),
            'direccion': form.address.data.strip() if form.address.data else None,
            'telefono': form.phone_number.data.strip() if form.phone_number.data else None
        }

        codigo = str(random.randint(100000, 999999))
        session['codigo_verificacion'] = codigo

        mail = current_app.extensions['mail']
        msg = Message('Código de verificación - Galletas Gourmet', recipients=[session['nuevo_usuario']['email']])
        msg.body = f'Tu código de verificación es: {codigo}'
        mail.send(msg)

        return redirect(url_for('auth.verificacion'))

    return render_template('login/login_cliente.html', form=form, cliente_message=True)

@auth_bp.route("/verificacion", methods=['GET', 'POST'])
@nocache
def verificacion():
    form = CodigoVerificacionForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            codigo_ingresado = form.codigo.data
            if codigo_ingresado == session.get('codigo_verificacion'):
                datos = session.get('nuevo_usuario')
                if datos:
                    nuevo = User(
                        username=datos['username'],
                        name=datos['nombre'],
                        last_name=datos['apellido'],
                        email=datos['email'],
                        address=datos['direccion'],
                        phone_number=datos['telefono'],
                        role='cliente'
                    )
                    nuevo.set_password(datos['password'])
                    db.session.add(nuevo)
                    db.session.commit()
                    session.pop('nuevo_usuario')
                    session.pop('codigo_verificacion')
                    flash("Cuenta creada exitosamente. Ahora puedes iniciar sesión.", "verificacion_success")
                    return redirect(url_for("auth.login"))
            else:
                flash("Código incorrecto, intenta nuevamente.", "verificacion_error")

    return render_template("login/verificar_codigo.html", form=form)

@auth_bp.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@nocache
def editar_usuario(id):
    if current_user.role != 'empleado':
        flash("Acceso no autorizado", "error_usuarios")
        return redirect(url_for('auth.login'))

    usuario = User.query.get_or_404(id)
    form = RegistroUsuarioForm(obj=usuario)
    form.password.validators = [Optional()]

    if form.validate_on_submit():
        usuario.username = form.username.data
        usuario.name = form.name.data
        usuario.last_name = form.last_name.data
        usuario.address = form.address.data
        usuario.phone_number = form.phone_number.data
        usuario.role = form.role.data
        usuario.email = form.email.data

        if form.password.data:
            usuario.set_password(form.password.data)

        db.session.commit()
        flash("Usuario actualizado correctamente", "success")
        return redirect(url_for('auth.listar_usuarios'))

    return render_template('login/editar.html', form=form, usuario=usuario)

@auth_bp.route('/usuarios/eliminar/<int:id>', methods=['POST'])
@login_required
@nocache
def eliminar_usuario(id):
    if current_user.role != 'empleado':
        flash("Acceso no autorizado", "error_usuarios")
        return redirect(url_for('auth.login'))

    usuario = User.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash("Usuario eliminado exitosamente", "success")
    return redirect(url_for('auth.listar_usuarios'))

@auth_bp.before_app_request
def check_session_timeout():
    if current_user.is_authenticated:
        if 'login_time' in session:
            login_time = datetime.strptime(session['login_time'], "%Y-%m-%d %H:%M:%S")
            time_diff = datetime.now() - login_time
            if time_diff > timedelta(minutes=20):
                logout_user()
                session.clear()
                flash("Sesión cerrada por inactividad", "info")
                return redirect(url_for('auth.login'))
        session['login_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
