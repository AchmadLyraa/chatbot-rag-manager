from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import psycopg2.pool
from app.core.config import settings

# SQLAlchemy — untuk ORM (file manager)
engine = create_engine(settings.database_url, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# psycopg2 pool — untuk raw query pgvector (RAG)
pg_pool = psycopg2.pool.ThreadedConnectionPool(
    minconn=1,
    maxconn=10,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    dbname=settings.DB_NAME,
)

def get_connection():
    return pg_pool.getconn()

def release_connection(conn):
    pg_pool.putconn(conn)
