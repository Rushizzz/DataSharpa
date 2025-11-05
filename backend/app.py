"""
DataSherpa - GenAI-powered Data Engineering Assistant
Main FastAPI application
"""
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from services.llm_service import LLMService
from services.retrieval_service import RetrievalService
from services.shell_generator import ShellCommandGenerator
from services.resource_optimizer import ResourceOptimizer
from services.documentation_agent import DocumentationAgent

app = FastAPI(
    title="DataSherpa API",
    description="GenAI-powered assistant for Data Engineers",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
llm_service = LLMService()
retrieval_service = RetrievalService()
shell_generator = ShellCommandGenerator(llm_service)
resource_optimizer = ResourceOptimizer(llm_service)
documentation_agent = DocumentationAgent(llm_service)


class DebugQuery(BaseModel):
    question: str
    context: Optional[str] = None


class ShellCommandRequest(BaseModel):
    query: str
    log_format: Optional[str] = None
    error_pattern: Optional[str] = None


class ResourceOptimizationRequest(BaseModel):
    job_history: str
    cluster_metrics: Optional[dict] = None


class DocumentationRequest(BaseModel):
    pipeline_code: str
    dag_code: Optional[str] = None


@app.get("/")
async def root():
    return {
        "message": "Welcome to DataSherpa API",
        "version": "1.0.0",
        "features": [
            "Natural Language Debugging",
            "Log Embedding & Retrieval",
            "Shell Command Generator",
            "Resource Optimization Advisor",
            "Auto-Documentation Agent"
        ]
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/debug")
async def debug_pipeline(query: DebugQuery):
    """
    Natural Language Debugging endpoint
    Ask questions about pipeline failures and get contextual answers
    """
    try:
        # Retrieve relevant logs
        relevant_logs = retrieval_service.search_logs(query.question)
        
        # Generate answer using LLM
        answer = llm_service.generate_debug_answer(
            question=query.question,
            context=query.context,
            relevant_logs=relevant_logs
        )
        
        return {
            "question": query.question,
            "answer": answer,
            "relevant_logs": relevant_logs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload-logs")
async def upload_logs(file: UploadFile = File(...)):
    """
    Upload pipeline logs for indexing and semantic search
    """
    try:
        content = await file.read()
        log_text = content.decode('utf-8')
        
        # Index the logs
        result = retrieval_service.index_logs(log_text, file.filename)
        
        return {
            "message": "Logs uploaded and indexed successfully",
            "filename": file.filename,
            "chunks_indexed": result["chunks_count"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-shell-command")
async def generate_shell_command(request: ShellCommandRequest):
    """
    Generate optimized shell commands based on query
    """
    try:
        command = shell_generator.generate_command(
            query=request.query,
            log_format=request.log_format,
            error_pattern=request.error_pattern
        )
        
        return {
            "query": request.query,
            "command": command["command"],
            "explanation": command["explanation"],
            "examples": command.get("examples", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/optimize-resources")
async def optimize_resources(request: ResourceOptimizationRequest):
    """
    Get Spark resource optimization suggestions
    """
    try:
        recommendations = resource_optimizer.analyze_and_recommend(
            job_history=request.job_history,
            cluster_metrics=request.cluster_metrics
        )
        
        return {
            "recommendations": recommendations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-documentation")
async def generate_documentation(request: DocumentationRequest):
    """
    Auto-generate markdown documentation from pipeline code
    """
    try:
        documentation = documentation_agent.generate_docs(
            pipeline_code=request.pipeline_code,
            dag_code=request.dag_code
        )
        
        return {
            "documentation": documentation
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search-logs")
async def search_logs(query: str, limit: int = 5):
    """
    Semantic search through indexed logs
    """
    try:
        results = retrieval_service.search_logs(query, limit=limit)
        return {
            "query": query,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
