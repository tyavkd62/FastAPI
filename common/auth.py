from enum import StrEnum
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from jose import JWTError, jwt

SECRET_KEY = "THIS_IS_SUPER_SECRET_KEY"
ALGORITHM = 'HS256'

class Role(StrEnum):
    ADMIN = 'ADMIN'
    USER = 'USER'
    
def create_access_token(
    payload: dict,
    role: Role,
    expires_delta: timedelta = timedelta(hours=6),
):
    expire = datetime.utcnow() + expires_delta
    payload.update(
        {
            'role': role,
            'exp': expire
        }
    )
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def decodes_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    