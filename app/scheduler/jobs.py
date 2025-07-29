# app/scheduler/jobs.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.db.session import async_session
from app.services.weather_service import crawl_naver_weather
from app.db.crud import create_weather_data

async def scheduled_weather_crawl_job():
    """
    스케줄러에 의해 주기적으로 실행될 작업.
    날씨를 크롤링하고, 그 결과를 DB에 저장합니다.
    """
    weather_info = await crawl_naver_weather(location="서울")
    
    if not weather_info:
        print("크롤링된 날씨 정보가 없어 DB 저장을 건너뜁니다.")
        return

    async with async_session() as db:
        await create_weather_data(db=db, weather_info=weather_info)
        print(f"✅ 성공: '서울'의 날씨 정보를 데이터베이스에 저장했습니다.")

# 스케줄러 인스턴스 생성
scheduler = AsyncIOScheduler()

def setup_scheduler():
    # 매일 아침 8시에 작업 실행
    scheduler.add_job(scheduled_weather_crawl_job, CronTrigger(hour=18, minute=23))
    # 테스트용 (1분마다)
    # scheduler.add_job(scheduled_weather_crawl_job, 'interval', minutes=1)
    return scheduler