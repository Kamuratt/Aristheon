from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Union
from dotenv import load_dotenv
import os

# Carregar as variáveis de ambiente
load_dotenv()

# Recuperando o segredo da chave e algoritmo do arquivo .env
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))  # 15 minutos por padrão
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))  # Definindo 7 dias para o refresh token

# Contexto para criptografia de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para verificar a senha fornecida
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha fornecida corresponde ao hash armazenado.
    """
    return pwd_context.verify(plain_password, hashed_password)

# Função para criar o token de acesso (JWT)
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    """
    Cria um token JWT com um tempo de expiração configurado.
    O padrão é 15 minutos, mas pode ser alterado com expires_delta.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Função para criar o refresh token (JWT)
def create_refresh_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    """
    Cria um refresh token JWT com um tempo de expiração configurado.
    O padrão é 7 dias, mas pode ser alterado com expires_delta.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)  # Default: 7 dias para o refresh token
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Função para validar o token de acesso (JWT)
def verify_access_token(token: str) -> Union[dict, None]:
    """
    Valida o token JWT. Retorna o payload decodificado se for válido ou None se for inválido ou expirado.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Retorna o payload decodificado se for válido
    except JWTError:
        return None  # Se o token for inválido ou expirado
