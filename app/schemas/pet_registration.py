# =============================
# Pydantic 모델 정의 (행정구역별 반려동물등록 개체 수 현황)
# =============================
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PetRegistrationBase(BaseModel):
    """반려동물 등록 기본 스키마"""
    sido: str = Field(..., description="시도")
    sigungu: Optional[str] = Field(None, description="시군구")
    dog_registration_total: int = Field(..., ge=0, description="개등록 누계")
    cat_registration_total: int = Field(..., ge=0, description="고양이등록 누계")
    total_registration: int = Field(..., ge=0, description="총 등록 누계")
    data_year: Optional[str] = Field(None, description="데이터 기준년도")
    data_month: Optional[str] = Field(None, description="데이터 기준월")
    update_date: Optional[str] = Field(None, description="데이터 갱신일자")


class PetRegistrationCreate(PetRegistrationBase):
    """반려동물 등록 생성 스키마"""
    pass


class PetRegistrationUpdate(BaseModel):
    """반려동물 등록 업데이트 스키마"""
    sido: Optional[str] = Field(None, description="시도")
    sigungu: Optional[str] = Field(None, description="시군구")
    dog_registration_total: Optional[int] = Field(None, ge=0, description="개등록 누계")
    cat_registration_total: Optional[int] = Field(None, ge=0, description="고양이등록 누계")
    total_registration: Optional[int] = Field(None, ge=0, description="총 등록 누계")
    data_year: Optional[str] = Field(None, description="데이터 기준년도")
    data_month: Optional[str] = Field(None, description="데이터 기준월")
    update_date: Optional[str] = Field(None, description="데이터 갱신일자")


class PetRegistrationRead(PetRegistrationBase):
    """반려동물 등록 조회 스키마"""
    id: int = Field(..., description="고유 식별자")
    full_address: str = Field(..., description="전체 주소")
    dog_percentage: float = Field(..., description="개 등록 비율 (%)")
    cat_percentage: float = Field(..., description="고양이 등록 비율 (%)")
    created_at: datetime = Field(..., description="데이터 생성 시각")
    updated_at: Optional[datetime] = Field(None, description="데이터 수정 시각")

    class Config:
        orm_mode = True
        from_attributes = True


class PetRegistrationSummary(BaseModel):
    """반려동물 등록 요약 스키마"""
    total_regions: int = Field(..., description="총 행정구역 수")
    total_dogs: int = Field(..., description="총 개 등록 수")
    total_cats: int = Field(..., description="총 고양이 등록 수")
    total_pets: int = Field(..., description="총 반려동물 등록 수")
    average_dog_percentage: float = Field(..., description="평균 개 등록 비율 (%)")
    average_cat_percentage: float = Field(..., description="평균 고양이 등록 비율 (%)")
    top_regions: list[dict] = Field(..., description="등록 수 상위 지역")


class PetRegistrationStats(BaseModel):
    """반려동물 등록 통계 스키마"""
    sido_stats: dict[str, dict] = Field(..., description="시도별 통계")
    sigungu_stats: dict[str, dict] = Field(..., description="시군구별 통계")
    total_stats: dict = Field(..., description="전체 통계")


# API 응답을 위한 스키마
class PetRegistrationResponse(BaseModel):
    """API 응답 스키마"""
    currentCount: int = Field(..., description="현재 페이지 데이터 수")
    data: list[PetRegistrationRead] = Field(..., description="반려동물 등록 데이터")
    matchCount: int = Field(..., description="검색 조건에 맞는 데이터 수")
    page: int = Field(..., description="현재 페이지")
    perPage: int = Field(..., description="페이지당 데이터 수")
    totalCount: int = Field(..., description="전체 데이터 수") 