from sqlalchemy import (
    create_engine, 
    Column, 
    Integer, 
    String, 
    ForeignKey, 
    Enum, 
    DateTime,
    Boolean,
    CheckConstraint, 
    Index
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv
import enum
import os
from sqlalchemy.exc import OperationalError
from uuid import uuid4

# Carregando variáveis de ambiente
load_dotenv()

# Lendo URL do banco de dados do arquivo .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Verificação da variável de ambiente DATABASE_URL
if not DATABASE_URL:
    raise ValueError("DATABASE_URL não está definido no arquivo .env")

# Criação do engine e configuração do session maker
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para as models
Base = declarative_base()

# ========== ENUMS ========== 
class UserRole(str, enum.Enum):
    OPERATOR = "operator"
    BUYER = "buyer"
    MANAGER = "manager"

class PRStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

# ========== TABELAS ==========

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(256), nullable=False)
    role = Column(Enum(UserRole), nullable=False)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    current_stock = Column(Integer, default=0, nullable=False)
    min_stock = Column(Integer, nullable=False, server_default="0")
    max_stock = Column(Integer, nullable=False, server_default="1")

    # Restrições de integridade de dados
    __table_args__ = (
        CheckConstraint('min_stock >= 0', name='check_min_stock_non_negative'),
        CheckConstraint('max_stock > min_stock', name='check_max_stock_greater'),
        CheckConstraint('current_stock >= 0', name='check_current_stock_non_negative'),
        Index('idx_product_stocks', 'min_stock', 'max_stock')
    )

class PurchaseRequest(Base):
    __tablename__ = "purchase_requests"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False, server_default="1")
    requester_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(PRStatus), default=PRStatus.PENDING, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Restrição para garantir que a quantidade seja positiva
    __table_args__ = (
        CheckConstraint('quantity > 0', name='check_quantity_positive'),
    )

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(Integer, primary_key=True, index=True)
    jti = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)

    # Índice para otimizar consultas baseadas em usuário e jti
    __table_args__ = (
        Index("ix_refresh_user_jti", "user_id", "jti"),
    )

# ========== BLACKLIST DE ACCESS TOKEN ==========

class AccessTokenBlacklist(Base):
    __tablename__ = "access_token_blacklist"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(512), unique=True, nullable=False)  # Token será armazenado como string
    jti = Column(String(36), nullable=False)  # Adicionando o campo jti
    revoked_at = Column(DateTime, default=datetime.utcnow, nullable=False)  # Marca quando foi revogado

    # Índice para facilitar buscas rápidas
    __table_args__ = (
        Index('idx_blacklist_token', 'token'),  # Índice para consultas rápidas
        Index('idx_blacklist_jti', 'jti')  # Índice para consultas rápidas pelo jti
    )


# ========== VERIFICAÇÃO DE CONEXÃO ==========

try:
    engine.connect()
    print("✅ Conexão com o banco de dados bem-sucedida!")
except OperationalError as e:
    print(f"❌ Erro de conexão: {e}")
    raise
