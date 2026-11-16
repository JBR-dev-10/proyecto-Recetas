from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    ingredientes = relationship("Ingrediente", back_populates="propietario", cascade="all, delete-orphan")
    recetas = relationship("Receta", back_populates="autor", cascade="all, delete-orphan")
    calificaciones = relationship("Calificacion", back_populates="usuario", cascade="all, delete-orphan")


class Ingrediente(Base):
    __tablename__ = "ingredientes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    nombre = Column(String(100), nullable=False)
    cantidad = Column(Float, nullable=False)
    unidad = Column(String(50), nullable=False)  # ej: gramos, unidades, ml

    propietario = relationship("Usuario", back_populates="ingredientes")


class Receta(Base):
    __tablename__ = "recetas"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    nombre_plato = Column(String(200), nullable=False)
    ingredientes_json = Column(JSON, nullable=False)  # Lista de ingredientes con cantidades
    pasos_json = Column(JSON, nullable=False)         # Lista ordenada de pasos
    tiempo_estimado = Column(String(50), nullable=False)
    dificultad = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    autor = relationship("Usuario", back_populates="recetas")
    calificaciones = relationship("Calificacion", back_populates="receta", cascade="all, delete-orphan")


class Calificacion(Base):
    __tablename__ = "calificaciones"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    receta_id = Column(Integer, ForeignKey("recetas.id", ondelete="CASCADE"), nullable=False)
    puntuacion = Column(Integer, nullable=False)  # Validado de 1 a 5
    comentario = Column(Text, nullable=True)

    usuario = relationship("Usuario", back_populates="calificaciones")
    receta = relationship("Receta", back_populates="calificaciones")