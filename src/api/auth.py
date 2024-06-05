from fastapi import Security, HTTPException, status, Request
from fastapi.security.api_key import APIKeyHeader
import os
import dotenv
from datetime import datetime, timedelta
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Optional

dotenv.load_dotenv()

api_keys = []  

api_keys.append(os.environ.get("API_KEY"))
api_key_header = APIKeyHeader(name="access_token", auto_error=False)


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class TokenData(BaseModel):
    user_id: Optional[int] = None



async def get_api_key(request: Request, api_key_header: str = Security(api_key_header)):
    if api_key_header in api_keys:
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden"
        )
