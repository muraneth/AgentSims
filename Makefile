.PHONY: docker-build docker-run docker-clean start stop

# 镜像名称
IMAGE_REGISTRY := jpccr.ccs.tencentyun.com
IMAGE_GROUP := llm-town
VERSION := 0.1.15

# 构建 Docker 镜像
build-contracts:
	docker build -t ${IMAGE_REGISTRY}/${IMAGE_GROUP}/contracts:${VERSION} -f ./deployment/docker/Dockerfile.contracts .

build-client:
	docker build -t ${IMAGE_REGISTRY}/${IMAGE_GROUP}/client:${VERSION} -f ./deployment/docker/Dockerfile.client .

build-client-test:
	docker build -t ${IMAGE_REGISTRY}/${IMAGE_GROUP}/client-test:${VERSION} -f ./deployment/docker/Dockerfile.client-test .

build-client-live:
	docker build -t ${IMAGE_REGISTRY}/${IMAGE_GROUP}/client-live:${VERSION} -f ./deployment/docker/Dockerfile.client-live .

build: build-client

start:
	cd ./deployment/docker/llm_town && docker-compose up -d

start-test:
	cd ./deployment/docker/llm_town_test && docker-compose up -d

start-live:
	cd ./deployment/docker/llm_town_live && docker-compose up -d

stop:
	cd ./deployment/docker/llm_town && docker-compose down

stop-test:
	cd ./deployment/docker/llm_town_test && docker-compose down

stop-live:
	cd ./deployment/docker/llm_town_live && docker-compose down
