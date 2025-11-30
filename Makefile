.PHONY: help install run test docker-build docker-run k8s-deploy clean

help:
	@echo "Cyfox - Makefile Commands"
	@echo ""
	@echo "  make install      - Install Python dependencies"
	@echo "  make run          - Run Cyfox locally"
	@echo "  make test         - Run tests"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"
	@echo "  make k8s-deploy   - Deploy to k3s cluster"
	@echo "  make clean        - Clean build artifacts"

install:
	pip install -r requirements.txt

run:
	python -m src.main

test:
	pytest tests/ -v

docker-build:
	docker build -t cyfox:latest .

docker-run:
	docker run --privileged --network host --pid host \
		-v /dev:/dev -v /sys:/sys cyfox:latest

k8s-deploy:
	kubectl apply -f k3s/namespace.yaml
	kubectl apply -f k3s/configmap.yaml
	kubectl apply -f k3s/deployment.yaml

clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

