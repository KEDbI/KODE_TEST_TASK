from fastapi import Depends, status, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.database.database import get_user_data


security = HTTPBasic()


async def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = await get_user_data(credentials.username)
    if user['username'] is None or user['password'] != credentials.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user
