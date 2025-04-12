from flask import (
    Blueprint, render_template, redirect, url_for, flash, request,
    session, current_app
)
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from datetime import datetime
from sqlalchemy.orm import joinedload
import os

from models import db, Receta, MateriaPrima, RecetaIngrediente, ProductoTerminado
from forms import RecetaForm, IngredienteForm, RecetaImagenForm

recetas_bp = Blueprint('recetas', __name__, template_folder='../../templates/recetas')

# ------------------- NUEVA RECETA -------------------

@recetas_bp.route("/nueva_receta", methods=['GET', 'POST'])
@login_required
def nueva_receta():
    if current_user.role != 'empleado':
        flash("Acceso no autorizado", "error")
        return redirect(url_for('auth.login')) 
    
    form = RecetaForm()

    if request.method == 'POST' and form.validate_on_submit():
        session['receta'] = {
            'nombre': form.nombre.data,
            'descripcion': form.descripcion.data
        }
        session['ingredientes'] = []  # Limpiamos ingredientes si hay algo
        return redirect(url_for('recetas.agregar_ingredientes'))

    return render_template("nuevaReceta.html", form=form)


# ------------------- AGREGAR INGREDIENTES -------------------

@recetas_bp.route("/nueva_receta_ingredientes", methods=['GET', 'POST'])
@login_required
def agregar_ingredientes():
    if current_user.role != 'empleado':
        flash("Acceso no autorizado", "error")
        return redirect(url_for('auth.login'))
    
    form = IngredienteForm()
    materias_primas = MateriaPrima.query.all()
    form.materia_prima_id.choices = [(i.id, f"{i.nombre} ({i.unidad})") for i in materias_primas]

    if request.method == 'POST' and form.validate_on_submit():
        materia = MateriaPrima.query.get(form.materia_prima_id.data)
        if materia:
            nuevo_ingrediente = {
                'id': materia.id,
                'nombre': materia.nombre,
                'unidad': materia.unidad,
                'cantidad': float(form.cantidad.data)
            }
            session['ingredientes'].append(nuevo_ingrediente)
            flash(f"{materia.nombre} agregado a la receta.", "success")
            return redirect(url_for('recetas.agregar_ingredientes'))

    return render_template("nuevaRecetaIngredientes.html", form=form, materias_primas=materias_primas)

# ------------------- AGREGAR FOTO -------------------

@recetas_bp.route("/agregar_foto", methods=["GET", "POST"])
@login_required
def agregar_foto():

    if current_user.role != 'empleado':
        flash("Acceso no autorizado", "error")
        return redirect(url_for('auth.login'))
    
    form = RecetaImagenForm()

    if request.method == "POST" and form.validate_on_submit():
        imagen = form.imagen.data
        if imagen:
            nombre_archivo = secure_filename(imagen.filename)
            ruta = os.path.join(current_app.root_path, "static/uploads", nombre_archivo)
            imagen.save(ruta)
            session['imagen'] = nombre_archivo
            return redirect(url_for("recetas.finalizar_receta"))

    return render_template("agregarFoto.html", form=form)

# ------------------- FINALIZAR RECETA -------------------

@recetas_bp.route("/finalizar_receta")
@login_required
def finalizar_receta():
    if current_user.role != 'empleado':
        flash("Acceso no autorizado", "error")
        return redirect(url_for('auth.login'))
    
    try:
        # Validación de datos en sesión
        if 'receta' not in session or 'ingredientes' not in session or 'imagen' not in session:
            flash("Faltan datos para guardar la receta.", "warning")
            return redirect(url_for("recetas.nueva_receta"))

        datos = session['receta']
        ingredientes = session['ingredientes']
        imagen = session['imagen']

        # Crear la receta
        receta = Receta(
            nombre=datos['nombre'],
            descripcion=datos.get('descripcion', ''),
            imagen=imagen
        )
        db.session.add(receta)
        db.session.flush()  # Para obtener el ID de la receta

        total_costo = 0
        for item in ingredientes:
            materia = MateriaPrima.query.get(item['id'])
            if materia:
                proporcion = item['cantidad'] / materia.cantidad_disponible if materia.cantidad_disponible else 0
                costo = proporcion * materia.precio_por_unidad
                total_costo += costo

                detalle = RecetaIngrediente(
                    receta_id=receta.id,
                    materia_prima_id=materia.id,
                    cantidad=item['cantidad']
                )
                db.session.add(detalle)

                # Descontar del inventario
                materia.cantidad_disponible -= item['cantidad']
                if materia.cantidad_disponible < 0:
                    materia.cantidad_disponible = 0

        # Crear un solo producto terminado con 300 galletas
        producto = ProductoTerminado(
            nombre=receta.nombre,
            descripcion=receta.descripcion,
            cantidad=300,  # Valor fijo de galletas
            receta_id=receta.id,
            fecha_produccion=datetime.utcnow()
        )
        db.session.add(producto)

        db.session.commit()

        # Limpiar sesión
        session.pop('receta', None)
        session.pop('ingredientes', None)
        session.pop('imagen', None)

        flash("Receta y producto creado correctamente con 300 galletas.", "success")
        return redirect(url_for('recetas.nueva_receta'))

    except Exception as e:
        db.session.rollback()
        flash(f"Ocurrió un error al guardar la receta: {str(e)}", "danger")
        return redirect(url_for("recetas.nueva_receta"))



