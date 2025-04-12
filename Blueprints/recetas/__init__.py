from flask import Blueprint

# Define el blueprint aquí (sin otras dependencias)
recetas_bp = Blueprint('recetas', __name__)

# Importa las rutas DESPUÉS de definir el blueprint
from . import routes