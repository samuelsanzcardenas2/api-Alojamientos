import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuracion central de a aplicacion"""

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    _jwt_exp = os.getenv("JWT_EXP_MINUTES", "15")

    JWT_EXP_MINUTES = int(_jwt_exp) if _jwt_exp.isdigit() else 15

    _db_user = os.getenv("DB_USER", "").strip()
    _db_password = os.getenv("DB_PASSWORD", "").strip()
    _db_host = os.getenv("DB_HOST", "localhost").strip()
    _db_port = os.getenv("DB_PORT", "3307").strip()
    _db_name = os.getenv("DB_NAME", "alojamientos_db").strip()

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{_db_user}:{_db_password}@{_db_host}:{_db_port}/{_db_name}"
    )

    is_testing = os.getenv("FLASK_TESTING", "false").lower() == "true"

    if not is_testing:
        if not _db_user:
            raise ValueError("Falta la variable DB_USER en el archivo .env")
        if not _db_name:
            raise ValueError("Falta la variable DB_NAME en el archivo .env")
        if not SECRET_KEY:
            raise ValueError("Falta la variable SECRET_KEY en el archivo .env")
    else:
        # Valores por defecto para testing
        SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
        if not SECRET_KEY:
            SECRET_KEY = "test-key-for-pytest"
    _origins_env = os.getenv("CORS_ALLOWED_ORIGINS", "")
    if _origins_env:
        CORS_ALLOWED_ORIGINS = [o.strip() for o in _origins_env.split(",") if o.strip()]
    else:
        CORS_ALLOWED_ORIGINS = [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:5500",
            "http://localhost:8080",
        ]

    # Ruta base del proyecto
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # raiz del proyecto
