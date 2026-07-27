"""Módulo de configuración y conexión al motor de base de datos relacional (SQLAlchemy)."""
from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import src.config as config

# Construye la URL de conexión de manera segura utilizando las credenciales protegidas
DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=config.settings.DB_USER,
    password=config.settings.DB_PASSWORD.get_secret_value(),
    host=config.settings.DB_HOST,
    port=config.settings.DB_PORT,
    database=config.settings.DB_NAME
)

engine = create_engine(DATABASE_URL)

# Fábrica de sesiones de base de datos para inyectar en las peticiones HTTP
SessionLocal = sessionmaker(
    autocommit=False,
    bind=engine
)

# Convención de nombres para restricciones SQL, esencial para migraciones automáticas en Alembic
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


class Base(DeclarativeBase):
    """Clase base declarativa para todos los modelos ORM del sistema."""
    metadata = MetaData(naming_convention=convention)


