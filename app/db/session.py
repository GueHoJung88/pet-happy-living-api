from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings
from sqlalchemy.ext.declarative import declarative_base

settings = get_settings()

DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASS}@{settings.POSTGRES_HOST}:{settings.POSTGRES_LOCAL_PORT}/{settings.POSTGRES_DATABASE_NAME}"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# SQLAlchemy 기본 베이스 클래스 생성
Base = declarative_base()

async def get_db():
    async with async_session() as session:
        yield session
