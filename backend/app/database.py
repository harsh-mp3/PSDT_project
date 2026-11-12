import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
load_dotenv()
DB_URL=os.getenv('DATABASE_URL','sqlite:///./data/governance.db')
if DB_URL.startswith('sqlite:///'):
    Path(DB_URL.replace('sqlite:///','',1)).parent.mkdir(parents=True,exist_ok=True)
elif DB_URL.startswith('postgres://'):
    DB_URL='postgresql+psycopg://'+DB_URL.removeprefix('postgres://')
elif DB_URL.startswith('postgresql://'):
    DB_URL='postgresql+psycopg://'+DB_URL.removeprefix('postgresql://')
engine=create_engine(DB_URL,connect_args={'check_same_thread':False} if DB_URL.startswith('sqlite') else {})
SessionLocal=sessionmaker(bind=engine,autoflush=False,autocommit=False)
class Base(DeclarativeBase): pass
def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()
