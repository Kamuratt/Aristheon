from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import SessionLocal, User
from app.utils import verify_password, create_access_token, create_refresh_token  # Adicionamos create_refresh_token
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta

router = APIRouter()

# Definindo o modelo de dados para a requisição de login
class LoginRequest(BaseModel):
    email: str
    password: str

# Definindo o modelo de resposta para o login
class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str  # Agora incluímos o refresh token na resposta
    token_type: str
    access_token_expires_in: int  # Tempo de expiração do token
    user_id: int
    email: str

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Instanciando o OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Rota de login
@router.post("/login", response_model=LoginResponse)
async def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    # 1. Verifica se o usuário existe no banco de dados
    user = db.query(User).filter(User.email == login_request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos"
        )

    # 2. Verifica se a senha fornecida é a mesma que o hash armazenado
    if not verify_password(login_request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos"
        )

    # 3. Gera o token de acesso e o refresh token
    access_token = create_access_token(data={"sub": user.email, "id": user.id})
    refresh_token = create_refresh_token(data={"sub": user.email, "id": user.id})  # Novo refresh token

    # 4. Retorna os tokens e os dados do usuário
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,  # Retorna o refresh token
        "token_type": "bearer",
        "access_token_expires_in": 15,  # Aqui, o token expira em 15 minutos
        "user_id": user.id,  # ID do usuário para ser usado no cliente
        "email": user.email,  # Email do usuário (se necessário)
    }
