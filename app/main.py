from sshtunnel import SSHTunnelForwarder
import psycopg2
from fastapi import FastAPI
from app.api import endpoints_router
from app.core.config import get_settings
from app.core.logging_config import logger

from contextlib import asynccontextmanager
from app.scheduler.jobs import setup_scheduler
from app.db.session import engine, Base


app = FastAPI(title="Pet Happy Recommendation API", version="0.1.0")
app.include_router(endpoints_router.router, prefix="/api/v1")
settings = get_settings()
tunnel = None

async def create_tables():
    """DB 테이블 자동 생성"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

scheduler = setup_scheduler()

@app.on_event("startup")
async def start_ssh_tunnel():
    logger.info(f"🚀 FastAPI 서버 시작 중...(settings.ENV = {settings.ENV})")
    scheduler.start()
    global tunnel
    if settings.ENV == "dev":
        tunnel = SSHTunnelForwarder(
            (settings.SSH_HOST, settings.SSH_PORT),
            ssh_username=settings.SSH_USER,
            ssh_private_key=settings.PRIVATE_KEY_PATH,
            remote_bind_address=(settings.POSTGRES_HOST, settings.POSTGRES_PORT),
            local_bind_address=("127.0.0.1", settings.POSTGRES_LOCAL_PORT)
        )
        tunnel.start()
    else:
        logger.info("✅ 운영 환경으로 SSH Tunnel은 비활성화됩니다.")
    await create_tables()

@app.on_event("shutdown")
def stop_ssh_tunnel():
    logger.info("🚀 FastAPI 서버 종료 중...")
    scheduler.shutdown()
    if tunnel:
        tunnel.stop()

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # 앱 시작
#     await create_tables()
#     scheduler.start()
#     print("🚀 FastAPI 앱이 시작되었습니다. 스케줄러가 활성화되었습니다.")
#     yield
#     # 앱 종료
#     scheduler.shutdown()
#     print("👋 FastAPI 앱이 종료됩니다. 스케줄러가 안전하게 종료되었습니다.")