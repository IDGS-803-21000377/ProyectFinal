from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, current_user
from sqlalchemy.orm import joinedload
from models import DetalleVenta, Venta, db, Pedido, DetallePedido, ProductoTerminado
from datetime import datetime
import forms
import os

pedidos_bp = Blueprint('pedidos', __name__, url_prefix='/pedidos')

@pedidos_bp.route('/pedidos')
@login_required
def index():
    return render_template("pedidos.html")

@pedidos_bp.route('/', methods=['GET', 'POST'])
@login_required
def save():
    create_form = forms.PedidoForm(request.form)

    registros = []

    productos = ProductoTerminado.query.all()

    try:
        with open("registros.txt", "r") as archivo:
            for linea in archivo:
                partes = linea.strip().split(",")
                if len(partes) == 6:
                    registros.append({
                        "producto_terminado": partes[0],
                        "presentacion": partes[1],
                        "cantidad": partes[2],
                        "subtotal": partes[3],
                        "fecha_recoleccion": partes[4],
                        "fecha_registro": partes[5]
                    })
    except FileNotFoundError:
        pass

    detalles = (
        db.session.query(DetallePedido)
        .join(Pedido)
        .join(ProductoTerminado)
        .filter(Pedido.id_user == current_user.id_user, Pedido.estatus == "pendiente")
        .all()
    )

    print(f"ID del usuario actual: {current_user.id_user}")
    print(f"Detalles encontrados: {detalles}")

    if request.method == "POST":
        producto_terminado = request.form.get("producto_terminado")
        presentacion = request.form.get("presentacion")
        cantidad = int(request.form.get("cantidad", 0))
        fecha_recoleccion = request.form.get("fecha_recoleccion")

        precios_presentacion = {
            "paquete": 50,
            "caja": 90,
            "individual": 8
        }

        precio_presentacion = precios_presentacion.get(presentacion, 0)
        subtotal = precio_presentacion * cantidad

        print("producto_terminado:", producto_terminado)
        print("Tipo:", type(producto_terminado))
        with open("registros.txt", "a") as archivo:
            archivo.write(f"{producto_terminado},{presentacion},{cantidad},{subtotal},{fecha_recoleccion},{datetime.utcnow().date()}\n")

        return redirect(url_for("pedidos.save"))

    return render_template("pedidos.html", form=create_form, registros=registros, detalles=detalles, productos=productos)

@pedidos_bp.route("/delete", methods=["POST"])
@login_required
def delete():
    id_registro = int(request.form.get("id", 0))

    if id_registro:
        with open("registros.txt", "r") as archivo:
            registros = archivo.readlines()
        
        if 0 < id_registro <= len(registros):
            del registros[id_registro - 1]
        
        with open("registros.txt", "w") as archivo:
            archivo.writelines(registros)

    return redirect(url_for("pedidos.save"))

@pedidos_bp.route("/cargar_pedidos", methods=["POST"])
@login_required
def cargar_pedidos():
    try:
        with open("registros.txt", "r") as file:
            lineas = file.readlines()

        for linea in lineas:
            datos = linea.strip().split(',')

            if len(datos) == 6:
                id_producto, presentacion, cantidad, subtotal, fecha_recoleccion, fecha = datos

                if not id_producto.isdigit():
                    print(f"ID inválido para ProductoTerminado: {id_producto}")
                    continue

                try:
                    fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
                    fecha_recoleccion = datetime.strptime(fecha_recoleccion, "%Y-%m-%d").date()
                except ValueError as ve:
                    print(f"Error al convertir fechas: {ve}")
                    continue

                producto = ProductoTerminado.query.get(int(id_producto))
                if not producto:
                    print(f"Producto con ID {id_producto} no encontrado.")
                    continue

                pedido = Pedido(
                    id_user=current_user.id_user,
                    fecha_recoleccion=fecha_recoleccion,
                    fecha=fecha
                )
                db.session.add(pedido)
                db.session.flush()

                detalle = DetallePedido(
                    idPedido=pedido.idPedido,
                    idProductoTerminado=producto.id,
                    presentacion=presentacion,
                    cantidad=int(cantidad),
                    subtotal=float(subtotal)
                )
                db.session.add(detalle)

        db.session.commit()

        with open("registros.txt", "w") as file:
            file.write("")

        flash("Registros guardados correctamente", "success")

    except Exception as e:
        print(f"Error al guardar registros: {str(e)}")

    return redirect(url_for("pedidos.save"))