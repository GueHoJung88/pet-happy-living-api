# 🐾 Pet Happy Living API

**A FastAPI-based microservice for recommending pet-friendly residential areas, built on Kubernetes and ready for ML/LLM/IoT extensions.**

---

## 🗂️ Project Overview

**Pet Happy Living API**는 반려동물의 행복한 삶을 위한 거주 지역을 추천하는 웹 서비스의 핵심 API 서버입니다. 도시 환경 데이터, 공공 인프라, 소음·녹지·밀집도 등 다양한 요소를 분석하여 반려동물과 보호자에게 최적의 거주지를 추천하는 AI 기반 마이크로서비스입니다.

---

## 🛠️ Tech Stack

| Layer            | Tech                             |
|------------------|----------------------------------|
| Language         | Python 3.10                      |
| Framework        | FastAPI                         |
| Web Server       | Uvicorn (ASGI)                   |
| Containerization | Docker, Kubernetes (K8s)         |
| DB               | PostgreSQL, Redis                |
| Infra            | AWS EC2                          |
| Docs & Test      | OpenAPI, Swagger UI, curl        |

---

## 📁 Project Structure

```
pet-happy-api/
├── app/
│   ├── main.py                # FastAPI 엔트리포인트
│   ├── api/
│   │   └── endpoints.py       # API 엔드포인트 (e.g., /health)
│   └── core/
│       └── config.py          # 설정 및 환경변수 로딩
├── requirements.txt           # Python 패키지 목록
├── Dockerfile                 # Docker 이미지 설정
└── README.md                  # 프로젝트 설명 문서
```

---

## 🚀 Getting Started

### 1️⃣ Clone this repo

```bash
git clone https://github.com/<your-username>/pet-happy-living-api.git
cd pet-happy-living-api
```

### 2️⃣ Build & Run with Docker

```bash
docker build -t pet-happy-api .
docker run -d -p 8000:8000 pet-happy-api
```

**접속 DEV**  : <a href="http://localhost:8000/docs" target="_blank">http://localhost:8000/docs</a>

**접속 PROD** : <a href="http://ec2-3-37-57-105.ap-northeast-2.compute.amazonaws.com:8000/docs" target="_blank">http://ec2-3-37-57-105.ap-northeast-2.compute.amazonaws.com:8000/docs</a>

#### 📦 Install Docker (Ubuntu 기준)

```bash
# 1. 기존 도커가 있다면 제거
sudo apt remove docker docker-engine docker.io containerd runc

# 2. 의존 패키지 설치
sudo apt update
sudo apt install -y ca-certificates curl gnupg

# 3. GPG 키 등록
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 4. Docker 공식 리포지토리 등록
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 5. Docker 설치
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 6. 사용자에게 docker 권한 부여
sudo usermod -aG docker $USER
newgrp docker  # 현재 세션에 바로 적용

### 3️⃣ Kubernetes 배포

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

---

## ✅ Health Check

```bash
curl http://<your-ip>/health
# {"status": "ok"}
```

---

## 📈 Future Extensions(예시)

- 🧠 LLM + RAG 기반 거주지 질문응답
- 📊 데이터 분석 기반 기회비용 지표 제공
- 📡 IoT 센서 연동 (소음, 온도, 산책량 등)
- 🐶 사용자 기반 반려동물 특성 맞춤 추천

---

## 📝 License

MIT License
