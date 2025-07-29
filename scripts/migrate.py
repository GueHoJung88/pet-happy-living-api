#!/usr/bin/env python3
# =============================
# 마이그레이션 관리 스크립트
# =============================

import os
import sys
import subprocess
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from app.core.config import get_settings

def run_command(command: str) -> None:
    """명령어를 실행하고 결과를 출력합니다."""
    print(f"실행 중: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print("출력:")
        print(result.stdout)
    
    if result.stderr:
        print("오류:")
        print(result.stderr)
    
    if result.returncode != 0:
        print(f"명령어 실행 실패 (종료 코드: {result.returncode})")
        sys.exit(1)

def init_migration() -> None:
    """마이그레이션을 초기화합니다."""
    print("🔧 마이그레이션 초기화 중...")
    run_command("alembic init alembic")
    print("✅ 마이그레이션 초기화 완료")

def create_migration(message: str) -> None:
    """새로운 마이그레이션을 생성합니다."""
    print(f"📝 마이그레이션 생성 중: {message}")
    run_command(f'alembic revision --autogenerate -m "{message}"')
    print("✅ 마이그레이션 생성 완료")

def upgrade_database() -> None:
    """데이터베이스를 최신 버전으로 업그레이드합니다."""
    print("⬆️ 데이터베이스 업그레이드 중...")
    run_command("alembic upgrade head")
    print("✅ 데이터베이스 업그레이드 완료")

def downgrade_database(revision: str) -> None:
    """데이터베이스를 특정 버전으로 다운그레이드합니다."""
    print(f"⬇️ 데이터베이스 다운그레이드 중: {revision}")
    run_command(f"alembic downgrade {revision}")
    print("✅ 데이터베이스 다운그레이드 완료")

def show_migration_history() -> None:
    """마이그레이션 히스토리를 표시합니다."""
    print("📋 마이그레이션 히스토리:")
    run_command("alembic history")

def show_current_revision() -> None:
    """현재 마이그레이션 버전을 표시합니다."""
    print("📍 현재 마이그레이션 버전:")
    run_command("alembic current")

def show_pending_migrations() -> None:
    """대기 중인 마이그레이션을 표시합니다."""
    print("⏳ 대기 중인 마이그레이션:")
    run_command("alembic show")

def main():
    """메인 함수"""
    if len(sys.argv) < 2:
        print("""
🔧 FastAPI DB 마이그레이션 도구

사용법:
  python scripts/migrate.py <명령어> [옵션]

명령어:
  init                    - 마이그레이션 초기화
  create <메시지>         - 새 마이그레이션 생성
  upgrade                 - 데이터베이스 업그레이드
  downgrade <버전>        - 데이터베이스 다운그레이드
  history                 - 마이그레이션 히스토리 표시
  current                 - 현재 버전 표시
  show                    - 대기 중인 마이그레이션 표시

예시:
  python scripts/migrate.py create "Add pet registration table"
  python scripts/migrate.py upgrade
  python scripts/migrate.py downgrade -1
        """)
        return

    command = sys.argv[1]

    if command == "init":
        init_migration()
    elif command == "create":
        if len(sys.argv) < 3:
            print("❌ 메시지를 입력해주세요.")
            return
        message = sys.argv[2]
        create_migration(message)
    elif command == "upgrade":
        upgrade_database()
    elif command == "downgrade":
        if len(sys.argv) < 3:
            print("❌ 다운그레이드할 버전을 입력해주세요.")
            return
        revision = sys.argv[2]
        downgrade_database(revision)
    elif command == "history":
        show_migration_history()
    elif command == "current":
        show_current_revision()
    elif command == "show":
        show_pending_migrations()
    else:
        print(f"❌ 알 수 없는 명령어: {command}")

if __name__ == "__main__":
    main() 