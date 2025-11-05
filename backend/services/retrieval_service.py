"""
Retrieval Service for log embedding and semantic search
Uses embedding models for indexing and retrieval
"""
import os
from typing import List, Dict
import numpy as np
from datetime import datetime
import json
import hashlib


class RetrievalService:
    def __init__(self):
        self.embedding_endpoint = os.getenv("EMBEDDING_API_ENDPOINT", "http://localhost:8002/v1/embeddings")
        self.api_key = os.getenv("EMBEDDING_API_KEY", "")
        self.index = []  # Simple in-memory index (use vector DB in production)
        self.documents = {}
        
    def _get_embedding(self, text: str) -> List[float]:
        """
        Get embedding vector for text using NIM embedding API
        """
        try:
            import requests
            
            headers = {
                "Content-Type": "application/json",
            }
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            payload = {
                "input": text,
                "model": "nvidia/nv-embedqa-e5-v5"
            }
            
            response = requests.post(
                self.embedding_endpoint,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["data"][0]["embedding"]
            else:
                # Fallback: simple hash-based embedding for development
                return self._simple_embedding(text)
                
        except Exception as e:
            print(f"Embedding API Error: {e}")
            return self._simple_embedding(text)
    
    def _simple_embedding(self, text: str, dim: int = 384) -> List[float]:
        """
        Simple fallback embedding using hash
        """
        hash_val = int(hashlib.md5(text.encode()).hexdigest(), 16)
        np.random.seed(hash_val % (2**32))
        embedding = np.random.randn(dim).tolist()
        return embedding
    
    def _chunk_text(self, text: str, chunk_size: int = 500) -> List[str]:
        """
        Split text into chunks for indexing
        """
        lines = text.split('\n')
        chunks = []
        current_chunk = []
        current_size = 0
        
        for line in lines:
            line_size = len(line)
            if current_size + line_size > chunk_size and current_chunk:
                chunks.append('\n'.join(current_chunk))
                current_chunk = [line]
                current_size = line_size
            else:
                current_chunk.append(line)
                current_size += line_size
        
        if current_chunk:
            chunks.append('\n'.join(current_chunk))
        
        return chunks
    
    def index_logs(self, log_text: str, filename: str) -> Dict:
        """
        Index log text for semantic search
        """
        chunks = self._chunk_text(log_text)
        
        for i, chunk in enumerate(chunks):
            embedding = self._get_embedding(chunk)
            
            doc_id = f"{filename}_{i}"
            self.documents[doc_id] = {
                "text": chunk,
                "filename": filename,
                "chunk_id": i,
                "timestamp": datetime.now().isoformat()
            }
            
            self.index.append({
                "id": doc_id,
                "embedding": embedding
            })
        
        return {
            "chunks_count": len(chunks),
            "filename": filename
        }
    
    def search_logs(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Semantic search through indexed logs
        """
        if not self.index:
            return []
        
        query_embedding = self._get_embedding(query)
        
        # Calculate cosine similarity
        similarities = []
        for item in self.index:
            similarity = self._cosine_similarity(query_embedding, item["embedding"])
            similarities.append({
                "id": item["id"],
                "score": similarity
            })
        
        # Sort by similarity
        similarities.sort(key=lambda x: x["score"], reverse=True)
        
        # Get top results
        results = []
        for sim in similarities[:limit]:
            doc = self.documents.get(sim["id"])
            if doc:
                results.append({
                    "text": doc["text"],
                    "filename": doc["filename"],
                    "score": sim["score"],
                    "timestamp": doc["timestamp"]
                })
        
        return results
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors
        """
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return float(dot_product / (norm1 * norm2))
