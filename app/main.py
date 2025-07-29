from sshtunnel import SSHTunnelForwarder
import psycopg2
from fastapi import FastAPI
from app.api import endpoints_router
from app.core.config import get_settings
from app.core.logging_config import logger


app = FastAPI(title="Pet Happy Recommendation API", version="0.1.0")
app.include_router(endpoints_router.router, prefix="/api/v1")
settings = get_settings()
tunnel = None

@app.on_event("startup")
def start_ssh_tunnel():
    logger.info(f"🚀 FastAPI 서버 시작 중...(settings.ENV = {settings.ENV})")
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

@app.on_event("shutdown")
def stop_ssh_tunnel():
    logger.info("🚀 FastAPI 서버 종료 중...")
    if tunnel:
        tunnel.stop()
