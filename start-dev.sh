#!/bin/bash

set -e

SERVICE_NAME="pet-happy-api"
COMPOSE_FILES="-f docker-compose.base.yml -f docker-compose.dev.yml"
ENV_FILE=".env.dev"

echo "✅ [START: DEV] Starting $SERVICE_NAME in development mode"

# 🔁 인자 파싱: --build 옵션 확인
BUILD_FLAG=""
BUILD_MODE=false
for arg in "$@"; do
  if [ "$arg" == "--build" ]; then
    BUILD_FLAG="--build"
    BUILD_MODE=true
    break
  fi
done

# ℹ️ 안내 메시지 출력
if [ "$BUILD_MODE" = false ]; then
  echo ""
  echo "⚠️  [INFO] '--build' 옵션 없이 실행되었습니다. 기존 Docker 이미지를 재사용합니다."
  echo "🔄 코드 변경 사항이 반영되지 않거나, 아래와 같은 경우에는 반드시 '--build' 옵션을 사용하세요:"
  echo "  - requirements.txt 변경"
  echo "  - Dockerfile 수정"
  echo "  - 의존성 패키지 추가/삭제"
  echo "👉 예시: ./start-dev.sh --build"
  echo ""
fi

# 🐳 docker compose up
docker compose $COMPOSE_FILES --env-file $ENV_FILE up -d $BUILD_FLAG --force-recreate

echo "📦 [STATUS] Container status:"
docker compose $COMPOSE_FILES ps

echo ""
echo "🌐 [SERVICE URL]"
echo "📖 API Documentation: http://localhost:8000/docs"
echo "🔗 Health Check: http://localhost:8000/api/v1/health"
echo ""
