# app/__init__.py

from .auth import (
    get_password_hash,
    verify_password,
    authenticate_user,
    create_access_token,
    create_refresh_token,
    revoke_refresh_token,
    is_token_revoked,
    verify_token,
)

from .utils import (
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_access_token,
)

from .login import router as login_router
from .database import User, Product, PurchaseRequest, SessionLocal, engine, UserRole, PRStatus
from .crud import (
    create_user,
    get_user_by_id,
    get_user_by_email,
    get_all_users,
    update_user_password,
    update_user,
    delete_user,
    create_product,
    get_product_by_id,
    get_all_products,
    update_product,
    delete_product,
    create_purchase_request,
    get_purchase_request_by_id,
    get_purchase_requests_by_user,
    get_all_purchase_requests,
    update_purchase_request_status,
    delete_purchase_request,
)

# Funções adicionais podem ser importadas conforme necessidade

