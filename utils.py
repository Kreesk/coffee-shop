from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
import jwt
import datetime
import os

load_dotenv()
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")

def create_token(username, role):
    payload = {
        'role': role,
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        'iat': datetime.datetime.utcnow(),
        'nbf': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return {'token': token}

def verify_token(token: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    try:
        decoded = jwt.decode(token.credentials, SECRET_KEY, algorithms=['HS256'])
        return {"username": decoded['username'], "role": decoded['role']}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Токен истек")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Неверный токен")

def verify_admin(user: dict = Depends(verify_token)) -> dict:
    if user['role'] != 'admin':
        raise HTTPException(status_code=403, detail="Только для администратора")
    return user