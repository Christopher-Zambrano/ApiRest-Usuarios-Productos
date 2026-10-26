from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel

class UserDB(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, nullable=False)
    nombre = Column(String(70), index=True, nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(250), nullable=False)
    
    productos = relationship("ProductosDB", back_populates="propietario")
    
class ProductosDB(Base):
    __tablename__ = "productos"
    
    id = Column(Integer, primary_key=True, nullable=False)
    nombre = Column(String(70), index=True, nullable=False)
    cantidad = Column(Integer, nullable=False)
    
    user_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    propietario = relationship("UserDB", back_populates="productos")
    
class ProductoCreate(BaseModel):
    nombre: str
    cantidad: int
    
class ProductoResponse(BaseModel):
    id: int
    nombre:str
    cantidad:int
    
    class config():
        from_attributes = True
        
class UserCreate(BaseModel):
    nombre:str
    correo:str
    password:str
    
class UserResponse(BaseModel):
    id:int
    nombre:str
    correo:str
    productos: list[ProductoResponse] = []
    
    class config():
        from_attributes = True
        
class Login(BaseModel):
    correo:str
    password:str