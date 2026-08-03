from sqlalchemy.orm import Session

from database import SessionLocal
from models import User


# =====================================
# REGISTER
# =====================================

def register_user(username, password):

    db: Session = SessionLocal()

    try:

        existing_user = db.query(User).filter(
            User.username == username
        ).first()

        if existing_user:
            return False

        new_user = User(
            username=username,
            password=password
        )

        db.add(new_user)
        db.commit()

        return True

    finally:

        db.close()


# =====================================
# LOGIN
# =====================================

def login_user(username, password):

    db: Session = SessionLocal()

    try:

        user = db.query(User).filter(
            User.username == username,
            User.password == password
        ).first()

        if user:
            return True

        return False

    finally:

        db.close()