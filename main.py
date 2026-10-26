from database import (Base, engine, get_db)
from model import (UserCreate, UserDB, UserResponse, ProductoResponse, ProductoCreate, ProductosDB, Login)
from security import (crear_token, decifrar_token, encriptar_password, verificar_password)
from sqlalchemy.orm import Session
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    correo = decifrar_token(token)
    if not correo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
        
    user = db.query(UserDB).filter(UserDB.correo == correo).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
        
    return user

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.get("/usuarios/me",response_model=UserResponse)
def obtener_perfil_actual(current_user: UserDB = Depends(get_current_user)):
    return current_user

@app.get("/usuarios/{id}", response_model=UserResponse)
def obtener_usuario_id(id:int, db:Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.id == id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
        
    return user

@app.post("/usuarios",response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(nuevo_usuario: UserCreate, db: Session = Depends(get_db)):
    
    user = db.query(UserDB).filter(UserDB.correo == nuevo_usuario.correo).first()
    
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Correo ya registrado"
        )
        
    password_segura = encriptar_password(nuevo_usuario.password)
        
    registro = UserDB(
        nombre = nuevo_usuario.nombre,
        correo = nuevo_usuario.correo,
        hashed_password = password_segura
    )
    
    db.add(registro)
    db.commit()
    db.refresh(registro)
    
    return registro

@app.post("/productos", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def registrar_producto(nuevo_prod: ProductoCreate, db:Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    
    registro = ProductosDB(
        nombre = nuevo_prod.nombre,
        cantidad = nuevo_prod.cantidad,
        user_id = current_user.id
    )
    
    db.add(registro)
    db.commit()
    db.refresh(registro)
    
    return registro

@app.post("/login")
def iniciar_sesion(log: Login, db:Session = Depends(get_db)):
    
    user = db.query(UserDB).filter(UserDB.correo == log.correo).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
        
    password = verificar_password(log.password , user.hashed_password)
    
    if not password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
        
    token = crear_token({"sub": user.correo})
    
    return{
        "access token": token,
        "token type": "bearer",
    }
    
@app.put("/usuarios/me", response_model=UserResponse)
def modificar_usuario(user_mod: UserCreate, db:Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    

    
    current_user.nombre = user_mod.nombre
    current_user.correo = user_mod.correo
    
    password_valida = encriptar_password(user_mod.password)
    
    current_user.hashed_password = password_valida
    
    db.commit()
    db.refresh(current_user)
    
    return current_user

@app.delete("/usuarios/me")
def eliminar_usuario(db:Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    
    
    db.delete(current_user)
    db.commit()
    
    return {
        "mensaje": "Usuario eliminado con exito"
    }
    
@app.delete("/productos/{id}")
def eliminar_productos(id:int , db:Session = Depends(get_db), current_user:UserDB = Depends(get_current_user)):
    
    productos = db.query(ProductosDB).filter(ProductosDB.id == id).first()
    
    if not productos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
        
    if productos.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No puedes eliminar un producto que no te pertenece"
        )
        
    db.delete(productos)
    db.commit()
    
    return {
        "mensaje": "Producto eliminado con exito"
    }