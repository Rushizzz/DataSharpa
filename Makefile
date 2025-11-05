.PHONY: help install dev build docker-build docker-up docker-down k8s-deploy clean

help:
	@echo "DataSherpa - Available Commands"
	@echo "================================"
	@echo "install        - Install all dependencies"
	@echo "dev            - Start development servers"
	@echo "build          - Build production bundles"
	@echo "docker-build   - Build Docker images"
	@echo "docker-up      - Start Docker Compose services"
	@echo "docker-down    - Stop Docker Compose services"
	@echo "k8s-deploy     - Deploy to Kubernetes"
	@echo "clean          - Clean build artifacts"

install:
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "Installing CLI dependencies..."
	cd cli && pip install -r requirements.txt

dev:
	@echo "Starting development servers..."
	@echo "Backend will run on http://localhost:8000"
	@echo "Frontend will run on http://localhost:3000"
	@make -j 2 dev-backend dev-frontend

dev-backend:
	cd backend && python app.py

dev-frontend:
	cd frontend && npm start

build:
	@echo "Building production bundles..."
	cd frontend && npm run build

docker-build:
	@echo "Building Docker images..."
	docker-compose build

docker-up:
	@echo "Starting Docker Compose services..."
	docker-compose up -d
	@echo "Services started:"
	@echo "  Frontend: http://localhost:3000"
	@echo "  Backend:  http://localhost:8000"
	@echo "  MySQL:    localhost:3306"

docker-down:
	@echo "Stopping Docker Compose services..."
	docker-compose down

k8s-deploy:
	@echo "Deploying to Kubernetes..."
	kubectl apply -f k8s/namespace.yaml
	kubectl apply -f k8s/configmap.yaml
	kubectl apply -f k8s/secrets.yaml
	kubectl apply -f k8s/backend-deployment.yaml
	kubectl apply -f k8s/frontend-deployment.yaml
	@echo "Checking deployment status..."
	kubectl get pods -n datasherpa

clean:
	@echo "Cleaning build artifacts..."
	rm -rf backend/__pycache__
	rm -rf backend/**/__pycache__
	rm -rf frontend/build
	rm -rf frontend/node_modules
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
