from flask import Flask, flash, logging, render_template, redirect, url_for
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf import CSRFProtect
from config import DevelopmentConfig
from models import db, User
from Blueprints.auth.routes import auth_bp
from Blueprints.recetas.routes import recetas_bp
from Blueprints.inventarioMat.routes import inventarioMaterbp
from Blueprints.Inventario.routes import inventario_bp
from Blueprints.produccion.routes import produccion_bp
from Blueprints.proveedores.routes import proveedores_bp
from Blueprints.pedidos.routes import pedidos_bp
from Blueprints.ventas.routes import ventas_bp
from Blueprints.dashboard.routes import dashboard_bp
from Blueprints.Inventario.routes import inventario_bp
from flask_migrate import Migrate

# ---------- Inicialización de la app ----------
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# ---------- Protección CSRF ----------
csrf = CSRFProtect(app)

# ---------- Base de datos ----------
db.init_app(app)
migrate = Migrate(app, db)
mail = Mail(app)

# ---------- Login ----------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = "Primero debes registrarte e iniciar sesión para acceder a esta página."
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    flash(login_manager.login_message, login_manager.login_message_category)
    return redirect(url_for(login_manager.login_view))

# ---------- Crear BD y usuario admin por defecto ----------
with app.app_context():
    db.create_all()
    
    user = User.query.filter_by(username="LuisGio51").first()
    if not user:
        user = User(
            username="LuisGio51",
            email="gourmetCookies@gmail.com",
            name="Luis",
            last_name="Claudio",
            address="Bernardo Cobos",
            phone_number="4778283293",
            role="empleado"
        )
        user.set_password("12345")
        db.session.add(user)
        db.session.commit()
        print("✔️ Base de datos y usuario 'LuisGio51' creados exitosamente.")

# ---------- Registrar Blueprints ----------
app.register_blueprint(auth_bp)
app.register_blueprint(recetas_bp)
app.register_blueprint(inventario_bp)
app.register_blueprint(inventarioMaterbp)
app.register_blueprint(produccion_bp, url_prefix='/produccion')
app.register_blueprint(proveedores_bp)
app.register_blueprint(pedidos_bp)
app.register_blueprint(ventas_bp)
app.register_blueprint(dashboard_bp)


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errores/errores.html", code=404, title="Página no encontrada", message="La página que buscas no existe o fue movida."), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template("errores/errores.html", code=500, title="Error interno del servidor", message="Ocurrió un error inesperado. Intenta más tarde."), 500

@app.errorhandler(403)
def forbidden_error(error):
    return render_template("errores/errores.html", code=403, title="Acceso denegado", message="No tienes permiso para acceder a esta página."), 403


# ---------- Iniciar servidor ----------
if __name__ == '__main__':
    app.run()
