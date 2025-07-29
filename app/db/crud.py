from app.models.users import User
from sqlalchemy.future import select
from app.models.weather import WeatherData
from sqlalchemy.ext.asyncio import AsyncSession

async def get_pet_by_id(db, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def create_weather_data(db: AsyncSession, weather_info: dict):
    """
    크롤링한 날씨 정보를 DB에 저장합니다.
    """
    new_weather_data = WeatherData(
        location=weather_info.get("location"),
        current_temp=weather_info.get("current_temp"),
        weather_status=weather_info.get("weather_status"),
        air_quality=weather_info.get("air_quality"),
    )
    db.add(new_weather_data)
    await db.commit()
    await db.refresh(new_weather_data)
    return new_weather_data