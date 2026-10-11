from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal
from app.core.departments import DEPARTMENTS
from app.core.security import hash_password
from app.models.department import Department, DepartmentStatus
from app.models.user import User, UserRole, UserStatus


def seed() -> None:
    db: Session = SessionLocal()
    try:
        for nome, descricao in DEPARTMENTS:
            exists = db.query(Department).filter(Department.nome == nome).first()
            if not exists:
                db.add(Department(nome=nome, descricao=descricao, estado=DepartmentStatus.ACTIVE))
                print(f"Departamento criado: {nome}")

        email = settings.SEED_ADMIN_EMAIL.lower()
        admin = db.query(User).filter(User.email == email).first()
        if not admin:
            admin = User(
                nome_completo="CEO Admin",
                email=email,
                password_hash=hash_password(settings.SEED_ADMIN_PASSWORD),
                password_changed_at=datetime.now(timezone.utc).replace(tzinfo=None),
                cargo="CEO",
                role=UserRole.CEO,
                estado=UserStatus.ACTIVE,
                foto=settings.DEFAULT_AVATAR,
            )
            db.add(admin)
            print(f"CEO Admin criado: {email}")
        else:
            print("CEO Admin já existe.")

        pca_email = settings.SEED_PCA_EMAIL.lower()
        pca = db.query(User).filter(User.email == pca_email).first()
        if not pca:
            pca = User(
                nome_completo=settings.SEED_PCA_NAME,
                email=pca_email,
                password_hash=hash_password(settings.SEED_PCA_PASSWORD),
                password_changed_at=datetime.now(timezone.utc).replace(tzinfo=None),
                cargo="Presidente do Conselho de Administração",
                role=UserRole.PCA,
                estado=UserStatus.ACTIVE,
                foto=settings.DEFAULT_AVATAR,
            )
            db.add(pca)
            print(f"PCA criado: {pca_email}")
        else:
            print("PCA já existe.")

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()