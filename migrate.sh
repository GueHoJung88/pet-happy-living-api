#!/bin/bash
# =============================
# Docker 환경에서 마이그레이션 실행 스크립트
# =============================

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 로그 함수
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 도움말 함수
show_help() {
    echo "
🔧 FastAPI DB 마이그레이션 도구 (Docker 환경)

사용법:
  ./migrate.sh <명령어> [옵션]

명령어:
  init                    - 마이그레이션 초기화
  create <메시지>         - 새 마이그레이션 생성
  upgrade                 - 데이터베이스 업그레이드
  downgrade <버전>        - 데이터베이스 다운그레이드
  history                 - 마이그레이션 히스토리 표시
  current                 - 현재 버전 표시
  show                    - 대기 중인 마이그레이션 표시
  reset                   - 데이터베이스 초기화 (주의!)

예시:
  ./migrate.sh create \"Add pet registration table\"
  ./migrate.sh upgrade
  ./migrate.sh downgrade -1
  ./migrate.sh reset

주의: reset 명령어는 모든 데이터를 삭제합니다!
"
}

# 컨테이너 이름 확인
get_container_name() {
    local container_name=$(docker ps --filter "name=pet-happy-api" --format "{{.Names}}" | head -1)
    if [ -z "$container_name" ]; then
        log_error "pet-happy-api 컨테이너를 찾을 수 없습니다."
        log_info "Docker 컨테이너가 실행 중인지 확인해주세요."
        exit 1
    fi
    echo "$container_name"
}

# 마이그레이션 초기화
init_migration() {
    log_info "마이그레이션 초기화 중..."
    local container_name=$(get_container_name)
    
    docker exec -it "$container_name" alembic init alembic
    log_success "마이그레이션 초기화 완료"
}

# 새 마이그레이션 생성
create_migration() {
    if [ -z "$1" ]; then
        log_error "마이그레이션 메시지를 입력해주세요."
        exit 1
    fi
    
    log_info "마이그레이션 생성 중: $1"
    local container_name=$(get_container_name)
    
    docker exec -it "$container_name" alembic revision --autogenerate -m "$1"
    log_success "마이그레이션 생성 완료"
}

# 데이터베이스 업그레이드
upgrade_database() {
    log_info "데이터베이스 업그레이드 중..."
    local container_name=$(get_container_name)
    
    docker exec -it "$container_name" alembic upgrade head
    log_success "데이터베이스 업그레이드 완료"
}

# 데이터베이스 다운그레이드
downgrade_database() {
    if [ -z "$1" ]; then
        log_error "다운그레이드할 버전을 입력해주세요."
        exit 1
    fi
    
    log_warning "데이터베이스 다운그레이드 중: $1"
    local container_name=$(get_container_name)
    
    docker exec -it "$container_name" alembic downgrade "$1"
    log_success "데이터베이스 다운그레이드 완료"
}

# 마이그레이션 히스토리 표시
show_history() {
    log_info "마이그레이션 히스토리:"
    local container_name=$(get_container_name)
    
    docker exec -it "$container_name" alembic history
}

# 현재 버전 표시
show_current() {
    log_info "현재 마이그레이션 버전:"
    local container_name=$(get_container_name)
    
    docker exec -it "$container_name" alembic current
}

# 대기 중인 마이그레이션 표시
show_pending() {
    log_info "대기 중인 마이그레이션:"
    local container_name=$(get_container_name)
    
    docker exec -it "$container_name" alembic show
}

# 데이터베이스 초기화 (주의!)
reset_database() {
    log_warning "⚠️  주의: 이 작업은 모든 데이터를 삭제합니다!"
    read -p "정말로 데이터베이스를 초기화하시겠습니까? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "데이터베이스 초기화 중..."
        local container_name=$(get_container_name)
        
        # 모든 마이그레이션을 다운그레이드
        docker exec -it "$container_name" alembic downgrade base
        
        # 마이그레이션 테이블 삭제
        docker exec -it "$container_name" psql -U $POSTGRES_USER -d $POSTGRES_DATABASE_NAME -c "DROP TABLE IF EXISTS alembic_version;"
        
        log_success "데이터베이스 초기화 완료"
    else
        log_info "초기화가 취소되었습니다."
    fi
}

# 메인 함수
main() {
    if [ $# -eq 0 ]; then
        show_help
        exit 0
    fi
    
    case "$1" in
        "init")
            init_migration
            ;;
        "create")
            create_migration "$2"
            ;;
        "upgrade")
            upgrade_database
            ;;
        "downgrade")
            downgrade_database "$2"
            ;;
        "history")
            show_history
            ;;
        "current")
            show_current
            ;;
        "show")
            show_pending
            ;;
        "reset")
            reset_database
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            log_error "알 수 없는 명령어: $1"
            show_help
            exit 1
            ;;
    esac
}

# 스크립트 실행
main "$@" 