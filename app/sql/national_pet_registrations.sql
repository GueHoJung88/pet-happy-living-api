-- =============================
-- 행정구역별 반려동물등록 개체 수 현황 테이블 생성
-- =============================

CREATE TABLE IF NOT EXISTS national_pet_registrations (
    id SERIAL PRIMARY KEY,                           -- 고유 식별자
    sido VARCHAR(50) NOT NULL,                       -- 시도
    sigungu VARCHAR(50),                             -- 시군구
    dog_registration_total INTEGER NOT NULL DEFAULT 0, -- 개등록 누계
    cat_registration_total INTEGER NOT NULL DEFAULT 0, -- 고양이등록 누계
    total_registration INTEGER NOT NULL DEFAULT 0,     -- 총 등록 누계
    data_year VARCHAR(4),                             -- 데이터 기준년도
    data_month VARCHAR(2),                            -- 데이터 기준월
    update_date VARCHAR(10),                          -- 데이터 갱신일자
    created_at TIMESTAMPTZ DEFAULT NOW(),             -- 데이터 생성 시각
    updated_at TIMESTAMPTZ                            -- 데이터 수정 시각
);

-- 시도와 시군구 조합으로 고유성 보장하는 인덱스
CREATE UNIQUE INDEX IF NOT EXISTS idx_sido_sigungu_unique 
ON national_pet_registrations(sido, sigungu);

-- 시도별 검색을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_sido 
ON national_pet_registrations(sido);

-- 시군구별 검색을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_sigungu 
ON national_pet_registrations(sigungu);

-- 총 등록 수 기준 정렬을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_total_registration 
ON national_pet_registrations(total_registration DESC);

-- 개 등록 수 기준 정렬을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_dog_registration 
ON national_pet_registrations(dog_registration_total DESC);

-- 고양이 등록 수 기준 정렬을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_cat_registration 
ON national_pet_registrations(cat_registration_total DESC);

-- 생성 시각 기준 정렬을 위한 인덱스
CREATE INDEX IF NOT EXISTS idx_created_at 
ON national_pet_registrations(created_at DESC);

-- 테이블 코멘트 추가
COMMENT ON TABLE national_pet_registrations IS '행정구역별 반려동물등록 개체 수 현황';
COMMENT ON COLUMN national_pet_registrations.id IS '고유 식별자';
COMMENT ON COLUMN national_pet_registrations.sido IS '시도';
COMMENT ON COLUMN national_pet_registrations.sigungu IS '시군구';
COMMENT ON COLUMN national_pet_registrations.dog_registration_total IS '개등록 누계';
COMMENT ON COLUMN national_pet_registrations.cat_registration_total IS '고양이등록 누계';
COMMENT ON COLUMN national_pet_registrations.total_registration IS '총 등록 누계';
COMMENT ON COLUMN national_pet_registrations.data_year IS '데이터 기준년도';
COMMENT ON COLUMN national_pet_registrations.data_month IS '데이터 기준월';
COMMENT ON COLUMN national_pet_registrations.update_date IS '데이터 갱신일자';
COMMENT ON COLUMN national_pet_registrations.created_at IS '데이터 생성 시각';
COMMENT ON COLUMN national_pet_registrations.updated_at IS '데이터 수정 시각';

-- 샘플 데이터 삽입 (서울시 전체)
INSERT INTO national_pet_registrations (sido, sigungu, dog_registration_total, cat_registration_total, total_registration, data_year, data_month, update_date) 
VALUES ('서울', NULL, 537884, 7278, 545162, '2024', '01', '2024-01-15')
ON CONFLICT (sido, sigungu) DO UPDATE SET
    dog_registration_total = EXCLUDED.dog_registration_total,
    cat_registration_total = EXCLUDED.cat_registration_total,
    total_registration = EXCLUDED.total_registration,
    data_year = EXCLUDED.data_year,
    data_month = EXCLUDED.data_month,
    update_date = EXCLUDED.update_date,
    updated_at = NOW();

-- 샘플 데이터 삽입 (강남구)
INSERT INTO national_pet_registrations (sido, sigungu, dog_registration_total, cat_registration_total, total_registration, data_year, data_month, update_date) 
VALUES ('서울특별시', '강남구', 34402, 441, 34843, '2024', '01', '2024-01-15')
ON CONFLICT (sido, sigungu) DO UPDATE SET
    dog_registration_total = EXCLUDED.dog_registration_total,
    cat_registration_total = EXCLUDED.cat_registration_total,
    total_registration = EXCLUDED.total_registration,
    data_year = EXCLUDED.data_year,
    data_month = EXCLUDED.data_month,
    update_date = EXCLUDED.update_date,
    updated_at = NOW();

-- 샘플 데이터 삽입 (강동구)
INSERT INTO national_pet_registrations (sido, sigungu, dog_registration_total, cat_registration_total, total_registration, data_year, data_month, update_date) 
VALUES ('서울특별시', '강동구', 25292, 223, 25515, '2024', '01', '2024-01-15')
ON CONFLICT (sido, sigungu) DO UPDATE SET
    dog_registration_total = EXCLUDED.dog_registration_total,
    cat_registration_total = EXCLUDED.cat_registration_total,
    total_registration = EXCLUDED.total_registration,
    data_year = EXCLUDED.data_year,
    data_month = EXCLUDED.data_month,
    update_date = EXCLUDED.update_date,
    updated_at = NOW(); 