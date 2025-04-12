
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, current_user
from models import db, Venta, DetalleVenta, Pedido, DetallePedido, ProductoTerminado
from datetime import datetime
import os
import forms

ventas_bp = Blueprint('ventas', __name__, url_prefix='/ventas')

@ventas_bp.route('/', methods=['GET', 'POST'])
@login_required
def save():
    if current_user.role != 'empleado':
      flash("Acceso no autorizado", "error")
      return redirect(url_for('auth.login'))
    create_form = forms.PedidoForm(request.form)

    registros = []

    productos = ProductoTerminado.query.all()

    ventas_realizadas = db.session.query(Venta, DetalleVenta, ProductoTerminado) \
    .select_from(Venta) \
    .join(DetalleVenta, DetalleVenta.idVenta == Venta.idVenta) \
    .join(ProductoTerminado, ProductoTerminado.id == DetalleVenta.idProductoTerminado) \
    .order_by(Venta.fechaVenta.desc()) \
    .all()

    try:
        with open("ventas.txt", "r") as archivo:
            for linea in archivo:
                partes = linea.strip().split(",")
                if len(partes) == 5:
                    registros.append({
                        "producto_terminado": partes[0],
                        "presentacion": partes[1],
                        "cantidad": partes[2],
                        "subtotal": partes[3],
                        "fecha_registro": partes[4]
                    })
    except FileNotFoundError:
        pass

    detalles = (
        db.session.query(DetallePedido)
        .join(Pedido)
        .join(ProductoTerminado)
        .filter(Pedido.estatus == "pendiente")
        .options(db.joinedload(DetallePedido.pedido))
        .all()
    )

    if request.method == "POST":
        producto_terminado = request.form.get("producto_terminado")
        presentacion = request.form.get("presentacion")
        cantidad = int(request.form.get("cantidad", 0))

        precios_presentacion = {
            "paquete": 50,
            "caja": 90,
            "individual": 8
        }

        precio_presentacion = precios_presentacion.get(presentacion, 0)
        subtotal = precio_presentacion * cantidad
        
        print("producto_terminado:", producto_terminado)

        with open("ventas.txt", "a") as archivo:
            archivo.write(f"{producto_terminado},{presentacion},{cantidad},{subtotal},{datetime.utcnow().date()}\n")

        return redirect(url_for("ventas.save"))

    return render_template("ventas.html", form=create_form, registros=registros, detalles=detalles, productos=productos, ventas_realizadas = ventas_realizadas)

@ventas_bp.route("/delete", methods=["POST"])
@login_required
def delete():
    if current_user.role != 'empleado':
      flash("Acceso no autorizado", "error")
      return redirect(url_for('auth.login'))
    id_registro = int(request.form.get("id", 0))

    if id_registro:
        with open("ventas.txt", "r") as archivo:
            registros = archivo.readlines()
        
        if 0 < id_registro <= len(registros):
            del registros[id_registro - 1]
        
        with open("ventas.txt", "w") as archivo:
            archivo.writelines(registros)

    return redirect(url_for("ventas.save"))

