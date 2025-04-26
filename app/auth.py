import os
from datetime import datetime, timedelta
from uuid import uuid4

from dotenv import load_dotenv
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database import User, RefreshToken, AccessTokenBlacklist

# ----- Carrega variáveis do ambiente -----
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# ----- Configuração de criptografia -----
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ------------------------------------------------------
# ------------------ Funções de senha ------------------
# ------------------------------------------------------

def get_password_hash(password: str) -> str:
    """Gera o hash da senha usando bcrypt + salt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha fornecida corresponde ao hash armazenado."""
    return pwd_context.verify(plain_password, hashed_password)

# ------------------------------------------------------
# ------------------ Autenticação ----------------------
# ------------------------------------------------------

def authenticate_user(db: Session, email: str, password: str) -> User | None:
    """Autentica o usuário:
    - Busca o email.
    - Verifica a senha.
    Retorna o usuário ou None."""
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

# ------------------------------------------------------
# ------------------- Funções de Tokens ----------------
# ------------------------------------------------------

def _create_token(
    sub: str,
    expires_delta: timedelta,
    token_type: str,
    role: str = None,
    jti: str = None
) -> str:
    """Gera um token JWT:
    - sub = subject (id do usuário).
    - exp = expiração.
    - type = access ou refresh.
    - role = papel do usuário (somente para access token).
    - jti = ID único do refresh token."""
    now = datetime.utcnow()
    payload = {
        "sub": sub,
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
    }
    if role and token_type == "access":
        payload["role"] = role
    if token_type == "refresh":
        payload["jti"] = jti or str(uuid4())

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_access_token(user_id: int, role: str) -> str:
    """Gera um access token para o usuário."""
    return _create_token(
        sub=str(user_id),
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        token_type="access",
        role=role
    )

def create_refresh_token(db: Session, user_id: int) -> str:
    """Gera um refresh token e salva no banco."""
    jti = str(uuid4())
    expires_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    db_token = RefreshToken(
        user_id=user_id,
        jti=jti,
        expires_at=expires_at
    )
    db.add(db_token)
    db.commit()

    return _create_token(
        sub=str(user_id),
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        token_type="refresh",
        jti=jti
    )

# ------------------------------------------------------
# ------------------- Funções de Blacklist -------------
# ------------------------------------------------------

def revoke_refresh_token(db: Session, jti: str) -> None:
    """Revoga um refresh token, adicionando-o à blacklist."""
    db_token = AccessTokenBlacklist(jti=jti, revoked_at=datetime.utcnow())
    db.add(db_token)
    db.commit()

def is_token_revoked(db: Session, jti: str) -> bool:
    """Verifica se o refresh token está na blacklist."""
    db_token = db.query(AccessTokenBlacklist).filter(AccessTokenBlacklist.jti == jti).first()
    return db_token is not None

# ------------------------------------------------------
# ------------------- Verificação de Tokens ------------
# ------------------------------------------------------

def verify_token(db: Session, token: str, token_type: str = "access") -> dict:
    """Verifica a validade do token:
    - Access token: verifica assinatura e expiração.
    - Refresh token: consulta o banco para verificar validade.
    Retorna o payload ou levanta JWTError."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise JWTError("Invalid token or signature.")

    if payload.get("type") != token_type:
        raise JWTError(f"Invalid token type: {payload.get('type')}")

    if token_type == "refresh":
        jti = payload.get("jti")
        user_id = int(payload["sub"])

        if is_token_revoked(db, jti):
            raise JWTError("Refresh token has been revoked.")

        db_token = db.query(RefreshToken).filter_by(jti=jti, user_id=user_id).first()

        if not db_token:
            raise JWTError("Refresh token not found in database.")
        if db_token.revoked:
            raise JWTError("Refresh token revoked.")
        if db_token.expires_at < datetime.utcnow():
            raise JWTError("Refresh token expired.")

    return payload
