from logging.config import fileConfig
from alembic import context
import os
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool
from database import Base, engine  # Usa o engine do seu arquivo database.py
from database import User, Product, PurchaseRequest, RefreshToken, AccessTokenBlacklist  # Importa suas models
from sqlalchemy.engine.url import URL

# Carregar variáveis de ambiente
load_dotenv()

# Carregar a URL do banco de dados diretamente do .env
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL não está definido no arquivo .env")

# Configura o URL do banco de dados para o Alembic
config = context.config
config.set_main_option("sqlalchemy.url", database_url)

# Configuração de logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Define o metadata para o autogenerate das migrações
target_metadata = Base.metadata  # Incluir a tabela AccessTokenBlacklist e todas as outras tabelas

def run_migrations_offline() -> None:
    """Executa migrações no modo offline."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Executa migrações no modo online."""
    connectable = engine  # Usa o engine já configurado no database.py

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# Decide se as migrações serão executadas no modo offline ou online
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
