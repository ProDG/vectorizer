from fastapi import Depends, Header, HTTPException, status

from app.core.config import settings


def get_token_from_header(Authorization: str = Header()):
    # Extract the token from the Authorization header.

    scheme, _, param = Authorization.partition(" ")
    if scheme.lower() != "bearer" or not param or param != settings.auth_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return param


def token_required(token: str = Depends(get_token_from_header)):
    # Here you can add additional logic if needed, such as logging the token.
    # For now, we just ensure the token is present.
    return True
