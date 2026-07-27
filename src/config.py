"""Módulo de configuración general que carga variables de entorno mediante Pydantic Settings."""
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import text
import src.database as database


class Settings(BaseSettings):
    """Configuración global de la aplicación cargada desde el archivo `.env` o variables del sistema."""
    DB_USER: str
    DB_PASSWORD: SecretStr  # Protege la contraseña en logs y volcados de memoria
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    SECRET_KEY: SecretStr  # Clave secreta para firmar tokens de seguridad JWT

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()  # type: ignore


