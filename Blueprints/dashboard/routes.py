from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from flask_login import login_required
from sqlalchemy import func, case
from datetime import datetime, timedelta, date
from models import db, Venta, ProductoTerminado, DetalleVenta
import os

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def dashboard():
    if current_user.role != 'empleado':
        flash("Acceso no autorizado", "error")
        return redirect(url_for('auth.login'))
    
    hoy = date.today()

    ventas_dia = db.session.query(func.sum(Venta.precio)).filter(Venta.fechaVenta == hoy).scalar() or 0

    ventas_totales = db.session.query(func.sum(Venta.precio)).scalar() or 0

    productos_vendidos = db.session.query(
        ProductoTerminado.nombre,
        func.sum(
            case(
                (DetalleVenta.presentacion == 'caja', DetalleVenta.cantidad * 20),
                (DetalleVenta.presentacion == 'paquete', DetalleVenta.cantidad * 10),
                (DetalleVenta.presentacion == 'individual', DetalleVenta.cantidad * 1),
                else_=DetalleVenta.cantidad
            )
        ).label('total_vendidos')
    ).join(DetalleVenta.producto_terminado
    ).group_by(ProductoTerminado.nombre
    ).order_by(func.sum(
        case(
            (DetalleVenta.presentacion == 'caja', DetalleVenta.cantidad * 20),
            (DetalleVenta.presentacion == 'paquete', DetalleVenta.cantidad * 10),
            (DetalleVenta.presentacion == 'individual', DetalleVenta.cantidad * 1),
            else_=DetalleVenta.cantidad
        )
    ).desc()
    ).limit(5).all()

    productos_vendidos_datas = [
    {"nombre": producto, "total_vendidos": total} for producto, total in productos_vendidos
    ]

    presentaciones_vendidas = db.session.query(
        DetalleVenta.presentacion,
        func.sum(DetalleVenta.cantidad).label('total')
    ).group_by(DetalleVenta.presentacion
    ).order_by(func.sum(DetalleVenta.cantidad).desc()
    ).limit(5).all()

    total_presentaciones = sum([p.total for p in presentaciones_vendidas]) or 1  # Evita división por cero
    presentaciones_porcentaje = [{
        'presentacion': p.presentacion,
        'total': p.total,
        'porcentaje': round((p.total / total_presentaciones) * 100, 2)
    } for p in presentaciones_vendidas]
    
    productos_vendidos_data = [{'nombre': p.nombre, 'total_vendidos': p.total_vendidos} for p in productos_vendidos]
    presentaciones_vendidas_data = [{'presentacion': p.presentacion, 'total': p.total} for p in presentaciones_vendidas]
    
    fechas_ventas = db.session.query(Venta.fechaVenta, func.sum(Venta.precio).label('ventas_totales'))\
        .group_by(Venta.fechaVenta).order_by(Venta.fechaVenta).all()

    fechas = [str(f[0]) for f in fechas_ventas] 
    ventas_por_fecha = [f[1] for f in fechas_ventas]

    return render_template('dashboard.html',
                           ventas_dia=ventas_dia,
                           ventas_totales=ventas_totales,
                           productos_vendidos=productos_vendidos,
                           productos_vendidos_datas= productos_vendidos_datas,
                           presentaciones_vendidas=presentaciones_vendidas,
                           fechas=fechas,
                           ventas_por_fecha=ventas_por_fecha,
                           presentaciones_porcentaje=presentaciones_porcentaje)
