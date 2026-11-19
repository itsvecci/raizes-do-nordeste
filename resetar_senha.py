
from getpass import getpass

from app.database import SessionLocal
from app import models
from app.security import gerar_hash_senha


db = SessionLocal()

try:
    usuario = db.query(models.Usuario).filter(
        models.Usuario.id == 3
    ).first()

    if not usuario:
        print("Usuário não encontrado.")

    elif usuario.perfil != "ADMIN":
        print("O usuário não possui perfil ADMIN.")

    else:
        nova_senha = getpass("Digite a nova senha: ")
        confirmar_senha = getpass("Confirme a nova senha: ")

        if not nova_senha:
            print("A senha não pode ficar vazia.")

        elif nova_senha != confirmar_senha:
            print("As senhas não conferem.")

        else:
            usuario.senha_hash = gerar_hash_senha(nova_senha)

            db.commit()

            print("Senha do administrador atualizada com sucesso!")

except Exception as erro:
    db.rollback()
    print("Erro ao atualizar a senha:", erro)

finally:
    db.close()
