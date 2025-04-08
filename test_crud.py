import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Generator
import sqlalchemy
from uuid import uuid4
from database import SessionLocal, User, Product, PurchaseRequest, UserRole, PRStatus

@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()

# ========== TESTES DE USUÁRIO ==========
def test_create_user(db):
    email = f"user_{uuid4()}@example.com"
    user = User(email=email, hashed_password="hashedpwd", role=UserRole.OPERATOR)
    db.add(user)
    db.commit()
    db.refresh(user)
    assert user.id is not None
    assert user.email == email
    assert user.role == UserRole.OPERATOR

def test_create_user_duplicate_email(db):
    email = f"user_{uuid4()}@example.com"
    user1 = User(email=email, hashed_password="pwd", role=UserRole.MANAGER)
    user2 = User(email=email, hashed_password="pwd", role=UserRole.BUYER)
    db.add(user1)
    db.commit()
    db.add(user2)
    with pytest.raises(IntegrityError):
        db.commit()

# ========== TESTES DE PRODUTO ==========
def test_create_valid_product(db):
    product = Product(name="Produto 1", current_stock=10, min_stock=5, max_stock=20)
    db.add(product)
    db.commit()
    db.refresh(product)
    assert product.id is not None
    assert product.current_stock == 10

@pytest.mark.parametrize("current_stock", [-1, -5])
def test_create_product_with_negative_current_stock(db, current_stock):
    product = Product(name="Produto Inválido", current_stock=current_stock, min_stock=0, max_stock=1)
    db.add(product)
    with pytest.raises(IntegrityError):
        db.commit()

@pytest.mark.parametrize("min_stock", [-1, -10])
def test_create_product_with_negative_min_stock(db, min_stock):
    product = Product(name="Produto Inválido 2", current_stock=0, min_stock=min_stock, max_stock=10)
    db.add(product)
    with pytest.raises(IntegrityError):
        db.commit()

@pytest.mark.parametrize("max_stock", [-1, -5])
def test_create_product_with_negative_max_stock(db, max_stock):
    product = Product(name="Produto Inválido 3", current_stock=0, min_stock=0, max_stock=max_stock)
    db.add(product)
    with pytest.raises(IntegrityError):
        db.commit()

def test_create_product_with_invalid_stock_relation(db):
    product = Product(name="Produto Estoque Ruim", current_stock=5, min_stock=10, max_stock=8)
    db.add(product)
    with pytest.raises(IntegrityError):
        db.commit()

# ========== TESTES DE SOLICITAÇÕES DE COMPRA ==========
def test_create_valid_purchase_request(db):
    email = f"user_{uuid4()}@example.com"
    user = User(email=email, hashed_password="pwd", role=UserRole.BUYER)
    product = Product(name="Produto Compra", current_stock=10, min_stock=2, max_stock=15)
    db.add_all([user, product])
    db.commit()
    db.refresh(user)
    db.refresh(product)

    pr = PurchaseRequest(product_id=product.id, quantity=3, requester_id=user.id, status=PRStatus.PENDING)
    db.add(pr)
    db.commit()
    db.refresh(pr)

    assert pr.id is not None
    assert pr.quantity == 3
    assert pr.status == PRStatus.PENDING

@pytest.mark.parametrize("quantity", [0, -1, -5])
def test_create_purchase_request_with_invalid_quantity(db, quantity):
    email = f"user_{uuid4()}@example.com"
    user = User(email=email, hashed_password="pwd", role=UserRole.BUYER)
    product = Product(name=f"Produto Falho {quantity}", current_stock=10, min_stock=2, max_stock=15)
    db.add_all([user, product])
    db.commit()
    db.refresh(user)
    db.refresh(product)

    pr = PurchaseRequest(product_id=product.id, quantity=quantity, requester_id=user.id)
    db.add(pr)
    with pytest.raises(IntegrityError):
        db.commit()

# ========== REGRAS EXTRAS DE NEGÓCIO ==========
def test_max_stock_greater_than_min_stock(db):
    product = Product(name="Produto Limite", current_stock=5, min_stock=5, max_stock=5)
    db.add(product)
    with pytest.raises(IntegrityError):
        db.commit()

def test_product_with_zero_min_stock_and_max_greater(db):
    product = Product(name="Zerado OK", current_stock=0, min_stock=0, max_stock=10)
    db.add(product)
    db.commit()
    db.refresh(product)
    assert product.id is not None

# ========== TESTE DE ENUMS ==========
def test_invalid_enum_role(db):
    email = f"user_{uuid4()}@example.com"
    user = User(email=email, hashed_password="pwd", role="admin")
    db.add(user)
    with pytest.raises(sqlalchemy.exc.DataError):
        db.commit()

def test_invalid_enum_status(db):
    email = f"user_{uuid4()}@example.com"
    user = User(email=email, hashed_password="pwd", role=UserRole.OPERATOR)
    product = Product(name="Produto Enum", current_stock=5, min_stock=1, max_stock=10)
    db.add_all([user, product])
    db.commit()
    db.refresh(user)
    db.refresh(product)

    pr = PurchaseRequest(product_id=product.id, quantity=2, requester_id=user.id, status="concluido")
    db.add(pr)
    with pytest.raises(sqlalchemy.exc.DataError):
        db.commit()

