from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from sqlalchemy import text
import database

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: SecretStr
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8")

settings = Settings() #type: ignore

if __name__ == "__main__":
    try:
        with database.engine.connect() as conexion:
            resultado = conexion.execute(text("SELECT 1;"))
            print("Conexión exitosa. Versión de MySQL")
    except Exception as e:
        print("Error al conectar:", e)

