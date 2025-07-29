import httpx
from bs4 import BeautifulSoup
import datetime

async def crawl_naver_weather(location: str = "서울") -> dict:
    """
    네이버 날씨를 크롤링하여 딕셔너리로 반환합니다.
    """
    print(f"[{datetime.datetime.now()}] - ☁️ '{location}' 날씨 정보 크롤링을 시작합니다.")
    url = f"https://search.naver.com/search.naver?query={location}+날씨"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
        except httpx.RequestError as e:
            print(f"오류: 네이버 날씨 요청 실패 - {e}")
            return {}

    soup = BeautifulSoup(response.text, "html.parser")

    try:
        current_temp = soup.select_one("div.temperature_text > strong").text.strip().replace('현재 온도', '')
        weather_status = soup.select_one("div.weather_main > i > span.blind").text.strip()
        air_quality_tag = soup.select_one("a.air_area > div.text_area > span.text")
        air_quality = air_quality_tag.text.strip() if air_quality_tag else "정보 없음"
        
        return {
            "location": location,
            "current_temp": current_temp,
            "weather_status": weather_status,
            "air_quality": air_quality
        }
    except AttributeError:
        print("오류: 날씨 정보 파싱 실패. 페이지 구조가 변경되었을 수 있습니다.")
        return {}