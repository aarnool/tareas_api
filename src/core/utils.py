from fastapi import HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.dependencies import get_current_user

def get_dinamic_identifier(request):
    """Obtiene un identificador dinámico para la limitación de velocidad basada en IP o Validacion por el Cookie."""
    if "auth_token" in request.cookies:
        try:
            token = get_current_user(auth_token=request.cookies.get("auth_token"))
            return token.get("user_id", get_remote_address(request))
        except HTTPException:
            pass  # Si el token es inválido o ha expirado, se usará la dirección IP como identificador
        
    return get_remote_address(request)


limiter =  Limiter(key_func=get_dinamic_identifier)