@ventas_bp.route("/cargar_ventas", methods=["POST"])
@login_required
def cargar_ventas():
    if current_user.role != 'empleado':
      flash("Acceso no autorizado", "error")
      return redirect(url_for('auth.login'))
    try:
        with open("ventas.txt", "r") as file:
            lineas = file.readlines()

        for linea in lineas:
            datos = linea.strip().split(',')
            
            if len(datos) >= 6:
                idGalleta, presentacion, cantidad, subtotal, fecha_recoleccion, fecha = datos
                
                fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
                fecha_recoleccion = datetime.strptime(fecha_recoleccion, "%Y-%m-%d").date()

                venta = venta(
                    id_user=current_user.id_user,
                    fecha_recoleccion=fecha_recoleccion,
                    fecha=fecha,
                )
                db.session.add(venta)
                db.session.flush()

                detalle = DetalleVenta(
                    idPedido=venta.idVenta,
                    idGalleta=int(idGalleta) if idGalleta.isdigit() else None,
                    presentacion=presentacion,
                    cantidad=int(cantidad),
                    subtotal=float(subtotal)
                )
                db.session.add(detalle)

        db.session.commit()

        with open("ventas.txt", "w") as file:
            file.write("")

        flash("Registros guardados correctamente", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al guardar registros: {str(e)}", "danger")

    return redirect(url_for("ventas.save"))

@ventas_bp.route("/realizar_venta", methods=["POST"])
@login_required
def realizar_venta():
    if current_user.role != 'empleado':
        flash("Acceso no autorizado", "error")
        return redirect(url_for('auth.login'))

    try:
        with open("ventas.txt", "r") as file:
            lineas = file.readlines()

        venta_realizada = False  # Bandera para saber si al menos una venta fue válida

        for linea in lineas:
            datos = linea.strip().split(',')

            if len(datos) == 5:
                idProductoTerminado, presentacion, cantidad, subtotal, fecha = datos

                fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
                producto_terminado = ProductoTerminado.query.get(idProductoTerminado)

                if not producto_terminado:
                    flash(f"ProductoTerminado con id {idProductoTerminado} no encontrado.", "danger")
                    continue

                unidades_por_presentacion = {
                    "individual": 1,
                    "paquete": 10,
                    "caja": 20
                }

                unidades_a_restar = unidades_por_presentacion.get(presentacion.lower(), 1) * int(cantidad)

                if producto_terminado.cantidad >= unidades_a_restar:
                    # Crear venta
                    venta = Venta(
                        id_vendedor=current_user.id_user,
                        fechaVenta=fecha,
                        precio=float(subtotal)
                    )
                    db.session.add(venta)
                    db.session.flush()

                    # Actualizar inventario
                    producto_terminado.cantidad -= unidades_a_restar

                    # Crear detalle de venta
                    detalle_venta = DetalleVenta(
                        idVenta=venta.idVenta,
                        idProductoTerminado=producto_terminado.id,
                        cantidad=int(cantidad),
                        presentacion=presentacion,
                        subtotal=float(subtotal)
                    )
                    db.session.add(detalle_venta)

                    venta_realizada = True
                else:
                    flash(f"No hay suficiente inventario para realizar la venta", "danger")

        if venta_realizada:
            db.session.commit()
            with open("ventas.txt", "w") as file:
                file.write("")
            flash("Venta registrada correctamente", "success")
        else:
            db.session.rollback()

    except Exception as e:
        db.session.rollback()
        print(f"Error al guardar venta: {str(e)}")
        flash(f"Error al registrar venta: {str(e)}", "danger")

    return redirect(url_for("ventas.save"))

@ventas_bp.route('/realizar_venta_pedido', methods=['POST'])
@login_required
def realizar_venta_pedido():
    if current_user.role != 'empleado':
      flash("Acceso no autorizado", "error")
      return redirect(url_for('auth.login'))
    id_pedido = request.form.get('idPedido')
    pedido = Pedido.query.get(id_pedido)

    if not pedido:
        flash("Pedido no encontrado.", "error")
        return redirect(url_for('ventas.save'))

    venta = Venta(
        id_cliente=pedido.id_user,
        id_vendedor=current_user.id_user,
        idPedido=pedido.idPedido,
        fechaVenta=datetime.utcnow(),
        precio=pedido.detalles[0].subtotal * len(pedido.detalles)
    )

    db.session.add(venta)
    db.session.flush()  

    unidades_por_presentacion = {
        "individual": 1,
        "paquete": 10,
        "caja": 20
    }

    for detalle in pedido.detalles:
        producto_terminado = ProductoTerminado.query.get(detalle.idProductoTerminado)
        if not producto_terminado:
            flash(f"Producto terminado con ID {detalle.idProductoTerminado} no encontrado.", "danger")
            continue

        unidades_a_restar = unidades_por_presentacion.get(detalle.presentacion.lower(), 1) * detalle.cantidad

        if producto_terminado.cantidad >= unidades_a_restar:
            producto_terminado.cantidad -= unidades_a_restar
        else:
            flash(f"No hay suficiente inventario para '{producto_terminado.nombre}'.", "danger")
            continue  

        detalle_venta = DetalleVenta(
            idVenta=venta.idVenta,
            idProductoTerminado=detalle.idProductoTerminado,
            presentacion=detalle.presentacion,
            cantidad=detalle.cantidad,
            subtotal=detalle.subtotal
        )
        db.session.add(detalle_venta)

    pedido.estatus = "vendido"
    db.session.commit()

    flash("Venta registrada exitosamente.", "success")
    return redirect(url_for('ventas.save'))