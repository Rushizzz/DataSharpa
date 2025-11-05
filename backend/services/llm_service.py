"""
LLM Service for DataSherpa
Integrates with llama-3.1-nemotron-nano-8B-v1 model
"""
import os
from typing import List, Dict, Optional
import requests
import json


class LLMService:
    def __init__(self):
        self.model_name = "llama-3.1-nemotron-nano-8b-v1"
        self.api_endpoint = os.getenv("LLM_API_ENDPOINT", "http://localhost:8001/v1/chat/completions")
        self.api_key = os.getenv("LLM_API_KEY", "")
        
    def _call_llm(self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 1024) -> str:
        """
        Call the LLM API with given messages
        """
        try:
            headers = {
                "Content-Type": "application/json",
            }
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            payload = {
                "model": self.model_name,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            response = requests.post(
                self.api_endpoint,
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                # Fallback for development/testing
                return self._fallback_response(messages)
                
        except Exception as e:
            print(f"LLM API Error: {e}")
            return self._fallback_response(messages)
    
    def _fallback_response(self, messages: List[Dict[str, str]]) -> str:
        """
        Fallback response when LLM API is not available
        """
        return "LLM service is currently unavailable. Please configure LLM_API_ENDPOINT and try again."
    
    def generate_debug_answer(self, question: str, context: Optional[str], relevant_logs: List[Dict]) -> str:
        """
        Generate debugging answer based on question and logs
        """
        logs_context = "\n".join([f"- {log['text']}" for log in relevant_logs[:3]])
        
        messages = [
            {
                "role": "system",
                "content": """You are DataSherpa, an expert Data Engineering assistant. 
                You help debug Apache Spark jobs, Airflow DAGs, and data pipelines.
                Provide clear, actionable answers with specific references to log traces."""
            },
            {
                "role": "user",
                "content": f"""Question: {question}

Context: {context or 'No additional context provided'}

Relevant Log Traces:
{logs_context}

Please provide a detailed answer with:
1. Root cause analysis
2. Specific error explanation
3. Recommended fix
4. Prevention tips"""
            }
        ]
        
        return self._call_llm(messages, temperature=0.3, max_tokens=2048)
    
    def generate_shell_command(self, query: str, log_format: Optional[str], error_pattern: Optional[str]) -> Dict:
        """
        Generate shell command based on query
        """
        messages = [
            {
                "role": "system",
                "content": """You are an expert in Linux shell commands, especially awk, sed, grep, and log processing.
                Generate optimized one-liners for data engineering tasks."""
            },
            {
                "role": "user",
                "content": f"""Generate a shell command for: {query}

Log format: {log_format or 'Standard log format'}
Error pattern: {error_pattern or 'Not specified'}

Provide:
1. The command
2. Explanation of what it does
3. Example usage"""
            }
        ]
        
        response = self._call_llm(messages, temperature=0.2, max_tokens=1024)
        
        return {
            "command": response.split("\n")[0] if response else "",
            "explanation": response,
            "examples": []
        }
    
    def analyze_resource_optimization(self, job_history: str, cluster_metrics: Optional[Dict]) -> str:
        """
        Analyze and provide resource optimization recommendations
        """
        metrics_str = json.dumps(cluster_metrics, indent=2) if cluster_metrics else "No metrics provided"
        
        messages = [
            {
                "role": "system",
                "content": """You are a Spark performance optimization expert.
                Analyze job history and cluster metrics to provide specific configuration recommendations."""
            },
            {
                "role": "user",
                "content": f"""Job History:
{job_history}

Cluster Metrics:
{metrics_str}

Provide specific recommendations for:
1. Executor configuration (cores, memory)
2. Driver configuration
3. Parallelism settings
4. Memory management
5. Shuffle optimization"""
            }
        ]
        
        return self._call_llm(messages, temperature=0.3, max_tokens=2048)
    
    def generate_documentation(self, pipeline_code: str, dag_code: Optional[str]) -> str:
        """
        Generate markdown documentation from code
        """
        messages = [
            {
                "role": "system",
                "content": """You are a technical documentation expert.
                Create clear, comprehensive markdown documentation with diagrams and code snippets."""
            },
            {
                "role": "user",
                "content": f"""Generate documentation for this data pipeline:

Pipeline Code:
```python
{pipeline_code}
```

{f'DAG Code:\n```python\n{dag_code}\n```' if dag_code else ''}

Include:
1. Overview
2. Architecture diagram (mermaid)
3. Component descriptions
4. Data flow
5. Configuration parameters
6. Usage examples
7. Troubleshooting tips"""
            }
        ]
        
        return self._call_llm(messages, temperature=0.4, max_tokens=4096)
