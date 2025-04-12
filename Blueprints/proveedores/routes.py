from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from models import db, Proveedor
from forms import ProveedorForm

proveedores_bp = Blueprint('proveedores', __name__, url_prefix='/proveedores')

# -------------------- LISTAR PROVEEDORES --------------------
@proveedores_bp.route('/')
@login_required
def listar_proveedores():
    if current_user.role != 'empleado':
        flash("Acceso no autorizado", "proveedor_error")
        return redirect(url_for('auth.login'))

    proveedores = Proveedor.query.all()
    return render_template('proveedor/proveedores.html', proveedores=proveedores)

# -------------------- CREAR PROVEEDOR --------------------
@proveedores_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear_proveedor():
    if current_user.role != 'empleado':
        flash("Acceso no autorizado", "proveedor_error")
        return redirect(url_for('auth.login'))

    form = ProveedorForm()
    if form.validate_on_submit():
        nuevo_proveedor = Proveedor(
            nombre=form.nombre.data,
            direccion=form.direccion.data,
            telefono=form.telefono.data,
            email=form.email.data
        )
        try:
            db.session.add(nuevo_proveedor)
            db.session.commit()
            flash('Proveedor creado exitosamente.', 'proveedor_success')
            return redirect(url_for('proveedores.listar_proveedores'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error al crear proveedor: {e}")
            flash('Error al crear el proveedor.', 'proveedor_error')

    return render_template('proveedor/crear.html', form=form)

# -------------------- EDITAR PROVEEDOR --------------------
@proveedores_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_proveedor(id):
    if current_user.role != 'empleado':
        flash("Acceso no autorizado", "proveedor_error")
        return redirect(url_for('auth.login'))

    proveedor = Proveedor.query.get_or_404(id)
    form = ProveedorForm(obj=proveedor)

    if form.validate_on_submit():
        try:
            form.populate_obj(proveedor)
            db.session.commit()
            flash('Proveedor actualizado exitosamente.', 'proveedor_success')
            return redirect(url_for('proveedores.listar_proveedores'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error al actualizar proveedor: {e}")
            flash('Error al actualizar el proveedor.', 'proveedor_error')

    return render_template('proveedor/editar.html', form=form, proveedor=proveedor)

# -------------------- ELIMINAR PROVEEDOR --------------------
@proveedores_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_proveedor(id):
    if current_user.role != 'empleado':
        flash("Acceso no autorizado", "proveedor_error")
        return redirect(url_for('auth.login'))

    proveedor = Proveedor.query.get_or_404(id)
    try:
        db.session.delete(proveedor)
        db.session.commit()
        flash('Proveedor eliminado exitosamente.', 'proveedor_success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al eliminar proveedor: {e}")
        flash('Error al eliminar el proveedor.', 'proveedor_error')

    return redirect(url_for('proveedores.listar_proveedores'))
