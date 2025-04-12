from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, DateField, SubmitField
from wtforms.validators import DataRequired, Optional

from forms import GalletaForm, ProductoTerminadoForm
from models import ProductoTerminado, Receta, db


inventario_bp = Blueprint('inventario', __name__, url_prefix='/inventario')

@inventario_bp.route('/productos')
def listar_productos():
    if current_user.role != 'empleado':
        flash("Acceso no autorizado", "error")
        return redirect(url_for('auth.login'))
    
    productos = ProductoTerminado.query.all()
    return render_template('inventario/listar.html', productos=productos)

@inventario_bp.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):

    if current_user.role != 'empleado':
        flash("Acceso no autorizado", "error")
        return redirect(url_for('auth.login'))
    
    producto = ProductoTerminado.query.get_or_404(id)
    form = ProductoTerminadoForm(obj=producto)
    form.receta_id.choices = [(r.id, r.nombre) for r in Receta.query.all()]

    if form.validate_on_submit():
        producto.nombre = form.nombre.data
        producto.descripcion = form.descripcion.data
        producto.cantidad = form.cantidad.data
        producto.receta_id = form.receta_id.data
        db.session.commit()
        flash('Producto actualizado con éxito.')
        return redirect(url_for('inventario.listar_productos'))
    
    return render_template('inventario/editar.html', form=form, action='Editar')

@inventario_bp.route('/productos/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):

    if current_user.role != 'empleado':
        flash("Acceso no autorizado", "error")
        return redirect(url_for('auth.login'))
    
    producto = ProductoTerminado.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado con éxito.')
    return redirect(url_for('inventario.listar_productos'))