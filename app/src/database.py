from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import app.src.config as config
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


class Base(DeclarativeBase):
    pass

