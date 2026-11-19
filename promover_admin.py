from app.database import SessionLocal
from app import models

db = SessionLocal()

try:
    email = input("Digite o e-mail do usuario de teste: ")

    usuario = db.query(models.Usuario).filter(
        models.Usuario.email == email
    ).first()

    if usuario:
        usuario.perfil = "ADMIN"
        db.commit()
        print("Usuario atualizado para ADMIN!")
    else:
        print("Usuario nao encontrado.")

finally:
    db.close()
