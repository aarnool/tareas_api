import jwt
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.dependencies import get_current_user
from fastapi import Request

def get_dinamic_identifier(request: Request) -> str:
    """Obtiene un identificador dinámico para la limitación de velocidad basada en IP o Validacion por el Cookie."""

    if "auth_token" in request.cookies:
        try:
            payload = get_current_user(request.cookies.get("auth_token"))
            user_id = payload.get("user_id")
            return str(user_id)
        except jwt.PyJWTError:
            pass  # Si el token es inválido o ha expirado, se usará la dirección IP como identificador
        
    return get_remote_address(request)


limiter =  Limiter(key_func=get_dinamic_identifier)
