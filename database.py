from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv
import enum
import os

# ⬇️ Carrega variáveis do .env
load_dotenv()

# ⬇️ Pega a URL do banco direto do .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Configuração do Banco
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Enums
class UserRole(str, enum.Enum):
    OPERATOR = "operator"
    BUYER = "buyer"
    MANAGER = "manager"

# Tabelas
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
    role = Column(Enum(UserRole), nullable=False)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    current_stock = Column(Integer, default=0)
    min_stock = Column(Integer, nullable=False)
    max_stock = Column(Integer, nullable=False)

class PurchaseRequest(Base):
    __tablename__ = "purchase_requests"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

# Cria as tabelas
Base.metadata.create_all(bind=engine)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

# Verifica se a conexão funciona
try:
    engine.connect()
    print("Conexão com o banco de dados bem-sucedida!")
except OperationalError as e:
    print(f"Erro de conexão: {e}")