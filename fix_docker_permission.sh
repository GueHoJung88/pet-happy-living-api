#!/bin/bash

# 📦 Docker 권한 문제 자동 수정 스크립트
# 작성자: IT 총괄 정규호 (ConAI)
# 작성일: 2025-07-17
# 설명: Docker 사용 시 "permission denied" 오류를 해결하기 위해 현재 사용자를 docker 그룹에 추가하고, 권한 설정을 적용합니다.

set -e

USER_NAME=$(whoami)
DOCKER_SOCK="/var/run/docker.sock"

echo "🔧 현재 사용자: $USER_NAME"

# 1. docker 그룹 존재 확인
if ! getent group docker > /dev/null; then
    echo "➕ docker 그룹이 존재하지 않아 새로 생성합니다."
    sudo groupadd docker
else
    echo "✅ docker 그룹이 이미 존재합니다."
fi

# 2. 사용자 docker 그룹에 추가
echo "👤 사용자를 docker 그룹에 추가 중..."
sudo usermod -aG docker $USER_NAME

# 3. 소켓 권한 확인
echo "🔍 docker.sock 권한 확인:"
ls -l $DOCKER_SOCK || echo "⚠️  docker.sock 파일이 아직 존재하지 않음 (Docker 데몬이 실행 중인지 확인하세요)"

# 4. 그룹 변경 즉시 적용 (로그아웃 없이 적용)
echo "🔄 현재 셸에 docker 그룹 적용 (newgrp)..."
newgrp docker <<EONG
echo "✅ docker 권한 적용 완료! 테스트로 'docker ps'를 실행합니다."
docker ps || echo "⚠️  Docker 데몬이 실행되고 있지 않거나, 추가 권한 필요"
EONG

echo "🎉 모든 작업 완료! 이제 'docker' 명령을 권한 문제 없이 사용할 수 있어야 합니다."
