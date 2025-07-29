# =============================
# 테이블 정의 (행정구역별 반려동물등록 개체 수 현황)
# =============================

from sqlalchemy import Column, String, Integer, DateTime, func, Text, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

# SQLAlchemy 기본 베이스 클래스 생성
Base = declarative_base()


class PetRegistration(Base):
    __tablename__ = "national_pet_registrations"

    # 기본 키 (시도 + 시군구 조합으로 고유 식별)
    id = Column(Integer, primary_key=True, autoincrement=True, comment="고유 식별자")
    
    # 행정구역 정보
    sido = Column(String(50), nullable=False, comment="시도")
    sigungu = Column(String(50), nullable=True, comment="시군구")
    
    # 등록 현황 데이터
    dog_registration_total = Column(Integer, nullable=False, default=0, comment="개등록 누계")
    cat_registration_total = Column(Integer, nullable=False, default=0, comment="고양이등록 누계")
    total_registration = Column(Integer, nullable=False, default=0, comment="총 등록 누계")
    
    # 메타데이터
    data_year = Column(String(4), nullable=True, comment="데이터 기준년도")
    data_month = Column(String(2), nullable=True, comment="데이터 기준월")
    update_date = Column(String(10), nullable=True, comment="데이터 갱신일자")
    
    # 시스템 필드
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="데이터 생성 시각")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="데이터 수정 시각")
    
    # 복합 인덱스를 위한 고유 제약 조건
    __table_args__ = (
        # 시도와 시군구 조합으로 고유성 보장
        UniqueConstraint('sido', 'sigungu', name='uq_sido_sigungu'),
    )
    
    def __repr__(self):
        return f"<PetRegistration(sido='{self.sido}', sigungu='{self.sigungu}', total={self.total_registration})>"
    
    @property
    def full_address(self):
        """전체 주소 반환"""
        if self.sigungu:
            return f"{self.sido} {self.sigungu}"
        return self.sido
    
    @property
    def dog_percentage(self):
        """개 등록 비율 계산"""
        if self.total_registration > 0:
            return round((self.dog_registration_total / self.total_registration) * 100, 2)
        return 0.0
    
    @property
    def cat_percentage(self):
        """고양이 등록 비율 계산"""
        if self.total_registration > 0:
            return round((self.cat_registration_total / self.total_registration) * 100, 2)
        return 0.0 