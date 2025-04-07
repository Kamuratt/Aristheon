from sqlalchemy.orm import Session
from crud import create_user, delete_user
from crud import update_user, get_user_by_id, get_user_by_email
from database import SessionLocal


 # Assumindo que a função create_user está correta em "crud"
from database import SessionLocal  # Importando a sessão do banco de dados de database.py

# Criando a sessão com o banco de dados
db: Session = SessionLocal()  # Isso deve ser do tipo Session agora
"""
try:
    # Dados do novo usuário
    email = "exemplo@dominio.com"
    password = "senhaSegura123"
    role = "manager"  # Ou "operator", "buyer", dependendo do caso

    # Criando o usuário diretamente
    new_user = create_user(db=db, email=email, password=password, role=role)

    # Exibindo a confirmação da criação
    print(f"Usuário criado: {new_user.email} com o papel de {new_user.role}")

finally:
    db.close()  # Sempre feche a sessão depois de usá-la
"""
"""
try:
    user_id = 7
    delete_user(db, user_id=user_id)
finally:
    db.close()
"""    
"""
try:
    user_id = 9 # Coloque aqui o ID do usuário que deseja editar

    # Novos dados para o usuário
    new_email = "novoemail@dominio.com"
    new_role = "operator"
    new_password = "novasenha456"

    # Atualiza o usuário
    updated_user = update_user(
        db,
        user_id=user_id,
        email=new_email,
        role=new_role,
        password=new_password
    )

    if updated_user:
        print(f"Usuário atualizado com sucesso:")
        print(f"ID: {updated_user.id}")
        print(f"Email: {updated_user.email}")
        print(f"Role: {updated_user.role}")
    else:
        print("Usuário não encontrado.")

finally:
    db.close()
"""
"""
try:
    user_id = 9  # Coloque o ID que quer buscar
    user = get_user_by_id(db, user_id)

    if user:
        print("Usuário encontrado:")
        print(f"ID: {user.id}")
        print(f"Email: {user.email}")
        print(f"Role: {user.role}")
    else:
        print("Usuário não encontrado.")

finally:
    db.close()
"""
"""
try:
    email = "novoemail@dominio.com"  # Use o e-mail que quiser buscar
    user = get_user_by_email(db, email)

    if user:
        print("Usuário encontrado:")
        print(f"ID: {user.id}")
        print(f"Email: {user.email}")
        print(f"Role: {user.role}")
    else:
        print("Usuário não encontrado.")

finally:
    db.close()
"""