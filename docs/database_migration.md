# 🗄️ FastAPI 데이터베이스 마이그레이션 가이드

## 📋 목차

1. [개요](#개요)
2. [설치 및 설정](#설치-및-설정)
3. [기본 사용법](#기본-사용법)
4. [고급 사용법](#고급-사용법)
5. [문제 해결](#문제-해결)
6. [모범 사례](#모범-사례)

## 🎯 개요

이 프로젝트는 **Alembic**을 사용하여 데이터베이스 마이그레이션을 관리합니다. Alembic은 SQLAlchemy의 공식 마이그레이션 도구로, 데이터베이스 스키마 변경을 버전 관리하고 안전하게 적용할 수 있습니다.

### 🔧 주요 특징

- **버전 관리**: 데이터베이스 변경사항을 Git과 유사하게 버전 관리
- **자동 감지**: SQLAlchemy 모델 변경사항을 자동으로 감지
- **롤백 지원**: 이전 버전으로 안전하게 되돌리기 가능
- **팀 협업**: 여러 개발자가 동시에 작업할 때 충돌 방지

## 🚀 설치 및 설정

### 1. 의존성 설치

```bash
pip install alembic
```

### 2. 프로젝트 구조

```
pet-happy-living-api/
├── alembic/
│   ├── versions/          # 마이그레이션 파일들
│   ├── env.py            # Alembic 환경 설정
│   └── script.py.mako    # 마이그레이션 템플릿
├── app/
│   ├── models/           # SQLAlchemy 모델들
│   └── ...
├── alembic.ini          # Alembic 설정 파일
├── migrate.sh           # 마이그레이션 실행 스크립트
└── scripts/
    └── migrate.py       # Python 마이그레이션 도구
```

## 📖 기본 사용법

### 1. 마이그레이션 초기화

```bash
# Docker 환경
./migrate.sh init

# 로컬 환경
python scripts/migrate.py init
```

### 2. 새 마이그레이션 생성

```bash
# Docker 환경
./migrate.sh create "Add pet registration table"

# 로컬 환경
python scripts/migrate.py create "Add pet registration table"
```

### 3. 데이터베이스 업그레이드

```bash
# Docker 환경
./migrate.sh upgrade

# 로컬 환경
python scripts/migrate.py upgrade
```

### 4. 마이그레이션 상태 확인

```bash
# 현재 버전 확인
./migrate.sh current

# 마이그레이션 히스토리 확인
./migrate.sh history

# 대기 중인 마이그레이션 확인
./migrate.sh show
```

## 🔧 고급 사용법

### 1. 수동 마이그레이션 생성

자동 감지가 어려운 복잡한 변경사항의 경우:

```bash
# 마이그레이션 파일만 생성 (자동 감지 없음)
alembic revision -m "Complex data migration"
```

생성된 파일을 수정하여 원하는 SQL을 작성:

```python
def upgrade() -> None:
    # 복잡한 데이터 마이그레이션 로직
    op.execute("""
        UPDATE users 
        SET email = LOWER(email) 
        WHERE email != LOWER(email)
    """)

def downgrade() -> None:
    # 롤백 로직
    pass
```

### 2. 특정 버전으로 다운그레이드

```bash
# 이전 버전으로 되돌리기
./migrate.sh downgrade -1

# 특정 버전으로 되돌리기
./migrate.sh downgrade abc123def456
```

### 3. 데이터베이스 초기화

⚠️ **주의**: 이 작업은 모든 데이터를 삭제합니다!

```bash
./migrate.sh reset
```

### 4. 마이그레이션 파일 편집

생성된 마이그레이션 파일은 `alembic/versions/` 디렉토리에 저장됩니다:

```python
"""Add pet registration table

Revision ID: abc123def456
Revises: 
Create Date: 2024-01-15 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'abc123def456'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # 업그레이드 로직
    op.create_table('national_pet_registrations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('sido', sa.String(length=50), nullable=False),
        # ... 기타 컬럼들
    )

def downgrade() -> None:
    # 다운그레이드 로직
    op.drop_table('national_pet_registrations')
```

## 🛠️ 문제 해결

### 1. 마이그레이션 충돌 해결

여러 개발자가 동시에 마이그레이션을 생성할 때 발생할 수 있습니다:

```bash
# 충돌 확인
./migrate.sh show

# 충돌 해결 후 병합
alembic merge heads -m "Merge multiple heads"
```

### 2. 마이그레이션 실패 시 복구

```bash
# 실패한 마이그레이션 확인
./migrate.sh current

# 이전 버전으로 되돌리기
./migrate.sh downgrade -1

# 마이그레이션 파일 수정 후 다시 시도
./migrate.sh upgrade
```

### 3. 데이터베이스 연결 문제

```bash
# 환경 변수 확인
echo $POSTGRES_HOST
echo $POSTGRES_PORT
echo $POSTGRES_DATABASE_NAME

# 연결 테스트
docker exec -it pet-happy-api psql -U $POSTGRES_USER -d $POSTGRES_DATABASE_NAME -c "SELECT 1;"
```

### 4. 자동 감지 문제

모델이 감지되지 않는 경우:

1. **모델 import 확인**: `alembic/env.py`에서 모든 모델이 import되었는지 확인
2. **메타데이터 확인**: `target_metadata`가 올바르게 설정되었는지 확인
3. **Base 클래스 확인**: 모든 모델이 동일한 Base 클래스를 사용하는지 확인

## 📋 모범 사례

### 1. 마이그레이션 네이밍

```bash
# 좋은 예시
./migrate.sh create "Add user email verification"
./migrate.sh create "Update pet clinic coordinates"
./migrate.sh create "Add indexes for performance"

# 피해야 할 예시
./migrate.sh create "Update"
./migrate.sh create "Fix bug"
```

### 2. 마이그레이션 파일 구조

```python
def upgrade() -> None:
    # 1. 테이블 생성
    op.create_table(...)
    
    # 2. 인덱스 생성
    op.create_index(...)
    
    # 3. 데이터 마이그레이션
    op.execute("UPDATE ...")
    
    # 4. 제약 조건 추가
    op.create_unique_constraint(...)

def downgrade() -> None:
    # 역순으로 실행
    op.drop_constraint(...)
    op.execute("UPDATE ...")
    op.drop_index(...)
    op.drop_table(...)
```

### 3. 데이터 마이그레이션

```python
def upgrade() -> None:
    # 안전한 데이터 마이그레이션
    connection = op.get_bind()
    
    # 배치 처리로 대용량 데이터 처리
    result = connection.execute("SELECT id, email FROM users")
    for row in result:
        new_email = row.email.lower()
        connection.execute(
            "UPDATE users SET email = %s WHERE id = %s",
            (new_email, row.id)
        )

def downgrade() -> None:
    # 롤백 로직 (필요한 경우)
    pass
```

### 4. 성능 최적화

```python
def upgrade() -> None:
    # 대용량 테이블에 인덱스 추가 시
    op.create_index('idx_large_table_column', 'large_table', ['column'], 
                   postgresql_concurrently=True)
```

## 🔍 유용한 명령어

### Alembic 직접 사용

```bash
# 마이그레이션 상태 확인
alembic current
alembic history
alembic show

# 특정 버전으로 이동
alembic upgrade +2    # 2개 버전 앞으로
alembic downgrade -1  # 1개 버전 뒤로
alembic upgrade head  # 최신 버전으로
alembic downgrade base # 초기 버전으로

# 마이그레이션 정보 확인
alembic info
```

### Docker 환경에서 디버깅

```bash
# 컨테이너에 접속
docker exec -it pet-happy-api bash

# 데이터베이스 접속
docker exec -it pet-happy-api psql -U $POSTGRES_USER -d $POSTGRES_DATABASE_NAME

# 마이그레이션 테이블 확인
SELECT * FROM alembic_version;
```

## 📚 추가 자료

- [Alembic 공식 문서](https://alembic.sqlalchemy.org/)
- [SQLAlchemy 마이그레이션 가이드](https://docs.sqlalchemy.org/en/14/core/engines.html)
- [PostgreSQL 마이그레이션 모범 사례](https://www.postgresql.org/docs/current/ddl.html)

---

**💡 팁**: 마이그레이션을 실행하기 전에 항상 백업을 생성하고, 프로덕션 환경에서는 충분한 테스트를 거친 후 적용하세요! 