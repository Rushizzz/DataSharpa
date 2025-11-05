# DataSherpa Architecture

## System Overview

DataSherpa is a GenAI-powered assistant for Data Engineers, built with a microservices architecture designed for scalability and deployed on Amazon EKS.

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│                    (React + TailwindCSS)                     │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST
┌──────────────────────▼──────────────────────────────────────┐
│                      Backend API                             │
│                       (FastAPI)                              │
├──────────────────────────────────────────────────────────────┤
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │    LLM     │  │ Retrieval  │  │   Shell    │            │
│  │  Service   │  │  Service   │  │ Generator  │            │
│  └────────────┘  └────────────┘  └────────────┘            │
│  ┌────────────┐  ┌────────────┐                             │
│  │ Resource   │  │    Docs    │                             │
│  │ Optimizer  │  │   Agent    │                             │
│  └────────────┘  └────────────┘                             │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
┌───────▼──────┐ ┌────▼─────┐ ┌──────▼──────┐
│ llama-3.1    │ │ Embedding│ │   MySQL     │
│ nemotron     │ │   NIM    │ │  Database   │
│   (NIM)      │ │          │ │             │
└──────────────┘ └──────────┘ └─────────────┘
```

## Components

### Frontend (React)
- **Technology**: React 18, TailwindCSS, Lucide Icons
- **Features**:
  - Dashboard with system status
  - Natural language debugging interface
  - Log upload and management
  - Shell command generator UI
  - Resource optimization advisor
  - Documentation generator
- **Communication**: REST API calls to backend

### Backend API (FastAPI)
- **Technology**: Python 3.11, FastAPI, Uvicorn
- **Endpoints**:
  - `/debug` - Natural language debugging
  - `/upload-logs` - Log file upload and indexing
  - `/generate-shell-command` - Shell command generation
  - `/optimize-resources` - Resource optimization
  - `/generate-documentation` - Auto-documentation
  - `/search-logs` - Semantic log search
- **Services**:
  - **LLM Service**: Interfaces with llama-3.1-nemotron-nano-8B-v1
  - **Retrieval Service**: Embedding and semantic search
  - **Shell Generator**: Bash command generation
  - **Resource Optimizer**: Spark configuration recommendations
  - **Documentation Agent**: Markdown doc generation

### LLM Integration
- **Model**: llama-3.1-nemotron-nano-8B-v1
- **Purpose**: 
  - Natural language understanding
  - Code analysis
  - Error explanation
  - Command generation
  - Documentation generation
- **API**: OpenAI-compatible chat completions endpoint

### Retrieval System
- **Embedding Model**: NVIDIA NV-EmbedQA-E5-v5
- **Purpose**:
  - Log indexing
  - Semantic search
  - Context retrieval for debugging
- **Storage**: In-memory index (can be replaced with vector DB)

### CLI Tool
- **Technology**: Python with argparse
- **Commands**:
  - `health` - Check API health
  - `upload` - Upload log files
  - `debug` - Ask debugging questions
  - `shell` - Generate shell commands
  - `docs` - Generate documentation
  - `optimize` - Get resource recommendations
- **Use Case**: CI/CD integration, automation

### Database
- **Technology**: MySQL 8.0
- **Purpose**: 
  - User data storage
  - Pipeline metadata
  - Configuration storage
  - Audit logs

## Deployment Architecture

### Docker Compose (Development)
```yaml
services:
  - mysql (Database)
  - backend (FastAPI API)
  - frontend (React App)
```

### Kubernetes (Production - EKS)
```
┌─────────────────────────────────────────────┐
│              Amazon EKS Cluster              │
├─────────────────────────────────────────────┤
│  Namespace: datasherpa                      │
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │  Frontend Deployment (2 replicas)    │  │
│  │  - LoadBalancer Service              │  │
│  └──────────────────────────────────────┘  │
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │  Backend Deployment (3 replicas)     │  │
│  │  - LoadBalancer Service              │  │
│  │  - Health checks                     │  │
│  │  - Auto-scaling enabled              │  │
│  └──────────────────────────────────────┘  │
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │  ConfigMaps & Secrets                │  │
│  │  - API endpoints                     │  │
│  │  - API keys                          │  │
│  └──────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

## Data Flow

### 1. Natural Language Debugging
```
User Question → Backend API → Retrieval Service (search logs)
                            → LLM Service (generate answer)
                            → Response with answer + log traces
```

### 2. Log Upload & Indexing
```
Log File → Backend API → Chunk text
                       → Generate embeddings (NIM)
                       → Store in index
                       → Return confirmation
```

### 3. Shell Command Generation
```
User Query → Backend API → LLM Service (analyze query)
                         → Generate command + explanation
                         → Return with examples
```

### 4. Resource Optimization
```
Job History → Backend API → LLM Service (analyze patterns)
                          → Rule-based analysis
                          → Generate recommendations
                          → Return config templates
```

### 5. Documentation Generation
```
Pipeline Code → Backend API → LLM Service (analyze code)
                            → Generate markdown
                            → Add standard sections
                            → Return documentation
```

## Security Considerations

1. **API Keys**: Stored in Kubernetes secrets
2. **CORS**: Configured for specific origins
3. **Input Validation**: All endpoints validate input
4. **Rate Limiting**: Can be added via API Gateway
5. **Authentication**: Can be added (OAuth2, JWT)

## Scalability

1. **Horizontal Scaling**: 
   - Backend: 3+ replicas in K8s
   - Frontend: 2+ replicas in K8s
   - Auto-scaling based on CPU/memory

2. **Caching**: 
   - Can add Redis for frequently accessed data
   - LLM response caching

3. **Database**:
   - MySQL with read replicas
   - Can migrate to managed RDS

4. **Vector Storage**:
   - Current: In-memory
   - Production: Pinecone, Weaviate, or Milvus

## Monitoring & Observability

1. **Logs**: 
   - Application logs via stdout
   - Aggregated in CloudWatch

2. **Metrics**:
   - Prometheus for metrics collection
   - Grafana for visualization

3. **Tracing**:
   - OpenTelemetry for distributed tracing

4. **Health Checks**:
   - Liveness probes
   - Readiness probes

## Integration Points

1. **Apache Spark**: 
   - Analyze job logs
   - Optimize configurations

2. **Apache Airflow**:
   - Parse DAG errors
   - Generate documentation

3. **Linux Shell**:
   - Process log files
   - Generate commands

4. **CI/CD**:
   - CLI tool integration
   - Automated health checks
   - Documentation generation

## Future Enhancements

1. **Real-time Monitoring**: WebSocket support for live log streaming
2. **Multi-tenancy**: Support for multiple teams/projects
3. **Advanced Analytics**: Pipeline performance trends
4. **Custom Models**: Fine-tuned models for specific use cases
5. **Integration Hub**: Connectors for more data tools
