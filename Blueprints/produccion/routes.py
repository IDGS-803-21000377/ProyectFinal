from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from datetime import datetime
from models import db, Receta, ProductoTerminado, MateriaPrima, RecetaIngrediente
from sqlalchemy.orm import joinedload

produccion_bp = Blueprint("produccion", __name__, url_prefix="/produccion")

@produccion_bp.route("/")
@login_required
def vista_produccion():
    if current_user.role != 'empleado':
        flash("Acceso no autorizado", "produccion_error")
        return redirect(url_for('auth.login'))
    
    recetas = Receta.query.options(
        joinedload(Receta.receta_ingredientes).joinedload(RecetaIngrediente.materia_prima)
    ).order_by(Receta.nombre).all()
    
    return render_template("produccion.html", recetas=recetas)

@produccion_bp.route("/producir/<int:receta_id>", methods=["POST"])
@login_required
def producir_receta(receta_id):
    if current_user.role != 'empleado':
        flash("Acceso no autorizado", "produccion_error")
        return redirect(url_for('auth.login'))
    
    receta = Receta.query.get_or_404(receta_id)

    try:
        # Validar que haya suficiente materia prima
        for ingrediente in receta.receta_ingredientes:
            materia = ingrediente.materia_prima
            if materia.cantidad_disponible < ingrediente.cantidad:
                flash(f"No hay suficiente {materia.nombre} en inventario.", "produccion_error")
                return redirect(url_for('produccion.vista_produccion'))

        # Descontar del inventario
        for ingrediente in receta.receta_ingredientes:
            materia = ingrediente.materia_prima
            materia.cantidad_disponible -= ingrediente.cantidad
            db.session.add(materia)

        # Crear o actualizar el producto terminado
        producto = ProductoTerminado.query.filter_by(receta_id=receta.id).first()

        if producto:
            producto.cantidad += 300
            producto.fecha_produccion = datetime.utcnow()
        else:
            producto = ProductoTerminado(
                nombre=receta.nombre,
                descripcion=receta.descripcion,
                cantidad=300,
                receta_id=receta.id,
                fecha_produccion=datetime.utcnow()
            )
            db.session.add(producto)

        db.session.commit()
        flash(f"Se han producido 300 galletas para la receta '{receta.nombre}'.", "produccion_success")

    except Exception as e:
        db.session.rollback()
        flash(f"Error al producir: {str(e)}", "produccion_error")

    return redirect(url_for('produccion.vista_produccion'))
