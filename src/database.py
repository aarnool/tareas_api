from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import src.config as config
from sqlalchemy.engine import URL

DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=config.settings.DB_USER,
    password=config.settings.DB_PASSWORD.get_secret_value(),
    host=config.settings.DB_HOST,
    port=config.settings.DB_PORT,
    database=config.settings.DB_NAME
) 


engine = create_engine(
    DATABASE_URL
)


SessionLocal = sessionmaker(
    autocommit=False, 
    bind=engine)

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=convention)

