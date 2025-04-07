from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime
import database  # Agora estamos importando as tabelas do arquivo database.py

# Instância do CryptContext para hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------------------- USERS ----------------------

# Função para criar um novo usuário com a senha criptografada
def create_user(db: Session, email: str, password: str, role: str):
    hashed_password = pwd_context.hash(password)  # Criptografa a senha
    db_user = database.User(email=email, hashed_password=hashed_password, role=role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Função para obter um usuário pelo ID
def get_user_by_id(db: Session, user_id: int):
    return db.query(database.User).filter(database.User.id == user_id).first()

# Função para obter um usuário pelo e-mail
def get_user_by_email(db: Session, email: str):
    return db.query(database.User).filter(database.User.email == email).first()

# Função para obter todos os usuários
def get_all_users(db: Session):
    return db.query(database.User).all()

# Função para atualizar a senha de um usuário
def update_user_password(db: Session, user_id: int, new_password: str):
    hashed_password = pwd_context.hash(new_password)
    db.query(database.User).filter(database.User.id == user_id).update({"hashed_password": hashed_password})
    db.commit()

# Função para atualizar informações completas de um usuário
def update_user(db: Session, user_id: int, email: str = None, password: str = None, role: str = None):
    user = db.query(database.User).filter(database.User.id == user_id).first()
    if not user:
        return None
    if email:
        user.email = email
    if password:
        user.hashed_password = pwd_context.hash(password)
    if role:
        user.role = role
    db.commit()
    db.refresh(user)
    return user

# Função para excluir um usuário
def delete_user(db: Session, user_id: int):
    db.query(database.User).filter(database.User.id == user_id).delete()
    db.commit()


# ---------------------- PRODUCTS ----------------------

# Função para criar um novo produto
def create_product(db: Session, name: str, min_stock: int, max_stock: int, current_stock: int = 0):
    db_product = database.Product(name=name, min_stock=min_stock, max_stock=max_stock, current_stock=current_stock)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Função para obter um produto pelo ID
def get_product_by_id(db: Session, product_id: int):
    return db.query(database.Product).filter(database.Product.id == product_id).first()

# Função para obter todos os produtos
def get_all_products(db: Session):
    return db.query(database.Product).all()

# Função para atualizar informações de um produto
def update_product(db: Session, product_id: int, name: str = None, min_stock: int = None, max_stock: int = None, current_stock: int = None):
    product = db.query(database.Product).filter(database.Product.id == product_id).first()
    if not product:
        return None
    if name:
        product.name = name
    if min_stock is not None:
        product.min_stock = min_stock
    if max_stock is not None:
        product.max_stock = max_stock
    if current_stock is not None:
        product.current_stock = current_stock
    db.commit()
    db.refresh(product)
    return product

# Função para excluir um produto
def delete_product(db: Session, product_id: int):
    db.query(database.Product).filter(database.Product.id == product_id).delete()
    db.commit()


# ---------------------- PURCHASE REQUESTS ----------------------

# Função para criar uma solicitação de compra
def create_purchase_request(db: Session, product_id: int, quantity: int, requester_id: int):
    db_request = database.PurchaseRequest(product_id=product_id, quantity=quantity, requester_id=requester_id, status="pending")
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

# Função para obter uma solicitação de compra pelo ID
def get_purchase_request_by_id(db: Session, request_id: int):
    return db.query(database.PurchaseRequest).filter(database.PurchaseRequest.id == request_id).first()

# Função para obter todas as solicitações de compra de um usuário
def get_purchase_requests_by_user(db: Session, user_id: int):
    return db.query(database.PurchaseRequest).filter(database.PurchaseRequest.requester_id == user_id).all()

# Função para obter todas as solicitações de compra (admin ou geral)
def get_all_purchase_requests(db: Session):
    return db.query(database.PurchaseRequest).all()

# Função para atualizar o status de uma solicitação de compra
def update_purchase_request_status(db: Session, request_id: int, status: str):
    db.query(database.PurchaseRequest).filter(database.PurchaseRequest.id == request_id).update({"status": status})
    db.commit()

# Função para excluir uma solicitação de compra
def delete_purchase_request(db: Session, request_id: int):
    db.query(database.PurchaseRequest).filter(database.PurchaseRequest.id == request_id).delete()
    db.commit()
