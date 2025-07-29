# =============================
# Alembic 환경 설정
# =============================

import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

# 이 파일을 실행할 때 Python 경로에 프로젝트 루트를 추가
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# 모델들을 import (Alembic이 자동으로 감지할 수 있도록)
from app.models.weather import Base as WeatherBase
from app.models.users import Base as UsersBase
from app.models.pet_clinic import Base as PetClinicBase
from app.models.pet_registration import Base as PetRegistrationBase
from app.core.config import get_settings

# Alembic 설정 파일에서 설정을 가져옴
config = context.config

# 설정 파일이 있으면 로깅 설정을 해석
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 모델 메타데이터를 설정에 추가
target_metadata = None

# 모든 모델의 Base 클래스를 하나로 통합
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# 모든 모델을 import하여 메타데이터에 등록
import app.models.users
import app.models.pet_clinic
import app.models.pet_registration
import app.models.weather

# 메타데이터 설정
target_metadata = Base.metadata

def get_url():
    """데이터베이스 URL을 환경 변수에서 가져옴"""
    settings = get_settings()
    return f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASS}@{settings.POSTGRES_HOST}:{settings.POSTGRES_LOCAL_PORT}/{settings.POSTGRES_DATABASE_NAME}"

def run_migrations_offline() -> None:
    """오프라인 모드에서 마이그레이션을 실행합니다.

    이 함수는 'alembic offline' 명령으로 호출됩니다.
    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """마이그레이션을 실행합니다."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """비동기 마이그레이션을 실행합니다."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=get_url(),
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """온라인 모드에서 마이그레이션을 실행합니다.

    이 함수는 'alembic online' 명령으로 호출됩니다.
    """
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online() 