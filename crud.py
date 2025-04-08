from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime
from database import User, Product, PurchaseRequest, RoleEnum, StatusEnum

# Instância do CryptContext para hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------------------- USERS ----------------------

def create_user(db: Session, email: str, password: str, role: RoleEnum):
    hashed_password = pwd_context.hash(password)
    db_user = User(email=email, hashed_password=hashed_password, role=role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_all_users(db: Session):
    return db.query(User).all()

def update_user_password(db: Session, user_id: int, new_password: str):
    hashed_password = pwd_context.hash(new_password)
    db.query(User).filter(User.id == user_id).update({"hashed_password": hashed_password})
    db.commit()

def update_user(db: Session, user_id: int, email: str = None, password: str = None, role: RoleEnum = None):
    user = db.query(User).filter(User.id == user_id).first()
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

def delete_user(db: Session, user_id: int):
    db.query(User).filter(User.id == user_id).delete()
    db.commit()


# ---------------------- PRODUCTS ----------------------

def create_product(db: Session, name: str, min_stock: int, max_stock: int, current_stock: int = 0):
    db_product = Product(name=name, min_stock=min_stock, max_stock=max_stock, current_stock=current_stock)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_all_products(db: Session):
    return db.query(Product).all()

def update_product(db: Session, product_id: int, name: str = None, min_stock: int = None, max_stock: int = None, current_stock: int = None):
    product = db.query(Product).filter(Product.id == product_id).first()
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

def delete_product(db: Session, product_id: int):
    db.query(Product).filter(Product.id == product_id).delete()
    db.commit()


# ---------------------- PURCHASE REQUESTS ----------------------

def create_purchase_request(db: Session, product_id: int, quantity: int, requester_id: int):
    db_request = PurchaseRequest(
        product_id=product_id,
        quantity=quantity,
        requester_id=requester_id,
        status=StatusEnum.PENDING
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

def get_purchase_request_by_id(db: Session, request_id: int):
    return db.query(PurchaseRequest).filter(PurchaseRequest.id == request_id).first()

def get_purchase_requests_by_user(db: Session, user_id: int):
    return db.query(PurchaseRequest).filter(PurchaseRequest.requester_id == user_id).all()

def get_all_purchase_requests(db: Session):
    return db.query(PurchaseRequest).all()

def update_purchase_request_status(db: Session, request_id: int, status: StatusEnum):
    db.query(PurchaseRequest).filter(PurchaseRequest.id == request_id).update({"status": status})
    db.commit()

def delete_purchase_request(db: Session, request_id: int):
    db.query(PurchaseRequest).filter(PurchaseRequest.id == request_id).delete()
    db.commit()
