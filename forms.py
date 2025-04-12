from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, SelectField, FloatField, SubmitField,
    FieldList, FormField, IntegerField, PasswordField, DateField
)
from wtforms.validators import DataRequired, Optional, Length, Regexp, Email, NumberRange, ValidationError
from flask_wtf.file import FileField, FileAllowed
from flask_wtf.recaptcha import RecaptchaField


def not_common_password(form, field):
    password = field.data.strip().lower()
    with open("static/data/common_passwords.txt", "r", encoding="utf-8") as f:
        comunes = set(p.strip().lower() for p in f.readlines())
        if password in comunes:
            raise ValidationError("Esa contraseña es demasiado común. Por favor elige otra.")


class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Iniciar sesión')


class RegistroUsuarioForm(FlaskForm):
    username = StringField("Usuario", validators=[
        DataRequired(message="El nombre de usuario es requerido"),
        Length(min=3, max=80, message="El usuario debe tener entre 3 y 80 caracteres")
    ])

    email = StringField("Correo Electrónico", validators=[
        DataRequired(message="El correo electrónico es requerido"),
        Email(message="Correo inválido")
    ])

    password = PasswordField("Contraseña", validators=[
        DataRequired(),
        Length(min=8, message="Debe tener al menos 8 caracteres"),
        Regexp(r'(?=.*[A-Z])', message="Debe contener una mayúscula"),
        not_common_password
    ])

    name = StringField("Nombre", validators=[DataRequired(message="El nombre es requerido")])
    last_name = StringField("Apellido", validators=[DataRequired(message="El apellido es requerido")])
    address = StringField("Dirección", validators=[Optional()])
    phone_number = StringField("Teléfono", validators=[
        Optional(),
        Regexp(r'^\d{10}$', message="Debe ser un número de 10 dígitos")
    ])

    role = SelectField("Rol", choices=[
        ('empleado', 'Empleado'),
        ('cliente', 'Cliente'),
    ], validators=[DataRequired()])

    submit = SubmitField("Guardar Usuario")


class IngredienteForm(FlaskForm):
    materia_prima_id = SelectField(
        'Ingrediente',
        coerce=int,
        validators=[DataRequired()],
        choices=[]
    )
    cantidad = FloatField(
        'Cantidad',
        validators=[DataRequired(), NumberRange(min=0.01)]
    )


class RecetaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción', validators=[DataRequired()])


class GalletaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    descripcion = StringField('Descripción', validators=[Optional()])
    existencias = IntegerField('Existencias', validators=[
        DataRequired(),
        NumberRange(min=0, message="Las existencias no pueden ser negativas")
    ])
    precio = FloatField('Precio', validators=[
        DataRequired(),
        NumberRange(min=0, message="El precio no puede ser negativo")
    ])
    gramaje = StringField('Gramaje', validators=[Optional()])
    vidaAnaquel = DateField('Vida Anaquel', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Agregar Galleta')


class MaterialForm(FlaskForm):
    nombreProducto = StringField('Nombre del Producto', validators=[DataRequired()])
    cantidad_disponible = FloatField('Cantidad Disponible', validators=[
        DataRequired(),
        NumberRange(min=0, message="La cantidad no puede ser negativa")
    ])
    precio_por_unidad = FloatField('Precio por Unidad', validators=[
        DataRequired(),
        NumberRange(min=0, message="El precio no puede ser negativo")
    ])
    unidad = SelectField('Unidad de Medida', choices=[
        ('kg', 'Kilogramos'),
        ('g', 'Gramos'),
        ('ml', 'Mililitros'),
        ('pieza', 'Piezas')
    ], validators=[DataRequired()])
    proveedor_id = SelectField('Proveedor', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Guardar')


class ProduccionForm(FlaskForm):
    receta_id = SelectField('Selecciona una Receta', coerce=int, validators=[DataRequired()])
    cantidad = IntegerField('Cantidad de Lotes', validators=[
        DataRequired(),
        NumberRange(min=1, message="Debe producir al menos 1 lote")
    ])
    submit = SubmitField('Producir')


class ProveedorForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    direccion = StringField('Dirección')
    telefono = StringField('Teléfono')
    email = StringField('Email', validators=[Optional(), Email()])
    submit = SubmitField('Guardar')


class MaterialProveedorForm(FlaskForm):
    nombre = StringField('Nombre del Material', validators=[DataRequired()])
    cantidad_disponible = FloatField('Cantidad Disponible', validators=[
        DataRequired(),
        NumberRange(min=0, message="La cantidad no puede ser negativa")
    ])
    unidad = SelectField('Unidad', choices=[
        ('g', 'Gramos'),
        ('kg', 'Kilogramos'),
        ('ml', 'Mililitros'),
        ('l', 'Litros'),
        ('unidad', 'Unidades')
    ], validators=[DataRequired()])
    precio_por_unidad = FloatField('Precio por Unidad', validators=[
        DataRequired(),
        NumberRange(min=0, message="El precio no puede ser negativo")
    ])
    submit = SubmitField('Agregar Material')


class PedidoForm(FlaskForm):
    galleta = StringField('Galleta', validators=[DataRequired()])
    presentacion = StringField('Presentación', validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired(), NumberRange(min=1, message="Debe ser al menos 1")])
    fecha_recoleccion = DateField('Fecha de Recolección', validators=[DataRequired()])
    submit = SubmitField('Agregar Pedido')


class ProductoTerminadoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción')
    cantidad = FloatField('Cantidad (kg)', validators=[DataRequired()])
    receta_id = SelectField('Receta', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Guardar')


class RecetaImagenForm(FlaskForm):
    imagen = FileField('Imagen del producto', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Solo se permiten imágenes JPG, JPEG o PNG.'),
        DataRequired(message="Debes subir una imagen.")
    ])

class MaterialForm(FlaskForm):
    nombreProducto = StringField("Nombre del Producto", validators=[DataRequired(), Length(max=100)])
    cantidad_disponible = FloatField("Cantidad", validators=[DataRequired(), NumberRange(min=0)])
    unidad = SelectField('Unidad de Medida', choices=[
        ('kg', 'Kilogramos'),
        ('Lt', 'Litros'),
        ('Pieza', 'Piezas')
    ], validators=[DataRequired()])
    proveedor_id = SelectField("Proveedor", coerce=int, validators=[DataRequired()])
    precio_por_unidad = FloatField("Precio por unidad", validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Enviar Solicitud')

class CodigoVerificacionForm(FlaskForm):
    codigo = StringField('Código', validators=[DataRequired()])