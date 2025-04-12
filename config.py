import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()



class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave_segura_por_defecto')
    SESSION_COOKIE_SECURE = False
    UPLOAD_FOLDER = "static/uploads"
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf"}
    
    # Configuración de reCAPTCHA
    RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY', '6LevGAgrAAAAAEH3el5Kr_BpvX16s-eErIVH5vaS')
    RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY', '6LevGAgrAAAAADKLUnZjHsNkhADR9UL3qxRBqWsR')
    
    # Configuración de SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://LuisGio52:LGCP12345@127.0.0.1/galletasdb')

    #Flask-Mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'gourmetcookies654@gmail.com' 
    MAIL_PASSWORD = 'xlps ugrr iprs cgbh' 
    MAIL_DEFAULT_SENDER = 'gourmetcookies654@gmail.com' 
    
class DevelopmentConfig(Config):
    DEBUG = True
    RECAPTCHA_TESTING = True  # Permite pruebas de reCAPTCHA en desarrollo

class ProductionConfig:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave_segura_por_defecto')