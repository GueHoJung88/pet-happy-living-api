import os
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "Pet Happy Service"
    ENV : str = os.getenv("ENV", "dev")
    DEBUG : bool = os.getenv("DEBUG", True)

    # API KEY
    SEOUL_OPEN_API_KEY: str = os.getenv("SEOUL_OPEN_API_KEY", "sample")
    
    # SSH 정보
    SSH_HOST: str = os.getenv("SSH_HOST","ec2-52-79-101-221.ap-northeast-2.compute.amazonaws.com")
    SSH_PORT: int = os.getenv("SSH_PORT",22)
    SSH_USER: str = os.getenv("SSH_USER","ubuntu")
    PRIVATE_KEY_PATH: str = os.getenv("PRIVATE_KEY_PATH","./petple_db_server_key_pair.pem")

    # PostgreSQL 정보
    POSTGRES_URL: str = os.getenv("POSTGRES_URL", "localhost")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST","localhost")
    POSTGRES_LOCAL_PORT: int = os.getenv("POSTGRES_LOCAL_PORT",15432)
    POSTGRES_PORT: int = os.getenv("POSTGRES_PORT",5432)
    POSTGRES_DATABASE_NAME: str = os.getenv("POSTGRES_DATABASE_NAME","petple_service")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER","postgres")
    POSTGRES_PASS: str = os.getenv("POSTGRES_PASS","your_password")

    # Redis 정보
    REDIS_URL: str = os.getenv("REDIS_URL", "localhost")

    class Config:
        env_file = ".env"  # 환경 변수 파일 경로 # 기본값은 .env, 동적으로 override됨


# 성능을 위해 한번만 로드
@lru_cache()
def get_settings():
    # 1️⃣ ENV 환경 변수 먼저 확인
    current_env = os.getenv("ENV", "dev")

    # 2️⃣ 해당 ENV 값에 따라 .env 파일 선택
    env_file_path = f".env.{current_env}"

    # 3️⃣ 해당 env_file을 사용하여 Settings 인스턴스 생성
    return Settings(_env_file=env_file_path)
