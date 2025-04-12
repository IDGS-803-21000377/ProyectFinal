from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# -------------------- Autenticación --------------------
class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False) 
    address = db.Column(db.String(255), nullable=True) 
    phone_number = db.Column(db.String(20), nullable=True) 
    last_login = db.Column(db.DateTime, nullable=True)

    role = db.Column(db.String(20), nullable=False, default="user") 

    pedidos = db.relationship('Pedido', backref='usuario', lazy=True)

    def get_id(self):
        return str(self.id_user)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

# -------------------- Proveedor --------------------
class Proveedor(db.Model):
    __tablename__ = 'proveedores'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(255), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)

    materias_primas = db.relationship('MateriaPrima', back_populates='proveedor')
    solicitudes = db.relationship('SolicitudMaterial', back_populates='proveedor', cascade="all, delete-orphan")

# -------------------- Materia Prima --------------------
class MateriaPrima(db.Model):
    __tablename__ = 'materias_primas'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cantidad_disponible = db.Column(db.Float, nullable=False, default=0.0)
    unidad = db.Column(db.String(20), default="g")
    precio_por_unidad = db.Column(db.Float, nullable=False, default=0.0)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'), nullable=False)

    proveedor = db.relationship('Proveedor', back_populates='materias_primas')
    receta_ingredientes = db.relationship('RecetaIngrediente', back_populates='materia_prima')

# -------------------- Receta --------------------
class Receta(db.Model):
    __tablename__ = 'recetas'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    imagen = db.Column(db.String(100), nullable=True)
    
    receta_ingredientes = db.relationship(
        'RecetaIngrediente', 
        back_populates='receta', 
        cascade='all, delete-orphan',
        lazy='select'
    )

    productos = db.relationship(
        'ProductoTerminado', 
        back_populates='receta',
        lazy='dynamic'
    )

# -------------------- Receta Ingrediente --------------------
class RecetaIngrediente(db.Model):
    __tablename__ = 'recetas_ingredientes'
    
    id = db.Column(db.Integer, primary_key=True)
    receta_id = db.Column(db.Integer, db.ForeignKey('recetas.id'), nullable=False)
    materia_prima_id = db.Column(db.Integer, db.ForeignKey('materias_primas.id'), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)

    receta = db.relationship('Receta', back_populates='receta_ingredientes')
    materia_prima = db.relationship('MateriaPrima', back_populates='receta_ingredientes')

# -------------------- Producto Terminado --------------------
class ProductoTerminado(db.Model):
    __tablename__ = 'productos_terminados'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)
    cantidad = db.Column(db.Float, nullable=False, default=0)
    fecha_produccion = db.Column(db.DateTime, default=datetime.utcnow)
    receta_id = db.Column(db.Integer, db.ForeignKey('recetas.id'), nullable=False)

    receta = db.relationship('Receta', back_populates='productos')

# -------------------- Pedido --------------------
class Pedido(db.Model):
    __tablename__ = 'pedido'
    
    idPedido = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable=False)
    fecha_recoleccion = db.Column(db.Date, nullable=False)
    fecha = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    estatus = db.Column(db.String(10), nullable=False, default="pendiente")

    detalles = db.relationship('DetallePedido', backref='pedido', lazy=True, cascade="all, delete-orphan")

# -------------------- Detalle Pedido --------------------
class DetallePedido(db.Model):
    __tablename__ = 'detalle_pedido'

    idDetalle = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idPedido = db.Column(db.Integer, db.ForeignKey('pedido.idPedido'), nullable=False)
    idProductoTerminado = db.Column(db.Integer, db.ForeignKey('productos_terminados.id'), nullable=False)  
    presentacion = db.Column(db.String(150), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    producto_terminado = db.relationship("ProductoTerminado", backref="detalles")

# -------------------- Venta --------------------
class Venta(db.Model):
    __tablename__ = 'venta'
    
    idVenta = db.Column(db.Integer, primary_key=True)

    id_cliente = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable=True)
    id_vendedor = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable=False)

    idPedido = db.Column(db.Integer, db.ForeignKey('pedido.idPedido'), nullable=True)
    fechaVenta = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    precio = db.Column(db.Float, nullable=False)

    detalles = db.relationship('DetalleVenta', backref='venta', lazy=True)

# -------------------- Detalle Venta --------------------
class DetalleVenta(db.Model):
    __tablename__ = 'detalleVenta'
    
    idDetalleVenta = db.Column(db.Integer, primary_key=True)
    idVenta = db.Column(db.Integer, db.ForeignKey('venta.idVenta'), nullable=False)
    idProductoTerminado = db.Column(db.Integer, db.ForeignKey('productos_terminados.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    presentacion = db.Column(db.String(50), nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    producto_terminado = db.relationship("ProductoTerminado", backref="detalles_venta")

# -------------------- Error Logs --------------------
class ErrorLog(db.Model):
    __tablename__ = 'error_logs'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255))
    message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# -------------------- Solicitud de Material --------------------

class SolicitudMaterial(db.Model):
    __tablename__ = 'solicitudes_materiales'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    unidad = db.Column(db.String(20), nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False, default=0.0)  # ✅ NUEVO CAMPO
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'), nullable=False)

    proveedor = db.relationship('Proveedor', back_populates='solicitudes')


