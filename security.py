import bcrypt
from jose import jwt, JWTError
from datetime import datetime, timedelta,timezone
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_EXPIRE_TIME = 30

def encriptar_password(password:str) -> str:
    password_bytes  = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes,salt)
    
    return hashed.decode("utf-8")

def verificar_password(password_usuario: str, password_encriptada:str) -> bool:
    
    pass_plana = password_usuario.encode("utf-8")[:72]
    pass_encrip = password_encriptada.encode("utf-8")
    
    return bcrypt.checkpw(pass_plana, pass_encrip)

def crear_token(data:dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_EXPIRE_TIME)
    to_encode.update({"exp": expire})
    
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return token

def decifrar_token(token:str) -> str | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
        