# ------------------- CANCELAR RECETA -------------------

@recetas_bp.route("/cancelar_receta")
@login_required
def cancelar_receta():
    session.pop('receta', None)
    session.pop('ingredientes', None)
    session.pop('imagen', None)
    flash("Receta cancelada", "info")
    return redirect(url_for('recetas.nueva_receta'))

# ---------------------------------------------------------------------

@recetas_bp.route("/", methods=["GET"])
def lista_recetas_cliente():

    page = request.args.get('page', 1, type=int)

    recetas = Receta.query.options(
        joinedload(Receta.receta_ingredientes).joinedload(RecetaIngrediente.materia_prima)
    ).paginate(page=page, per_page=6, error_out=False)

    return render_template("inicio_cliente.html", recetas=recetas)

#--------------------------------------------------------------------------

from forms import RecetaForm  # Asegúrate de tener esta línea arriba

@recetas_bp.route("/ver_recetas")
@login_required
def ver_recetas():

    if current_user.role != 'empleado':
        flash("Acceso no autorizado", "error")
        return redirect(url_for('auth.login'))
    
    page = request.args.get("page", 1, type=int)
    
    recetas = Receta.query.options(
        joinedload(Receta.receta_ingredientes).joinedload(RecetaIngrediente.materia_prima)
    ).order_by(Receta.nombre).paginate(page=page, per_page=5)

    form = RecetaForm()  # Instancia del formulario

    return render_template("listaRecetas.html", recetas=recetas, form=form)


@recetas_bp.route("/editar_receta/<int:id>", methods=['GET', 'POST'])
@login_required
def editar_receta(id):

    if current_user.role != 'empleado':
        flash("Acceso no autorizado", "error")
        return redirect(url_for('auth.login'))
    
    receta = Receta.query.get_or_404(id)
    form = RecetaForm(obj=receta)

    if request.method == 'POST' and form.validate_on_submit():
        receta.nombre = form.nombre.data
        receta.descripcion = form.descripcion.data
        db.session.commit()
        flash("Receta actualizada correctamente", "success")
        return redirect(url_for('recetas.ver_recetas'))

    return render_template("editarReceta.html", form=form, receta=receta)


@recetas_bp.route("/eliminar_receta/<int:id>", methods=["POST"])
@login_required
def eliminar_receta(id):
    if current_user.role != 'empleado':
        flash("Acceso no autorizado", "receta_error")
        return redirect(url_for('auth.login'))

    receta = Receta.query.get_or_404(id)

    try:
        # Eliminar imagen del servidor
        if receta.imagen:
            ruta_imagen = os.path.join(current_app.root_path, "static/uploads", receta.imagen)
            if os.path.exists(ruta_imagen):
                os.remove(ruta_imagen)

        # Eliminar producto terminado relacionado
        producto = ProductoTerminado.query.filter_by(receta_id=receta.id).first()
        if producto:
            db.session.delete(producto)

        # Ingredientes se eliminarán por cascade si tu relación está bien definida
        db.session.delete(receta)
        db.session.commit()

        flash("Receta eliminada correctamente.", "receta_success")

    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar receta: {str(e)}", "receta_error")

    return redirect(url_for("recetas.ver_recetas"))