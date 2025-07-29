# =============================
# 공통 RESTful API 클라이언트 모듈
# =============================
import httpx
import asyncio
from typing import Dict, Any, Optional, List
from fastapi import HTTPException
from app.core.config import get_settings
from app.core.logging_config import logger

settings = get_settings()


class APIClient:
    """
    공통 RESTful API 클라이언트 클래스
    다양한 외부 API 호출을 위한 공통 인터페이스 제공
    """
    
    def __init__(self, base_url: str = "", timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session: Optional[httpx.AsyncClient] = None
    
    async def __aenter__(self):
        """비동기 컨텍스트 매니저 진입"""
        self.session = httpx.AsyncClient(
            timeout=self.timeout,
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """비동기 컨텍스트 매니저 종료"""
        if self.session:
            await self.session.aclose()
    
    async def _make_request(
        self, 
        method: str, 
        url: str, 
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> httpx.Response:
        """공통 HTTP 요청 메서드"""
        if not self.session:
            raise RuntimeError("APIClient must be used as async context manager")
        
        full_url = f"{self.base_url}{url}" if self.base_url else url
        
        try:
            response = await self.session.request(
                method=method,
                url=full_url,
                params=params,
                headers=headers,
                json=json_data,
                data=data
            )
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP Error {e.response.status_code}: {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except httpx.RequestError as e:
            logger.error(f"Request Error: {e}")
            raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")
    
    async def get(
        self, 
        url: str, 
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """GET 요청"""
        response = await self._make_request("GET", url, params=params, headers=headers)
        return response.json()
    
    async def post(
        self, 
        url: str, 
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """POST 요청"""
        response = await self._make_request("POST", url, json_data=json_data, data=data, headers=headers)
        return response.json()
    
    async def put(
        self, 
        url: str, 
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """PUT 요청"""
        response = await self._make_request("PUT", url, json_data=json_data, headers=headers)
        return response.json()
    
    async def delete(
        self, 
        url: str, 
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """DELETE 요청"""
        response = await self._make_request("DELETE", url, headers=headers)
        return response.json()

