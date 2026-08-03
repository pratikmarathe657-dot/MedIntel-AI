from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# =====================================
# DATABASE CONFIGURATION
# =====================================

DATABASE_URL = "sqlite:///medtrace.db"

engine = create_engine(
    DATABASE_URL,
    echo=False
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# =====================================
# DATABASE SESSION
# =====================================

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()