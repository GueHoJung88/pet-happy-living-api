#!/bin/bash

set -e

SERVICE_NAME="pet-happy-api"
COMPOSE_FILES="-f docker-compose.base.yml -f docker-compose.prod.yml"
ENV_FILE=".env.prod"

echo "🚀 [START: PROD] Starting $SERVICE_NAME in production mode"

# 🔍 --build 옵션 여부 확인
BUILD_FLAG=""
BUILD_MODE=false
for arg in "$@"; do
  if [ "$arg" == "--build" ]; then
    BUILD_FLAG="--build"
    BUILD_MODE=true
    break
  fi
done

# 안내 메시지
if [ "$BUILD_MODE" = false ]; then
  echo "⚠️  [INFO] Docker 이미지를 새로 빌드하지 않고 실행합니다. 변경 사항이 있다면 '--build' 옵션을 사용하세요."
  echo "⚠️  [INFO] '--build' 옵션 없이 실행되었습니다. 기존 Docker 이미지를 재사용합니다."
  echo "🔄 코드 변경 사항이 반영되지 않거나, 아래와 같은 경우에는 반드시 '--build' 옵션을 사용하세요:"
  echo "  - requirements.txt 변경"
  echo "  - Dockerfile 수정"
  echo "  - 의존성 패키지 추가/삭제"
  echo "👉 예시: ./start-prod.sh --build"
  echo ""
fi

# 🐳 docker compose 실행
docker compose $COMPOSE_FILES --env-file $ENV_FILE up -d $BUILD_FLAG --force-recreate

echo "📦 [STATUS] Container status:"
docker compose $COMPOSE_FILES ps

echo ""
echo "🌐 [SERVICE URL]"
echo "📖 API Documentation: http://ec2-3-37-57-105.ap-northeast-2.compute.amazonaws.com:8000/docs"
echo "🔗 Health Check: http://ec2-3-37-57-105.ap-northeast-2.compute.amazonaws.com:8000/api/v1/health"
echo ""
