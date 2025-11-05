# DataSherpa Setup Guide

## Prerequisites

- Docker and Docker Compose
- Python 3.11+
- Node.js 18+
- kubectl (for Kubernetes deployment)
- Access to NVIDIA NIM APIs (for LLM and Embedding services)

## Local Development Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd DataSharpa
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your API keys
nano .env
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

### 4. Start Backend API

```bash
cd backend
python app.py
```

The backend will be available at `http://localhost:8000`
The frontend will be available at `http://localhost:3000`

## Docker Deployment

### 1. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
LLM_API_ENDPOINT=http://your-llm-endpoint/v1/chat/completions
LLM_API_KEY=your_llm_api_key
EMBEDDING_API_ENDPOINT=http://your-embedding-endpoint/v1/embeddings
EMBEDDING_API_KEY=your_embedding_api_key
```

### 2. Build and Run with Docker Compose

```bash
# Build images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- MySQL: localhost:3306

## Kubernetes (EKS) Deployment

### 1. Create EKS Cluster

```bash
eksctl create cluster \
  --name datasherpa-cluster \
  --region us-west-2 \
  --nodegroup-name datasherpa-nodes \
  --node-type t3.medium \
  --nodes 3 \
  --nodes-min 2 \
  --nodes-max 5
```

### 2. Build and Push Docker Images

```bash
# Build images
docker build -t datasherpa-backend:latest ./backend
docker build -t datasherpa-frontend:latest ./frontend

# Tag for ECR
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-west-2.amazonaws.com

docker tag datasherpa-backend:latest <account-id>.dkr.ecr.us-west-2.amazonaws.com/datasherpa-backend:latest
docker tag datasherpa-frontend:latest <account-id>.dkr.ecr.us-west-2.amazonaws.com/datasherpa-frontend:latest

# Push to ECR
docker push <account-id>.dkr.ecr.us-west-2.amazonaws.com/datasherpa-backend:latest
docker push <account-id>.dkr.ecr.us-west-2.amazonaws.com/datasherpa-frontend:latest
```

### 3. Deploy to Kubernetes

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Create secrets (edit secrets.yaml.example first)
cp k8s/secrets.yaml.example k8s/secrets.yaml
# Edit k8s/secrets.yaml with your actual credentials
kubectl apply -f k8s/secrets.yaml

# Create configmap
kubectl apply -f k8s/configmap.yaml

# Deploy backend
kubectl apply -f k8s/backend-deployment.yaml

# Deploy frontend
kubectl apply -f k8s/frontend-deployment.yaml

# Check status
kubectl get pods -n datasherpa
kubectl get services -n datasherpa
```

### 4. Access the Application

```bash
# Get LoadBalancer URLs
kubectl get svc -n datasherpa

# Access frontend
kubectl get svc datasherpa-frontend-service -n datasherpa -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'

# Access backend API
kubectl get svc datasherpa-backend-service -n datasherpa -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
```

## CLI Tool Setup

### 1. Install CLI Dependencies

```bash
cd cli
pip install -r requirements.txt
```

### 2. Make CLI Executable

```bash
chmod +x datasherpa.py
```

### 3. Use the CLI

```bash
# Health check
./datasherpa.py health

# Upload logs
./datasherpa.py upload /path/to/logfile.log

# Ask debugging question
./datasherpa.py debug "Why is my Spark job failing?"

# Generate shell command
./datasherpa.py shell "Count unique errors in log file"

# Generate documentation
./datasherpa.py docs /path/to/pipeline.py --output docs.md

# Get resource optimization
./datasherpa.py optimize /path/to/job-history.txt
```

## Configuration

### LLM Integration

DataSherpa uses the llama-3.1-nemotron-nano-8B-v1 model. Configure the endpoint:

```bash
LLM_API_ENDPOINT=http://your-nim-endpoint/v1/chat/completions
LLM_API_KEY=your_api_key
```

### Embedding Service

For log retrieval, configure the embedding endpoint:

```bash
EMBEDDING_API_ENDPOINT=http://your-nim-endpoint/v1/embeddings
EMBEDDING_API_KEY=your_api_key
```

## Troubleshooting

### Backend not starting
- Check if port 8000 is available
- Verify environment variables are set correctly
- Check logs: `docker-compose logs backend`

### Frontend not connecting to backend
- Verify REACT_APP_API_URL is set correctly
- Check CORS settings in backend
- Ensure backend is running

### Kubernetes pods not starting
- Check pod logs: `kubectl logs <pod-name> -n datasherpa`
- Verify secrets are created correctly
- Check resource limits

## Next Steps

1. Configure your LLM and Embedding API endpoints
2. Upload sample logs to test the system
3. Try the debugging feature with natural language questions
4. Integrate with your CI/CD pipeline using the CLI tool
5. Set up monitoring and alerts

For more information, see the main README.md
