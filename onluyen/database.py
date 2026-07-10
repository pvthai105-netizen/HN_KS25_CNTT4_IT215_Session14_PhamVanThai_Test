from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

Base = declarative_base()
DB_URL = "mysql+pymysql://root:123456$@localhost:3306/worldcup_db"
engine = create_engine(DB_URL)

LocalSession = sessionmaker(autoflush=False, autocommit=False, expire_on_commit=False, bind=engine)

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

