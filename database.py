from sqlalchemy import (
    create_engine, 
    Column, 
    Integer, 
    String, 
    ForeignKey, 
    Enum, 
    DateTime,
    CheckConstraint,  # <--- ADICIONAR IMPORTAÇÃO
    Index  # <--- ADICIONAR PARA ÍNDICES
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv
import enum
import os
from sqlalchemy.exc import OperationalError

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ========== ENUMS ==========
class UserRole(str, enum.Enum):
    OPERATOR = "operator"
    BUYER = "buyer"
    MANAGER = "manager"

# ADICIONAR ENUM PARA STATUS DE SOLICITAÇÃO
class PRStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

# ========== TABELAS ==========
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(
        String(100), 
        unique=True, 
        nullable=False,
        index=True  # <--- ÍNDICE PARA BUSCAS POR EMAIL
    )
    hashed_password = Column(String(256), nullable=False)
    role = Column(Enum(UserRole), nullable=False)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(
        String(100), 
        nullable=False,
        index=True  # <--- ÍNDICE PARA BUSCAS POR NOME
    )
    current_stock = Column(
        Integer, 
        default=0,
        nullable=False
    )
    min_stock = Column(
        Integer, 
        nullable=False,
        server_default="0"  # <--- VALOR PADRÃO SEGURO
    )
    max_stock = Column(
        Integer, 
        nullable=False,
        server_default="1"  # <--- EVITA VALOR ZERO
    )

    # ========== CONSTRAINTS CRÍTICAS ==========
    __table_args__ = (
        CheckConstraint(
            'min_stock >= 0',  # Não permite estoque mínimo negativo
            name='check_min_stock_non_negative'
        ),
        CheckConstraint(
            'max_stock > min_stock',  # Garante estoque máximo válido
            name='check_max_stock_greater'
        ),
        CheckConstraint(
            'current_stock >= 0',  # Não permite estoque atual negativo
            name='check_current_stock_non_negative'
        ),
        Index(  # Índice composto para consultas frequentes
            'idx_product_stocks', 
            'min_stock', 
            'max_stock'
        )
    )

class PurchaseRequest(Base):
    __tablename__ = "purchase_requests"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(
        Integer, 
        ForeignKey("products.id", ondelete="CASCADE"),  # <--- CASCADE DELETE
        nullable=False
    )
    quantity = Column(
        Integer, 
        nullable=False,
        server_default="1"  # <--- QUANTIDADE MÍNIMA PADRÃO
    )
    requester_id = Column(
        Integer, 
        ForeignKey("users.id", ondelete="CASCADE"),  # <--- CASCADE DELETE
        nullable=False
    )
    status = Column(
        Enum(PRStatus),  # <--- TROCA STRING POR ENUM
        default=PRStatus.PENDING,
        nullable=False,
        index=True  # <--- ÍNDICE PARA FILTROS FREQUENTES
    )
    created_at = Column(
        DateTime, 
        default=datetime.utcnow,
        index=True  # <--- ÍNDICE PARA CONSULTAS TEMPORAIS
    )

    # ========== CONSTRAINTS ADICIONAIS ==========
    __table_args__ = (
        CheckConstraint(
            'quantity > 0',  # Não permite pedir quantidade zero/negativa
            name='check_quantity_positive'
        ),
    )

# ========== VERIFICAÇÃO DE CONEXÃO ==========
try:
    engine.connect()
    print("✅ Conexão com o banco de dados bem-sucedida!")
except OperationalError as e:
    print(f"❌ Erro de conexão: {e}")
    raise