# =============================
# 데이터 수집 공통 모듈
# =============================
import asyncio
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert as pg_insert
from app.api.common.api_client import SeoulOpenAPIClient
from app.core.logging_config import logger


class DataCollector:
    """
    데이터 수집 공통 클래스
    다양한 외부 API에서 데이터를 수집하고 데이터베이스에 저장하는 기능 제공
    """
    
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.seoul_client = SeoulOpenAPIClient()
    
    
    async def save_to_database(
        self, 
        table_model, 
        data_list: List[Dict[str, Any]], 
        unique_field: str = "mgt_no"
    ) -> int:
        """
        데이터를 데이터베이스에 저장
        
        Args:
            table_model: SQLAlchemy 모델 클래스
            data_list: 저장할 데이터 리스트
            unique_field: 고유 필드명 (충돌 시 업데이트 기준)
            
        Returns:
            저장된 레코드 수
        """
        if not data_list:
            return 0
        
        saved_count = 0
        
        for data in data_list:
            try:
                # 모델 인스턴스 생성
                model_instance = table_model(**data)
                
                # Pydantic 스키마로 변환 (있는 경우)
                if hasattr(model_instance, 'dict'):
                    model_data = model_instance.dict(exclude_unset=True)
                else:
                    model_data = data
                
                # UPSERT 쿼리 생성
                stmt = pg_insert(table_model).values(**model_data)
                stmt = stmt.on_conflict_do_update(
                    index_elements=[unique_field],
                    set_=model_data
                )
                
                await self.db_session.execute(stmt)
                saved_count += 1
                
            except Exception as e:
                logger.error(f"Error saving data to database: {e}")
                continue
        
        await self.db_session.commit()
        logger.info(f"Successfully saved {saved_count} records to database")
        return saved_count
    
    async def collect_and_save(
        self, 
        collection_method, 
        table_model, 
        start: int = 1, 
        end: int = 5,
        unique_field: str = "mgt_no"
    ) -> Dict[str, Any]:
        """
        데이터 수집 및 저장을 한번에 수행
        
        Args:
            collection_method: 데이터 수집 메서드
            table_model: 저장할 테이블 모델
            start: 시작 인덱스
            end: 종료 인덱스
            unique_field: 고유 필드명
            
        Returns:
            수집 및 저장 결과
        """
        try:
            # 데이터 수집
            data_list = await collection_method(start, end)
            
            if not data_list:
                return {
                    "status": "warning",
                    "message": "No data collected",
                    "collected_count": 0,
                    "saved_count": 0
                }
            
            # 데이터베이스 저장
            saved_count = await self.save_to_database(table_model, data_list, unique_field)
            
            return {
                "status": "success",
                "message": f"Data collected and saved successfully",
                "collected_count": len(data_list),
                "saved_count": saved_count
            }
            
        except Exception as e:
            logger.error(f"Error in collect_and_save: {e}")
            return {
                "status": "error",
                "message": str(e),
                "collected_count": 0,
                "saved_count": 0
            }


class BatchDataCollector:
    """
    배치 데이터 수집 클래스
    여러 데이터 소스를 동시에 수집하는 기능 제공
    """
    
    def __init__(self, db_session: AsyncSession):
        self.collector = DataCollector(db_session)
    
    async def collect_all_pet_data(self, start: int = 1, end: int = 5) -> Dict[str, Any]:
        """
        모든 반려동물 관련 데이터 수집
        
        Args:
            start: 시작 인덱스
            end: 종료 인덱스
            
        Returns:
            수집 결과 요약
        """
        tasks = [
            self.collector.collect_and_save(
                self.collector.collect_pet_clinics,
                None,  # 테이블 모델은 실제 사용 시 지정
                start,
                end
            ),
            self.collector.collect_and_save(
                self.collector.collect_pet_shops,
                None,  # 테이블 모델은 실제 사용 시 지정
                start,
                end
            ),
            self.collector.collect_and_save(
                self.collector.collect_pet_parks,
                None,  # 테이블 모델은 실제 사용 시 지정
                start,
                end
            )
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        summary = {
            "total_tasks": len(tasks),
            "successful_tasks": 0,
            "failed_tasks": 0,
            "total_collected": 0,
            "total_saved": 0,
            "details": []
        }
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                summary["failed_tasks"] += 1
                summary["details"].append({
                    "task_index": i,
                    "status": "error",
                    "message": str(result)
                })
            else:
                summary["successful_tasks"] += 1
                summary["total_collected"] += result.get("collected_count", 0)
                summary["total_saved"] += result.get("saved_count", 0)
                summary["details"].append({
                    "task_index": i,
                    "status": result.get("status", "unknown"),
                    "message": result.get("message", ""),
                    "collected_count": result.get("collected_count", 0),
                    "saved_count": result.get("saved_count", 0)
                })
        
        return summary 