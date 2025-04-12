from datetime import time
import threading
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import SolicitudMaterial, db, MateriaPrima, Proveedor
from forms import MaterialForm

inventarioMaterbp = Blueprint('materiales', __name__, url_prefix='/materiales')

@inventarioMaterbp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if current_user.role != 'empleado':
        flash("Acceso no autorizado", "material_error")
        return redirect(url_for('auth.login'))

    form = MaterialForm()
    form.proveedor_id.choices = [(p.id, p.nombre) for p in Proveedor.query.order_by(Proveedor.nombre).all()]

    if form.validate_on_submit():
        try:
            solicitud = SolicitudMaterial.query.filter_by(
                nombre=form.nombreProducto.data,
                unidad=form.unidad.data,
                proveedor_id=form.proveedor_id.data
            ).first()

            if solicitud:
                solicitud.cantidad += form.cantidad_disponible.data
                solicitud.precio_unitario = form.precio_por_unidad.data
                flash("Solicitud actualizada", "material_info")
            else:
                nueva_solicitud = SolicitudMaterial(
                    nombre=form.nombreProducto.data,
                    cantidad=form.cantidad_disponible.data,
                    unidad=form.unidad.data,
                    proveedor_id=form.proveedor_id.data,
                    precio_unitario=form.precio_por_unidad.data
                )
                db.session.add(nueva_solicitud)
                flash("Solicitud enviada al proveedor", "material_success")

            db.session.commit()
            return redirect(url_for('materiales.index'))

        except Exception as e:
            db.session.rollback()
            flash(f"Error al enviar la solicitud: {str(e)}", "material_error")

    materiales = db.session.query(
        MateriaPrima,
        Proveedor.nombre.label('nombre_proveedor')
    ).join(Proveedor).order_by(MateriaPrima.nombre).all()

    return render_template('inventarioMat/materiales.html', form=form, materiales=materiales)


@inventarioMaterbp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    if current_user.role != 'empleado':
        flash("Acceso no autorizado", "material_error")
        return redirect(url_for('auth.login'))

    material = MateriaPrima.query.get_or_404(id)
    form = MaterialForm(obj=material)
    form.proveedor_id.choices = [(p.id, p.nombre) for p in Proveedor.query.order_by(Proveedor.nombre).all()]

    if form.validate_on_submit():
        try:
            material.nombre = form.nombreProducto.data
            material.cantidad_disponible = form.cantidad_disponible.data
            material.unidad = form.unidad.data
            material.proveedor_id = form.proveedor_id.data
            material.precio_por_unidad = form.precio_por_unidad.data

            db.session.commit()
            flash('Material actualizado exitosamente', 'material_success')
            return redirect(url_for('materiales.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar material: {str(e)}', 'material_error')

    return render_template('inventarioMat/editar.html', form=form, material=material)


@inventarioMaterbp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    if current_user.role != 'empleado':
        flash("Acceso no autorizado", "material_error")
        return redirect(url_for('auth.login'))

    material = MateriaPrima.query.get_or_404(id)
    try:
        db.session.delete(material)
        db.session.commit()
        flash('Material eliminado exitosamente', 'material_success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar material: {str(e)}', 'material_error')
    return redirect(url_for('materiales.index'))


@inventarioMaterbp.route('/solicitudes', methods=['GET'])
@login_required
def ver_solicitudes():
    if current_user.role != 'empleado':
        flash("Acceso no autorizado", "material_error")
        return redirect(url_for('auth.login'))

    solicitudes = SolicitudMaterial.query.all()
    return render_template('proveedor/solicitudes.html', solicitudes=solicitudes)


@inventarioMaterbp.route('/pedir/<int:id>', methods=['POST'])
@login_required
def pedir_material(id):
    if current_user.role != 'empleado':
        flash("Acceso no autorizado", "material_error")
        return redirect(url_for('auth.login'))

    solicitud = SolicitudMaterial.query.get_or_404(id)

    try:
        existente = MateriaPrima.query.filter_by(nombre=solicitud.nombre, proveedor_id=solicitud.proveedor_id).first()

        if existente:
            existente.cantidad_disponible += solicitud.cantidad
            existente.precio_por_unidad = solicitud.precio_unitario
        else:
            nuevo_material = MateriaPrima(
                nombre=solicitud.nombre,
                cantidad_disponible=solicitud.cantidad,
                unidad=solicitud.unidad,
                precio_por_unidad=solicitud.precio_unitario,
                proveedor_id=solicitud.proveedor_id
            )
            db.session.add(nuevo_material)

        db.session.delete(solicitud)
        db.session.commit()
        flash("Material agregado al inventario", "material_success")

    except Exception as e:
        db.session.rollback()
        flash(f"Error al procesar la solicitud: {str(e)}", "material_error")

    return redirect(url_for('materiales.ver_solicitudes'))
