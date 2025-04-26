from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import SessionLocal, Base, engine, User
from app.login import router as login_router
from app.utils import verify_access_token
from pydantic import BaseModel

# Inicializando o app FastAPI
app = FastAPI()

# Incluindo as rotas do login
app.include_router(login_router)

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Definindo o modelo de dados para uma rota protegida
class UserResponse(BaseModel):
    id: int
    email: str

# Instanciando o OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Dependência para validar o token de acesso
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
        )
    user = db.query(User).filter(User.id == payload["id"]).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado",
        )
    return user

# Rota de exemplo protegida que requer autenticação
@app.get("/protected", response_model=UserResponse)
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email}

# Verifica o estado do servidor (ping)
@app.get("/ping")
async def ping():
    return {"message": "pong"}

# Inicialização do banco de dados (só uma vez)
Base.metadata.create_all(bind=engine)
