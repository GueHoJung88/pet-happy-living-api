#!/bin/bash

set -e

# 원하는 버전 설정
COMPOSE_VERSION="v2.24.6"
ARCH="linux-x86_64"

# 설치 경로 설정
PLUGIN_DIR="$HOME/.docker/cli-plugins"
COMPOSE_BIN="$PLUGIN_DIR/docker-compose"

echo "📦 Docker Compose 설치 시작 (버전: $COMPOSE_VERSION)"

# 디렉토리 생성
mkdir -p "$PLUGIN_DIR"

# 기존 파일 백업
if [ -f "$COMPOSE_BIN" ]; then
    echo "🗂️ 기존 docker-compose 백업: $COMPOSE_BIN.bak"
    mv "$COMPOSE_BIN" "$COMPOSE_BIN.bak"
fi

# 다운로드 및 설치
curl -SL "https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-${ARCH}" -o "$COMPOSE_BIN"
chmod +x "$COMPOSE_BIN"

# PATH에 ~/.docker/cli-plugins 이 없으면 안내
if [[ ":$PATH:" != *":$PLUGIN_DIR:"* ]]; then
    echo "⚠️  경고: $PLUGIN_DIR 경로가 PATH에 없습니다."
    echo "👉 아래 줄을 ~/.bashrc 또는 ~/.zshrc에 추가해 주세요:"
    echo ""
    echo "export PATH=\"\$HOME/.docker/cli-plugins:\$PATH\""
    echo ""
fi

# 확인
echo ""
echo "✅ 설치 완료!"
docker compose version